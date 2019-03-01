# -*- coding: utf-8 -*-
import StringIO
import collections
import itertools
import bisect
from collections import namedtuple

from Android import overload
from XmlPullParser import XmlPullParser


class ParseError(SyntaxError):
    pass


class TokenIterator(object):

    _StateClass = namedtuple(
        '_StateClass', 'byte_index, line_number, column_number, depth, event_type, event_data'
    )

    def __init__(self, source, encoding=None, features=None):
        features = features or [False, False]
        close_source = False
        if not hasattr(source, "read"):
            source = open(source, "rb")
            close_source = True

        # fields
        self._file = source
        self._version = None
        self._encoding = None
        self._standalone = None
        self._close_file = close_source
        self.root = self._root = None
        self._error = None
        self._events = []
        self._index = 0

        # temporal states
        self._depth = 0
        self._isEmptyTag = False     # Usado para distinguir <a .... /> de <a ..></a>
        self._cdsect = False

        # manejo namespace
        self._ns = 0
        self._ns_index = [0]
        self._ns_stack = [2]
        self._ns_prefix = ['xmlns', 'xml']
        self._ns_namespace = ['http://www.w3.org/2000/xmlns', 'http://www.w3.org/XML/1998/namespace'
]

        self._init_parser_(encoding, features)
        dmy = self._StateClass(0, 1, 0, 0, XmlPullParser.START_DOCUMENT, None)
        self._events.append(dmy)

    def _init_parser_(self, encoding, features):
        # features = [enable_ns_parsing, process_doc_declaration]
        features = (features + [False, False])[:2]
        try:
            from xml.parsers import expat
        except ImportError:
            try:
                import pyexpat as expat
            except ImportError:
                raise ImportError(
                    "No module named expat; use SimpleXMLTreeBuilder instead"
                )
        namespace_separator = '}' if features[0] else None
        parser = expat.ParserCreate(encoding, namespace_separator)
        # underscored names are provided for compatibility only
        self.parser = self._parser = parser
        self._exception_error = expat.error
        self._names = {}  # name memo cache
        self._doctype = None
        self.entity = {}
        try:
            self.version = "Expat %d.%d.%d" % expat.version_info
        except AttributeError:
            pass  # unknown
        # let expat do the buffering, if supported
        try:
            self._parser.buffer_text = 1
        except AttributeError:
            pass

        # callbacks
        parser.DefaultHandlerExpand = self._default
        parser.XmlDeclHandler = self._decl

        # wire up the parser for event reporting
        parser = self._parser
        append = lambda x: self._events.append(
            self._StateClass(parser.CurrentByteIndex,
                             parser.CurrentLineNumber,
                             parser.CurrentColumnNumber,
                             self._depth,
                             x[0],
                             x[1])
        )
        cbase = XmlPullParser
        events = cbase.TYPES + ["start-ns", "end-ns"]
        for event in events:
            if event in ["START_DOCUMENT", "END_DOCUMENT"]:
                pass
            elif event == "START_TAG":
                try:
                    parser.ordered_attributes = 1
                    parser.specified_attributes = 1

                    def handler(tag, attrib_in, event=cbase.START_TAG, append=append,
                                targetfcn=self._start_list):
                        self._depth += 1
                        context = parser.GetInputContext().split('>', 1)[0] + '>'
                        self._isEmptyTag = context.replace(' ', '').endswith('/>')
                        append((event, (targetfcn(tag, attrib_in), self._isEmptyTag)))
                    parser.StartElementHandler = handler
                except AttributeError:
                    def handler(tag, attrib_in, event=cbase.START_TAG, append=append,
                                targetfcn=self._start):
                        self._depth += 1
                        context = parser.GetInputContext().split('>', 1)[0] + '>'
                        self._isEmptyTag = context.replace(' ', '').endswith('/>')
                        append((event, (targetfcn(tag, attrib_in), self._isEmptyTag)))
                    parser.StartElementHandler = handler
            elif event == "END_TAG":
                def handler(tag, event=cbase.END_TAG, append=append,
                            targetfcn=self._end):
                    self._depth -= 1
                    append((event, (targetfcn(tag), self._isEmptyTag)))
                    self._isEmptyTag = False

                parser.EndElementHandler = handler
            elif event == 'TEXT':
                def handler(text, event=cbase.TEXT, append=append,
                            targetfcn=self._data):
                    if self._cdsect:
                        event = cbase.CDSECT
                    # elif not self._fixtext(text).strip(' \n\t\r'):
                    #     event = cbase.IGNORABLE_WHITESPACE
                    append((event, targetfcn(text)))

                parser.CharacterDataHandler = handler
            elif event == 'CDSECT':
                def handler():
                    self._cdsect = True
                parser.StartCdataSectionHandler = handler
                def handler():
                    self._cdsect = False
                parser.EndCdataSectionHandler = handler
            elif event == 'ENTITY_REF':
                pass
            elif event == 'IGNORABLE_WHITESPACE':
                pass
            elif event == 'PROCESSING_INSTRUCTION':
                def handler(target, data, event=cbase.PROCESSING_INSTRUCTION, append=append,
                            targetfcn=self._pi):
                    append((event, targetfcn(target, data)))

                parser.ProcessingInstructionHandler = handler
            elif event == 'COMMENT':
                def handler(data, event=cbase.COMMENT, append=append,
                            targetfcn=self._data):
                    append((event, targetfcn(data)))

                parser.CommentHandler = handler
            elif event == 'DOCDECL':
                if not features[1]: continue
                def handler(doctypeName, systemId, publicId, has_internal_subset,
                            event=cbase.DOCDECL, append=append, targetfcn=self._docdecl):
                    append((event, targetfcn(doctypeName, systemId, publicId, has_internal_subset)))
                    parser.StartDoctypeDeclHandler = handler

                def handler():
                    pass

                parser.EndDoctypeDeclHandler = handler
                pass
            elif event == "start-ns":
                def handler(prefix, uri, event=event, append=append):
                    try:
                        uri = (uri or "").encode("ascii")
                    except UnicodeError:
                        pass
                    append((event, (prefix or "", uri or "")))

                parser.StartNamespaceDeclHandler = handler
            elif event == "end-ns":
                def handler(prefix, event=event, append=append):
                    append((event, prefix))

                parser.EndNamespaceDeclHandler = handler
            else:
                raise ValueError("unknown event %r" % event)

    def _raiseerror(self, value):
        err = ParseError(value)
        err.code = value.code
        err.position = value.lineno, value.offset
        raise err

    @staticmethod
    def _starttagDec(tag_in, attrib_in, context):
        tfcn = lambda x, y: (x.split('}')[0] + '}' + y) if '}' in x else y
        tag = context[1:].split(' ', 1)[0]
        prefixtag = map(lambda y: y.rsplit(' ', 1)[-1], context.split('=')[:-1])
        prefixtag = filter(lambda x: not x.startswith('xmlns'), prefixtag)
        tag = tfcn(tag_in, tag)
        key, value = zip(*attrib_in)
        key = itertools.imap(tfcn, key, prefixtag)
        return tag, zip(key, value)

    def _fixtext(self, text):
        # convert text string to ascii, if possible
        try:
            return text.encode("ascii")
        except UnicodeError:
            return text

    def _fixname(self, key):
        # expand qname, and convert name string to ascii, if possible
        try:
            name = self._names[key]
        except KeyError:
            name = key
            if "}" in name:
                name = "{" + name
            self._names[key] = name = self._fixtext(name)
        return name

    def _decl(self, version, encoding, standalone):
        self._version = version
        self._encoding = encoding
        self._standalone = standalone

    def _start(self, tag, attrib_in):
        fixname = self._fixname
        fixtext = self._fixtext
        tag = fixname(tag)
        attrib = []
        for key, value in attrib_in.items():
            attrib.append((fixname(key), fixtext(value)))
        return (tag, attrib)

    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        fixtext = self._fixtext
        tag = fixname(tag)
        attrib = []
        while attrib_in:
            key, value, attrib_in = attrib_in[0], attrib_in[1], attrib_in[2:]
            attrib.append((fixname(key), fixtext(value)))
        return (tag, attrib)

    def _data(self, text):
        return self._fixtext(text)

    def _end(self, tag):
        return self._fixname(tag)

    def _comment(self, data):
        return self._fixtext(data)

    def _pi(self, target, data):
        return (self._fixtext(target), self._fixtext(data))

    def _docdecl(self, doctypeName, systemId, publicId, has_internal_subset):
        return (doctypeName, systemId, publicId, has_internal_subset)

    def _default(self, text):
        prefix = text[:1]
        if prefix == "&":
            # deal with undefined entities
            try:
                return self.entity[text[1:-1]]
            except KeyError:
                from xml.parsers import expat
                err = expat.error(
                    "undefined entity %s: line %d, column %d" %
                    (text, self._parser.ErrorLineNumber,
                     self._parser.ErrorColumnNumber)
                )
                err.code = 11  # XML_ERROR_UNDEFINED_ENTITY
                err.lineno = self._parser.ErrorLineNumber
                err.offset = self._parser.ErrorColumnNumber
                raise err
        elif prefix == "<" and text[:9] == "<!DOCTYPE":
            self._doctype = []  # inside a doctype declaration
        elif self._doctype is not None:
            # parse doctype contents
            if prefix == ">":
                self._doctype = None
                return
            text = text.strip()
            if not text:
                return
            self._doctype.append(text)
            n = len(self._doctype)
            if n > 2:
                type = self._doctype[1]
                if type == "PUBLIC" and n == 4:
                    name, type, pubid, system = self._doctype
                elif type == "SYSTEM" and n == 3:
                    name, type, system = self._doctype
                    pubid = None
                else:
                    return
                if pubid:
                    pubid = pubid[1:-1]
                self._doctype = None
                return (name, pubid, system[1:-1])

    ##
    # Feeds data to the parser.
    #
    # @param data Encoded data.

    def feed(self, data, isEnd=0):
        try:
            self._parser.Parse(data, isEnd)
        except self._exception_error, v:
            self._raiseerror(v)

    ##
    # Finishes feeding data to the parser.
    #
    # @return An element structure.
    # @defreturn Element

    def close(self):
        self.feed('', 1)
        del self._parser  # get rid of circular references

    def next(self, isCoarse=False):
        try:
            while 1:
                try:
                    item = self._events[self._index]
                    self._index += 1
                    if item.event_type == XmlPullParser.START_TAG and self._ns > 0:
                        ndx = bisect.bisect(self._ns_index, item.depth)
                        self._ns_index.insert(ndx, item.depth)
                        self._ns_stack.insert(ndx, len(self._ns_prefix))
                        self._ns = 0
                    if item.event_type not in ["start-ns", "end-ns"]:
                        if isCoarse and item.event_type not in [
                            XmlPullParser.START_DOCUMENT,
                            XmlPullParser.START_TAG,
                            XmlPullParser.TEXT,
                            XmlPullParser.END_TAG,
                            XmlPullParser.END_DOCUMENT]:
                            continue
                        return item
                    elif item.event_type == "start-ns":
                        prefix, uri = item.event_data
                        self._ns_prefix.append(prefix)
                        self._ns_namespace.append(uri)
                        self._ns += 1
                        continue
                    elif item.event_type == "end-ns":
                        self._ns += 1
                        linf = self._ns_stack[-2]
                        if len(self._ns_prefix) - self._ns == linf:
                            self._ns_index.pop()
                            self._ns_stack.pop()
                            self._ns_prefix = self._ns_prefix[:linf]
                            self._ns_namespace = self._ns_namespace[:linf]
                            self._ns = 0
                        continue
                except IndexError:
                    pass
                if self._error:
                    e = self._error
                    self._error = None
                    raise e
                if self._parser is None:
                    self.root = self._root
                    break
                # load event buffer
                del self._events[:]
                self._index = 0
                data = self._file.read(16384)
                if data:
                    try:
                        self.feed(data)
                    except SyntaxError as exc:
                        self._error = exc
                else:
                    parser = self._parser
                    dmy = self._StateClass(parser.CurrentByteIndex,
                                           parser.CurrentLineNumber,
                                           parser.CurrentColumnNumber,
                                           self._depth,
                                           XmlPullParser.END_DOCUMENT,
                                           None)
                    self._events.append(dmy)
                    self._root = self.close()
                    self._parser = None
        except:
            if self._close_file:
                self._file.close()
            raise
        if self._close_file:
            self._file.close()
        raise StopIteration

    def __iter__(self):
        return self


