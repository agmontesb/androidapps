# -*- coding: utf-8 -*-
import StringIO
import collections
import itertools
import bisect
import re
from collections import namedtuple

from Android import overload
from XmlPullParser import XmlPullParser


class ParseError(SyntaxError):
    pass


class XmlPullParserImpl(XmlPullParser):
    class TokenIterator(object):

        _StateClass = namedtuple(
            '_StateClass', 'byte_index, line_number, column_number, depth, event_type, event_data'
        )

        def __init__(self,):
            super(XmlPullParserImpl.TokenIterator, self).__init__()
            self._init_events()

        def _setInput(self, source, encoding=None, features=None):
            self._init_events()
            self.features = features or [False, False, False]
            close_source = False
            if not hasattr(source, "read"):
                source = open(source, "rb")
                close_source = True

            # fields
            self._file = source
            self._close_file = close_source
            self._version = None
            self._encoding = None
            self._standalone = None

            # temporal states
            self._depth = 0
            self._isEmptyTag = ''  # Usado para distinguir <a .... /> de <a ..></a>
            self._cdsect = False

            # manejo namespace
            self._ns = 0
            self._ns_index = [0]
            self._ns_stack = [0]
            self._ns_prefix = []
            self._ns_namespace = []
            self._init_parser_(encoding)

        def _init_events(self):
            self._close_file = False
            self._parser = None
            self._error = None
            self.root = self._root = None
            self._events = []
            self._index = 0
            self._text = None
            dmy = self._StateClass(0, 1, 0, 0, XmlPullParser.START_DOCUMENT, None)
            self._events.append(dmy)

        def _init_parser_(self, encoding):
            features = self.features
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
            self.doctype_parser = None
            self._exception_error = expat.error
            self._names = {}  # name memo cache
            self._textbuffer = ''
            self._doctype = None
            self.entity = {'quot': '"', 'amp': '&', 'apos': "'", 'lt': '<', 'gt': '>'}
            try:
                self.version = "Expat %d.%d.%d" % expat.version_info
            except AttributeError:
                pass  # unknown
            # let expat do the buffering, if supported
            append = lambda x, y=self: y._events.append(
                self._StateClass(y.parser.CurrentByteIndex,
                                 y.parser.CurrentLineNumber,
                                 y.parser.CurrentColumnNumber,
                                 y._depth,
                                 x[0],
                                 x[1])
            )
            cbase = XmlPullParser
            try:
                self._parser.buffer_text = 0
            except AttributeError:
                pass
            parser.UseForeignDTD(True)
            parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)

            # callbacks
            parser.DefaultHandler = self._default
            parser.DefaultHandlerExpand = self._default
            parser.XmlDeclHandler = self._decl

            def handler(entityName, is_parameter_entity, event=cbase.ENTITY_REF, append=append,
                        targetfcn=self._skipped_entity):
                try:
                    value = self.entity[entityName]
                    append((event, targetfcn(entityName, value)))
                except KeyError:
                    from xml.parsers import expat
                    err = expat.error(
                        "undefined entity %s: line %d, column %d" %
                        (entityName, self._parser.ErrorLineNumber,
                         self._parser.ErrorColumnNumber)
                    )
                    err.code = 11  # XML_ERROR_UNDEFINED_ENTITY
                    err.lineno = self._parser.ErrorLineNumber
                    err.offset = self._parser.ErrorColumnNumber
                    raise err

            parser.SkippedEntityHandler = handler
            parser.NotStandaloneHandler = lambda: 1

            # wire up the parser for event reporting
            events = cbase.TYPES + ["start-ns", "end-ns"]
            for event in events:
                if event in ["START_DOCUMENT", "END_DOCUMENT"]:
                    pass
                elif event == "START_TAG":
                    try:
                        parser.ordered_attributes = 1
                        parser.specified_attributes = 1
                        targetfcn = self._start_list
                    except:
                        targetfcn = self._start

                    def startTagDecorator(targetfcn):
                        def wrapper(*args, **kwargs):
                            answ = targetfcn(*args)
                            self._depth += 1
                            context = parser.GetInputContext()[1:].split('>', 1)[0].rstrip('> \n\r\t')
                            _isEmptyTag = context.endswith('/')
                            tag, context = (context.rstrip('/') + ' ').split(' ', 1)
                            self._isEmptyTag = tag if _isEmptyTag else ''
                            if features[0]:
                                tfcn = lambda x, y: (x.split('}')[0] + '}' + y) if '}' in x else y
                                tag_in, attrib_in = answ
                                tag_in = tfcn(tag_in, tag)
                                if attrib_in:
                                    reducefcn = lambda t, x: t.extend(x.split(' ')) or t
                                    prefixtag = reduce(reducefcn, context.strip().split('='), [])
                                    it = []
                                    m = 0
                                    for k in range(0,len(prefixtag),2):
                                        key, value = prefixtag[k], prefixtag[k + 1].strip('"\'')
                                        if not key.startswith('xmlns'):
                                            key = tfcn(attrib_in[m][0], key)
                                            value = attrib_in[m][1]
                                            m += 1
                                        elif not features[2]:
                                            continue
                                        it.append((key, value))
                                    attrib_in = it
                                    # attrib_in = self._start_list(tagin)
                                    # it = list(itertools.izip(*(2*[iter(prefixtag)])))
                                    # if not features[2]:
                                    #     it = map(lambda)
                                    # prefixtag = map(lambda y: y.rsplit(' ', 1)[-1], context.split('=')[:-1])
                                    #
                                    # prefixtag = filter(lambda x: not x.startswith('xmlns'), prefixtag)
                                    # key, value = zip(*attrib_in)
                                    # key = itertools.imap(tfcn, key, prefixtag)
                                    # attrib_in = zip(key, value)
                                answ = (tag_in, attrib_in)
                            append((cbase.START_TAG, (answ, bool(self._isEmptyTag))))

                        return wrapper

                    parser.StartElementHandler = startTagDecorator(targetfcn)
                elif event == "END_TAG":
                    def endTagDecorator(targetfcn):
                        def wrapper(*args, **kwargs):
                            tag_in = targetfcn(*args)
                            if features[0] and '}' in tag_in:
                                if self._isEmptyTag:
                                    tag = self._isEmptyTag
                                else:
                                    context = parser.GetInputContext().split('>', 1)[0] + '>'
                                    tag = context.strip('</> \n\r\t')
                                tfcn = lambda x, y: (x.split('}')[0] + '}' + y)
                                tag_in = tfcn(tag_in, tag)
                            self._depth -= 1
                            append((cbase.END_TAG, (tag_in, bool(self._isEmptyTag))))
                            self._isEmptyTag = ''

                        return wrapper

                    parser.EndElementHandler = endTagDecorator(self._end)
                elif event == 'TEXT':
                    def handler(text, event=cbase.TEXT, append=append,
                                targetfcn=self._data):
                        if self._cdsect:
                            event = cbase.CDSECT
                            append((event, targetfcn(text)))
                        else:
                            context = parser.GetInputContext()
                            if context.startswith('&'):
                                event = cbase.ENTITY_REF
                                key = context[1:].split(';', 1)[0]
                                targetfcn = self._skipped_entity
                                append((event, targetfcn(key, text)))
                            else:
                                if not text.strip(' \n\t\r'):
                                    event = cbase.IGNORABLE_WHITESPACE
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
                                targetfcn=self._data):
                        data = '%s %s' % (target, data)
                        append((event, targetfcn(data)))

                    parser.ProcessingInstructionHandler = handler
                elif event == 'COMMENT':
                    def handler(data, event=cbase.COMMENT, append=append,
                                targetfcn=self._data):
                        append((event, targetfcn(data)))

                    parser.CommentHandler = handler
                elif event == 'DOCDECL':
                    if not features[1]: continue
                    doctype_parser = parser
                    # doctype_parser = expat.ParserCreate(encoding, None)
                    doctype_parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_ALWAYS)

                    # Aca se deben redefinir los handlers para implementar el validador
                    def handler(doctypeName, systemId, publicId, has_internal_subset):
                        text = '<!DOCTYPE %s' % doctypeName
                        if systemId:
                            text += ' SYSTEM "%s"' % systemId
                        if publicId:
                            text += ' PUBLIC "%s"' % publicId
                        if has_internal_subset:
                            context = self._parser.GetInputContext()
                            internal_subset = context[1:].split(']', 1)[0]
                            text += ' [%s]' % internal_subset
                        text += '>'
                        self._textbuffer = text

                    doctype_parser.StartDoctypeDeclHandler = handler

                    def handler(*args):
                        data = self._textbuffer[9:-1]
                        self._textbuffer = None
                        parser.CommentHandler(data, event=XmlPullParser.DOCDECL)

                    doctype_parser.EndDoctypeDeclHandler = handler

                    def handler(*args):
                        pass

                    doctype_parser.EntityDeclHandler = handler
                    doctype_parser.ElementDeclHandler = handler
                    doctype_parser.AttlistDeclHandler = handler
                    doctype_parser.NotationDeclHandler = handler
                    pass
                elif event == "start-ns":
                    def handler(prefix, uri, event=event, append=append):
                        try:
                            uri = (uri or "").encode("ascii")
                        except UnicodeError:
                            pass
                        append((event, (prefix or "xmlns", uri or "")))

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

        def _skipped_entity(self, target, data):
            return (self._fixtext(target), self._fixtext(data))

        def _docdecl(self, doctypeName, systemId, publicId, has_internal_subset):
            return (doctypeName, systemId, publicId, has_internal_subset)

        def _default(self, text):
            prefix = text[:1]
            if prefix == "<" and text[:9] == "<!DOCTYPE":
                pattern = r'(<!DOCTYPE[^\[]+(\[[^\]]+\])*\s*>)'
                context = self._parser.GetInputContext()
                self._textbuffer = re.search(pattern, context).group()
                self._doctype = text
            elif self._doctype is not None:
                self._doctype += text
                if self._doctype == self._textbuffer:
                    data = self._doctype
                    if self.doctype_parser:
                        try:
                            self.doctype_parser.Parse(data, 0)
                        except self._exception_error, v:
                            self._raiseerror(v)
                    data = data[10:-1]
                    self._parser.CommentHandler(data, event=XmlPullParser.DOCDECL)
                    self._textbuffer = ''
                    self._doctype = None
            elif prefix == "&":
                # deal with undefined entities
                try:
                    key = text[1:-1]
                    if key.startswith('#x'):
                        value = chr(int(key, 16))
                    elif key.startswith('#'):
                        value = chr(int(key))
                    else:
                        value = self.entity[key]
                    return self._parser.CharacterDataHandler(text + ' ' + value, event=XmlPullParser.ENTITY_REF)
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
            elif not self._textbuffer:
                self._parser.CommentHandler(text, event=XmlPullParser.IGNORABLE_WHITESPACE)

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
                while True:
                    try:
                        nextEvent = self._peekEvents()
                        if self._text and nextEvent and nextEvent not in [XmlPullParser.TEXT, XmlPullParser.ENTITY_REF]:
                            item, self._text = self._text, None
                            return item
                        item = self._events[self._index]
                        self._index += 1
                        if item.event_type == XmlPullParser.START_TAG and self._ns > 0:
                            ndx = bisect.bisect(self._ns_index, item.depth)
                            self._ns_index.insert(ndx, item.depth)
                            self._ns_stack.insert(ndx, len(self._ns_prefix))
                            self._ns = 0
                        if item.event_type not in ["start-ns", "end-ns"]:
                            if not isCoarse:
                                return item
                            if item.event_type not in [
                                XmlPullParser.START_DOCUMENT,
                                XmlPullParser.START_TAG,
                                XmlPullParser.TEXT,
                                XmlPullParser.ENTITY_REF,
                                XmlPullParser.END_TAG,
                                XmlPullParser.END_DOCUMENT]:
                                continue
                            if item.event_type == XmlPullParser.ENTITY_REF:
                                texto = item.event_data[1]
                                item = item._replace(event_type=XmlPullParser.TEXT, event_data=texto)
                            if item.event_type == XmlPullParser.TEXT:
                                if self._text:
                                    texto = self._text.event_data + item.event_data
                                    self._text = self._text._replace(event_data=texto)
                                else:
                                    self._text = item
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

        def _peekEvents(self):
            index = self._index
            if index < len(self._events):
                return self._events[index].event_type

    def __init__(self):
        super(XmlPullParserImpl, self).__init__()
        self.setInput(None)

    def defineEntityReplacementText(self, entityName, replacementText):
        if self.getFeature(self.FEATURE_PROCESS_DOCDECL):
            raise Exception('IllegalStateException: "Entity replacement text may not be defined with DOCTYPE processing enabled."')
        if not hasattr(self, '_tokenizer'):
            raise Exception('IllegalStateException: "Entity replacement text must be defined after setInput()"')
        if entityName in ['amp', 'lt', 'gt', 'quot', 'apos']:
            raise Exception('XmlPullParserException: "standard XML entity can not be redefined by this method"')
        self._tokenizer.entity[entityName] = replacementText

    def getAttributeCount(self):
        if self.getEventType() != XmlPullParser.START_TAG: return -1
        return len(self._state.event_data[0][1])

    def getAttributeName(self, index):
        data = self._getRawAttribute(index)
        return data[-1]

    def getAttributeNamespace(self, index):
        data = self._getRawAttribute(index)
        return data[0][1:-1]

    def getAttributePrefix(self, index):
        data = self._getRawAttribute(index)
        return data[1]

    def getAttributeType(self, index):
        return 'CDATA'

    @overload('@str', 'str')
    def getAttributeValue(self, namespace, name):
        if self.getEventType() != XmlPullParser.START_TAG:
            raise Exception('IndexOutOfBoundsException')
        if namespace: name= '{%s}%s' % (namespace, name)
        attribs = self._state.event_data[0][1]
        bflag = self.getFeature(self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES)
        tfcn = lambda x: '{0}{2}'.format(*self._decomposeRawData(x[0], bflag)) != name
        iter = itertools.dropwhile(tfcn, attribs)
        try:
            return iter.next()[1]
        except StopIteration:
            return None

    @getAttributeValue.adddef('int')
    def getAttributeValue(self, index):
        nattribs = self.getAttributeCount()
        if nattribs < 0 or index < 0 or index > nattribs:
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
        data = self._getRawTag(eventType)
        if data:
            return data[-1]
        if eventType == self.ENTITY_REF:
            return self._state.event_data[0]
        return None

    def getNamespaceCount(self, depth):
        lsup = self.getDepth() + (1 if self.getEventType() == self.END_TAG else 0)
        if depth > lsup:
            raise Exception('XmlPullParserException: "Out of bound exception"')
        if not self.getFeature(self.FEATURE_PROCESS_NAMESPACES):
            return 0
        parser = self._tokenizer
        ndx = bisect.bisect(parser._ns_index, depth) - 1
        lsup = parser._ns_stack[ndx]
        return lsup - parser._ns_prefix[:lsup].count('xmlns')

    @overload
    def getNamespace(self):
        eventType = self.getEventType()
        data = self._getRawTag(eventType)
        return data[0][1:-1] if data else None

    @getNamespace.adddef('@str')
    def getNamespace(self, prefix):
        namespaceMap = collections.OrderedDict(xmlns='http://www.w3.org/2000/xmlns',
                                               xml='http://www.w3.org/XML/1998/namespace'
                                               )
        parser = self._tokenizer
        depth = self.getDepth()
        ndx = bisect.bisect(parser._ns_index, depth) - 1
        lsup = parser._ns_stack[ndx]
        namespaceMap.update(zip(parser._ns_prefix[:lsup], parser._ns_namespace[:lsup]))
        return namespaceMap.get(prefix, None)

    def getNamespacePrefix(self, pos):
        depth = self.getDepth()
        if self.getEventType() == self.END_TAG: depth += 1
        lsup = self.getNamespaceCount(depth)
        if pos > lsup - 1:
            raise Exception('IndexOutOfBoundsException')
        pos += self._tokenizer._ns_prefix[:pos+1].count('xmlns')
        while self._tokenizer._ns_prefix[pos] == 'xmlns':
            pos += 1
        return self._tokenizer._ns_prefix[pos]

    def getNamespaceUri(self, pos):
        depth = self.getDepth()
        if self.getEventType() == self.END_TAG: depth += 1
        lsup = self.getNamespaceCount(depth)
        if pos > lsup - 1:
            raise Exception('IndexOutOfBoundsException')
        pos += self._tokenizer._ns_prefix[:pos+1].count('xmlns')
        while self._tokenizer._ns_prefix[pos] == 'xmlns':
            pos += 1
        return self._tokenizer._ns_namespace[pos]

    def getPositionDescription(self):
        etype = self.getEventType()
        sb = self.TYPES[etype] if etype < len(self.TYPES) else 'Unknown'
        sb += ' '
        if etype in [self.START_TAG, self.END_TAG]:
            if self.isEmptyElementTag():
                sb += ('(empty) ')
            sb += '<'
            if etype == self.END_TAG:
                sb += '/'
            prefix = self.getPrefix()
            if prefix:
                sb += '{%s}%s:' % (self.getNamespace(), prefix)
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
        eventType = self.getEventType()
        data = self._getRawTag(eventType)
        return data[1] if data else None

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
        if etype in [self.TEXT, self.IGNORABLE_WHITESPACE, self.DOCDECL,
                     self.COMMENT, self.PROCESSING_INSTRUCTION, self.CDSECT]:
            return self._state.event_data
        if etype == self.ENTITY_REF:
            return self._state.event_data[1]

    def getTextCharacters(self, holderForStartAndLength):
        if self.getEventType() == self.ENTITY_REF and not self.getFeature(self.FEATURE_PROCESS_DOCDECL):
            text = self._state.event_data[0]
        else:
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
        if name not in [self.FEATURE_PROCESS_NAMESPACES,
                        self.FEATURE_PROCESS_DOCDECL,
                        self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES]:
            raise Exception('XmlPullParserException:"unsupported feature: %s"' % name)
        if hasattr(self, '_parser'):
            raise Exception('XmlPullParserException:"feature: %s can be set after calling setInput"' % name)
        if not hasattr(self, '_features'):
            self._features = {}
        self._features[name] = state

    @overload('@str')
    def setInput(self, reader_in):
        if reader_in is None:
            self._state = None
            self._tokenizer = XmlPullParserImpl.TokenIterator()
            self.nextToken()
        else:
            source = StringIO.StringIO(reader_in)
            self._setInput(source, None)

    @setInput.adddef('str', '@str')
    def setInput(self, source, encoding):
        self._setInput(source, encoding)

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

    @staticmethod
    def _decomposeRawData(data, hasNamespaceAttributes):
        if '}' not in data:
            if hasNamespaceAttributes and data.startswith('xmlns:'):
                data = ('{http://www.w3.org/2000/xmlns/}',) + tuple(data.split(':'))
            else:
                data = ('', None, data)
        else:
            namespace, data = data.split('}')
            namespace += '}'
            try:
                prefix, name = data.split(':')
                data = (namespace, prefix, name)
            except:
                data = (namespace, None, data)
        return data

    def _getRawTag(self, eventType):
        if eventType not in [self.START_TAG, self.END_TAG]:
            return None
        data = self._state.event_data[0]
        if eventType == self.START_TAG: data = data[0]
        bflag = self.getFeature(self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES)
        return self._decomposeRawData(data, bflag)

    def _getRawAttribute(self, index):
        nattribs = self.getAttributeCount()
        if nattribs < 0 or index < 0 or index > nattribs:
            raise Exception('IndexOutOfBoundsException')
        attribs = self._state.event_data[0][1]
        attrib = attribs[index][0]
        bflag = self.getFeature(self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES)
        return self._decomposeRawData(attrib, bflag)

    def _setInput(self, source, encoding):
        features = [self.getFeature(self.FEATURE_PROCESS_NAMESPACES),
                    self.getFeature(self.FEATURE_PROCESS_DOCDECL),
                    self.getFeature(self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES)]
        self._tokenizer._setInput(source, encoding, features)
        self.nextToken()