class XmlPullParserImpl(XmlPullParser):

    def defineEntityReplacementText(self, entityName, replacementText):
        if self.getFeature(self.FEATURE_PROCESS_DOCDECL):
            raise Exception('IllegalStateException: "Entity replacement text may not be defined with DOCTYPE processing enabled."')
        if not hasattr(self, '_tokenizer'):
            raise Exception('IllegalStateException: "Entity replacement text must be defined after setInput()"')
        if entityName in ['amp', 'lt', 'gt', 'quot', 'apos']:
            raise Exception('XmlPullParserException: "standard XML entity can not be redefined by this method"')
        self._documentEntities[entityName] = replacementText

    def getAttributeCount(self):
        if self.getEventType() != XmlPullParser.START_TAG: return -1
        return len(self._state.event_data[0][1])

    def getAttributeName(self, index):
        nattribs = self.getAttributeCount()
        if nattribs < 0 or index < 0 or index > nattribs:
            raise Exception('IndexOutOfBoundsException')
        attribs = self._state.event_data[0][1]
        return attribs[index][0]

    def getAttributeNamespace(self, index):
        attrib = self.getAttributeName(index)
        return attrib[1:].split('}', 1)[0] if '}' in attrib else ''

    def getAttributePrefix(self, index):
        namespace = self.getAttributeNamespace(index)
        return self._getPrefix(namespace) if namespace else None

    def getAttributeType(self, index):
        return 'CDATA'

    @overload('@str', 'str')
    def getAttributeValue(self, namespace, name):
        if self.getEventType() != XmlPullParser.START_TAG:
            raise Exception('IndexOutOfBoundsException')
        is_ns_enabled = self.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
        if is_ns_enabled and namespace:
            name = '{%s}%s' % (namespace, name)
        attribs = self._state.event_data[0][1]
        iter = itertools.dropwhile(lambda x: x[0] != name, attribs)
        try:
            return iter.next()[1]
        except StopIteration:
            return None

    @getAttributeValue.adddef('int')
    def getAttributeValue(self, index):
        if self.getEventType() != XmlPullParser.START_TAG or index < 0 or index > self.getAttributeCount() - 1:
            raise Exception('IndexOutOfBoundsException')
        attribs = self._state.event_data[0][1]
        return attribs[index][1]

    def getColumnNumber(self):
        return self._state.column_number

    def getDepth(self):
        return self._state.depth

    def getEventType(self):
        return self._state.event_type

    def getFeature(self, name):
        return self._features.get(name, False) if hasattr(self, '_features') else False

    def getInputEncoding(self):
        return self._tokenizer._encoding

    def getLineNumber(self):
        return self._state.line_number

    def getName(self):
        eventType = self.getEventType()
        if eventType in [self.START_TAG, self.END_TAG]:
            tag_data = self._state.event_data[0]
            name = tag_data[0] if eventType == self.START_TAG else tag_data
            return name[1:].split('}', 1)[-1] if '}' in name else name
        if eventType == self.ENTITY_REF:
            return self._state.event_data
        return None

    def getNamespaceCount(self, depth):
        if not self.getFeature(self.FEATURE_PROCESS_NAMESPACES):
            return 0
        parser = self._tokenizer
        ndx = bisect.bisect(parser._ns_index, depth) - 1
        return parser._ns_stack[ndx] - parser._ns_stack[0]

    @overload
    def getNamespace(self):
        if self.getEventType() not in [self.START_TAG, self.END_TAG]:
            return None
        name = self.getName()
        return name[1:].split('}', 1)[0] if '}' in name else ''

    @getNamespace.adddef('@str')
    def getNamespace(self, prefix):
        prefix = prefix or 'xmlns'
        ns_prefix = self._tokenizer._ns_prefix
        ncount = ns_prefix.count(prefix)
        if not ncount:
            return None
        ns_prefix = list(reversed(ns_prefix))
        npos = len(ns_prefix) - ns_prefix.index(prefix) - 1
        return self._tokenizer._ns_namespace[npos]

    def getNamespacePrefix(self, pos):
        depth = self.getDepth()
        lsup = self.getNamespaceCount(depth)
        if pos > lsup - 1:
            raise Exception('IndexOutOfBoundsException')
        return self._tokenizer._ns_prefix[pos]

    def getNamespaceUri(self, pos):
        depth = self.getDepth()
        lsup = self.getNamespaceCount(depth)
        if pos > lsup - 1:
            raise Exception('IndexOutOfBoundsException')
        return self._tokenizer._ns_namespace[pos]

    def getPositionDescription(self):
        etype = self.getEventType()
        sb = self.TYPES[etype] if etype < len(self.TYPES) else 'Unknown'
        sb += ' '
        if etype in [self.START_TAG, self.END_TAG]:
            if self._state[-1]:
                sb += ('(empty) ')
            sb += '<'
            if etype == self.END_TAG:
                sb += '/'
            # TODO insertar lo que corresponde al namespace y prefix
            sb += self.getName()
            if etype == self.START_TAG:
                attribs = self._state.event_data[0][1]
                sb += reduce(lambda t, x: t + ' %s="%s"' % (x[0], x[1]), attribs, '')
            sb += '>'
        elif etype == self.IGNORABLE_WHITESPACE:
            pass
        elif etype != self.TEXT:
            sb += self.getText()
        elif self.isWhitespace():
            sb += '(whitespace)'
        else:
            text = self.getText()
            if len(text) > 16:
                text = text[:16] + '...'
            sb += text
        sb + '@%s:%s' % (self.getLineNumber(), self.getColumnNumber())
        # TODO agregar lo referente a la localizacion or read in
        return sb

    def getPrefix(self):
        if self.getEventType() not in [self.START_TAG, self.END_TAG]:
            return None
        namespace = self.getNamespace()
        return self._getPrefix(namespace) if namespace else None

    def _getPrefix(self, namespace):
        ns_namespace = self._tokenizer._ns_namespace
        npos = ns_namespace.index(namespace)
        return self._tokenizer.prefix[npos]

    def getProperty(self, name):
        if name == "http://xmlpull.org/v1/doc/properties.html#xmldecl-version":
            return self._tokenizer._version
        if name == "http://xmlpull.org/v1/doc/properties.html#xmldecl-standalone":
            return self._tokenizer._standalone
        if name == "http://xmlpull.org/v1/doc/properties.html#location":
            return 'location'
        return ''

    def getText(self):
        etype = self.getEventType()
        if etype == self.TEXT:
            return self._state.event_data

    def getTextCharacters(self, holderForStartAndLength):
        text = self.getText()
        if text is None:
            holderForStartAndLength[0] = -1
            holderForStartAndLength[1] = -1
            return None
        holderForStartAndLength[0] = 0
        holderForStartAndLength[1] = len(text)
        return list(text)

    def isAttributeDefault(self, index):
        return False

    def isEmptyElementTag(self):
        if self.getEventType() == self.START_TAG:
            return self._state.event_data[-1]
        raise Exception('XmlPullParserException:"The parser is not on START_TAG"')

    def isWhitespace(self):
        if self.getEventType() in [self.TEXT, self.IGNORABLE_WHITESPACE, self.CDSECT]:
            text = self._state.event_data.strip(' \n\t\r')
            return not bool(text)
        raise Exception('XmlPullParserException')

    def next(self):
        self._state = self._tokenizer.next(True)
        return self.getEventType()

    def nextTag(self):
        etype = self.next()
        if etype == self.TEXT and self.isWhitespace():
            etype = self.next()
        if etype not in [self.START_TAG, self.END_TAG]:
            raise Exception('XmlPullParserException:"expected start or end tag"')
        return etype

    def nextText(self):
        if self.getEventType() != self.START_TAG:
            raise Exception('XmlPullParserException:"parser must be on START_TAG to read next text"')
        self.next()
        etype = self.getEventType()
        if etype == self.TEXT:
            result = self.getText()
            self.next()
            if self.getEventType() != self.END_TAG:
                raise Exception('XmlPullParserException:"event TEXT it must be immediately followed by END_TAG"')
            return result
        elif etype == self.END_TAG:
            return ''
        raise Exception('XmlPullParserException: "parser must be on START_TAG or TEXT to read text"')

    def nextToken(self):
        self._state = self._tokenizer.next()

    def require(self, atype, namespace, name):
        bFlag = atype != self.getEventType() or \
                (namespace != None and not (namespace == self.getNamespace())) or \
                (name != None and not (name == self.getName()))
        if bFlag:
            errMessage = 'XmlPullParserException: "expected %s %s"'
            raise Exception(errMessage  % (self.TYPES[atype], self.getPositionDescription()))

    def setFeature(self, name, state):
        if name is None:
            raise Exception('IllegalArgumentException: "Feature name is None"')
        if name not in [self.FEATURE_PROCESS_NAMESPACES, self.FEATURE_PROCESS_DOCDECL]:
            raise Exception('XmlPullParserException:"unsupported feature: %s"' % name)
        if hasattr(self, '_parser'):
            raise Exception('XmlPullParserException:"feature: %s can be set after calling setInput"' % name)
        if not hasattr(self, '_features'):
            self._features = {}
        self._features[name] = state

    @overload('@str')
    def setInput(self, reader_in):
        if reader_in is None:
            try:
                del self._tokenizer
                del self._state
            except:
                pass
        else:
            source = StringIO.StringIO(reader_in)
            self._setInput(source, None)

    @setInput.adddef('str', '@str')
    def setInput(self, source, encoding):
        self._setInput(source, encoding)

    def _setInput(self, source, encoding):
        features = [self.getFeature(self.FEATURE_PROCESS_NAMESPACES),
                    self.getFeature(self.FEATURE_PROCESS_DOCDECL)]
        self._tokenizer = TokenIterator(source, encoding, features)
        self._state = None
        self._documentEntities = {}
        self.nextToken()

    def setProperty(self, name, value):
        if name == "http://xmlpull.org/v1/doc/properties.html#location":
            self.location = value
        else:
            raise Exception('XmlPullParserException:"unsupported property: %s"' % name)

    @property
    def _state(self):
        try:
            return self._tokenizer_state
        except:
            raise Exception('XmlPullParserException: "Parser source not define, please call setInput first')

    @_state.setter
    def _state(self, value):
        self._tokenizer_state = value

    @_state.deleter
    def _state(self):
        del self._tokenizer_state

    @property
    def _tokenizer(self):
        try:
            return self._token_iterator
        except:
            raise Exception('XmlPullParserException: "Parser source not define, please call setInput first')

    @_tokenizer.setter
    def _tokenizer(self, value):
        self._token_iterator = value

    @_tokenizer.deleter
    def _tokenizer(self):
        del self._token_iterator