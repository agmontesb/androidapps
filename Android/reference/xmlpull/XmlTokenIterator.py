# -*- coding: utf-8 -*-
import bisect
import re
from collections import namedtuple

from Android.reference.xmlpull.XmlPullParser import XmlPullParser


class ParseError(SyntaxError):
    pass


class XmlTokenIterator(object):
    _StateClass = namedtuple(
        '_StateClass', 'byte_index, line_number, column_number, depth, event_type, event_data'
    )

    def __init__(self, ):
        super(XmlTokenIterator, self).__init__()
        self._init_events()

    def _setInput(self, source, encoding=None, features=None):
        self._init_events()
        self.features = features or [False, False, False, False]
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
        self.validator = None

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
        self._setParserCallbacks()

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
        self.validator = None
        self.doctype_parser = None
        self._lineoffset = 0
        self._coloffset = 0
        self._byteoffset = 0
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
        parser.returns_unicode = False
        parser.buffer_text = 0
        parser.UseForeignDTD(True)
        parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)

    def _setParserCallbacks(self):
        features = self.features
        parser = self._parser
        append = self._appendEvent
        cbase = XmlPullParser

        # callbacks
        def handler(text):
            return self._parser.CharacterDataHandler(text)

        parser.DefaultHandler = handler
        parser.DefaultHandlerExpand = handler
        parser.XmlDeclHandler = self._decl

        def handler(entityName, is_parameter_entity, event=cbase.ENTITY_REF, append=append,
                    targetfcn=self._skipped_entity, owner=self):
            try:
                entityMap = owner.validator.entity if owner.validator else owner.entity
                value = entityMap[entityName]
                append(event, targetfcn(entityName, value))
            except KeyError:
                from xml.parsers import expat
                err = expat.error(
                    "undefined entity %s: line %d, column %d" %
                    (entityName, self._parser.ErrorLineNumber,
                     self._parser.ErrorColumnNumber)
                )
                err.code = 11  # XML_ERROR_UNDEFINED_ENTITY
                err.lineno = self._parser.ErrorLineNumber
                err.columnno = self._parser.ErrorColumnNumber
                self._raiseerror(err)

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
                                contextStr = '"' + context.strip()
                                reducefcn = lambda t, x: t.extend(x.rpartition(x[0])[0:3:2]) or t
                                prefixtag = reduce(reducefcn, contextStr.split('='), [])[1:-1]
                                it = []
                                m = 0
                                for k in range(0, len(prefixtag), 2):
                                    key, value = prefixtag[k].strip(' \n\r\t'), prefixtag[k + 1].strip(' \n\r\t"\'')
                                    if not key.startswith('xmlns'):
                                        key = tfcn(attrib_in[m][0], key)
                                        value = attrib_in[m][1]
                                        m += 1
                                    elif not features[2]:
                                        continue
                                    it.append((key, value))
                                attrib_in = it
                            answ = (tag_in, attrib_in)
                        append(cbase.START_TAG, (answ, bool(self._isEmptyTag)))

                    return wrapper

                handler = startTagDecorator(targetfcn)
                parser.StartElementHandler = handler
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
                        append(cbase.END_TAG, (tag_in, bool(self._isEmptyTag)))
                        self._isEmptyTag = ''

                    return wrapper

                handler = endTagDecorator(self._end)
                parser.EndElementHandler = handler

            elif event == 'TEXT':
                def handler(text, event=cbase.TEXT, append=append,
                            targetfcn=self._data):
                    if self._cdsect:
                        event = cbase.CDSECT
                        append(event, targetfcn(text))
                    else:
                        context = parser.GetInputContext()
                        if context.startswith('&') and event == cbase.TEXT:
                            event = cbase.ENTITY_REF
                            key = context[1:].split(';', 1)[0]
                            targetfcn = self._skipped_entity
                            append(event, targetfcn(key, text))
                        else:
                            if not text.strip(' \n\t\r'):
                                event = cbase.IGNORABLE_WHITESPACE
                                if len(text) == 1:
                                    if context[:2] == '\r\n':
                                        text = context[:2]
                                    else:
                                        text = context[0]
                                else:
                                    text = re.match(r'[ \n\t\r]+', context).group()
                            append(event, targetfcn(text))

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
                    append(event, targetfcn(data))

                parser.ProcessingInstructionHandler = handler
            elif event == 'COMMENT':
                def handler(data, event=cbase.COMMENT, append=append,
                            targetfcn=self._data):
                    append(event, targetfcn(data))

                parser.CommentHandler = handler
            elif event == 'DOCDECL':
                pass
            elif event == "start-ns":
                def handler(prefix, uri, event=event, append=append):
                    try:
                        uri = (uri or "").encode("ascii")
                    except UnicodeError:
                        pass
                    append(event, (prefix or "xmlns", uri or ""))

                parser.StartNamespaceDeclHandler = handler
            elif event == "end-ns":
                def handler(prefix, event=event, append=append):
                    append(event, prefix)

                parser.EndNamespaceDeclHandler = handler
            else:
                raise ValueError("unknown event %r" % event)

    def _appendEvent(self, event_type, event_data):
        if event_type in [XmlPullParser.IGNORABLE_WHITESPACE, XmlPullParser.TEXT] and \
                self._events and \
                self._events[-1].event_type == event_type and \
                self._events[-1].depth == self._depth:
            event_data = self._events[-1].event_data + event_data
            self._events[-1] = self._events[-1]._replace(event_data=event_data)
        else:
            self._events.append(
                self._StateClass(self.CurrentByteIndex(),
                                 self.CurrentLineNumber(),
                                 self.CurrentColumnNumber(),
                                 self._depth,
                                 event_type,
                                 event_data)
            )

    def CurrentByteIndex(self):
        return self.parser.CurrentByteIndex + self._byteoffset

    def CurrentLineNumber(self):
        return self.parser.CurrentLineNumber + self._lineoffset

    def CurrentColumnNumber(self):
        answ = self.parser.CurrentColumnNumber
        if self.CurrentLineNumber() == self._lineoffset:
            answ += self._coloffset
        return answ

    def _raiseerror(self, value):
        err = ParseError(value)
        err.code = value.code
        lineno = value.lineno + self._lineoffset
        columnno = value.columnno
        if lineno == self._lineoffset:
            columnno += self._coloffset
        err.position = (lineno, columnno)
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
        if prefix == "&":
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
                err.columnno = self._parser.ErrorColumnNumber
                self._raiseerror(err)
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

    def setValidator(self, validator):
        from Android.reference.xmlpull.XmlPullParserValidator import XmlPullParserValidator
        if not isinstance(validator, XmlPullParserValidator):
            raise AttributeError('validator must be an instance of XmlPullParserValidator')
        self.validator = validator
        if self.features[3]:
            parser = self._parser

            def validatorDecorator(func, valfunc):
                def wrapper(*args, **kwargs):
                    try:
                        valfunc(*args)
                    except Exception as exc:
                        exc.code = 256
                        exc.lineno, exc.columnno = parser.CurrentLineNumber, parser.CurrentColumnNumber
                        self._raiseerror(exc)
                    return func(*args, **kwargs)

                return wrapper

            handler = validatorDecorator(parser.StartElementHandler, self.validator.start_tag)
            parser.StartElementHandler = handler

            handler = validatorDecorator(parser.EndElementHandler, self.validator.end_tag)
            parser.EndElementHandler = handler

            def validatorDecorator(func, validator=self.validator):
                def wrapper(text, **kwargs):
                    event = XmlPullParser.TEXT
                    if not validator.isCtypeMixed():
                        event = XmlPullParser.IGNORABLE_WHITESPACE
                    return func(text, event=event)

                return wrapper

            handler = validatorDecorator(parser.CharacterDataHandler)
            parser.CharacterDataHandler = handler

    def next(self, isCoarse=False):
        try:
            while True:
                try:
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
                        baseindx = 0 if item.depth and not self.features[3] else 1
                        # baseindx = 1
                        coarseEvents = [
                                           XmlPullParser.IGNORABLE_WHITESPACE,
                                           XmlPullParser.START_DOCUMENT,
                                           XmlPullParser.START_TAG,
                                           XmlPullParser.TEXT,
                                           XmlPullParser.ENTITY_REF,
                                           XmlPullParser.END_TAG,
                                           XmlPullParser.END_DOCUMENT][baseindx:]
                        if item.event_type not in coarseEvents:
                            continue
                        case = item.event_type
                        if case in [XmlPullParser.IGNORABLE_WHITESPACE, XmlPullParser.ENTITY_REF]:
                            texto = item.event_data
                            if case == XmlPullParser.ENTITY_REF:
                                texto = texto[1]
                            item = item._replace(event_type=XmlPullParser.TEXT, event_data=texto)
                        if item.event_type == XmlPullParser.TEXT:
                            if self._text:
                                texto = self._text.event_data + item.event_data
                                self._text = self._text._replace(event_data=texto)
                            else:
                                self._text = item
                            nextEvent = self._peekEvents()
                            bFlag = nextEvent in [XmlPullParser.START_TAG,
                                                  XmlPullParser.END_TAG,
                                                  XmlPullParser.END_DOCUMENT,
                                                  'start-ns']
                            if not bFlag: continue
                            item, self._text = self._text, None
                            texto = item.event_data
                            texto = texto.replace('\r\n', '\n').replace('\r', '\n')
                            item = item._replace(event_data=texto)
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
                self._loadData()
        except:
            if self._close_file:
                self._file.close()
            raise
        if self._close_file:
            self._file.close()
        raise StopIteration

    def _loadData(self):
        data = self._file.read(16384)
        if data:
            pattern = r'(<!DOCTYPE[^\[]+(?:\[[^\]]+\])*\s*>)'
            data = re.split(pattern, data)
            try:
                self.feed(data[0])
                if len(data) == 3:
                    if self.features[3] or self.features[1]:
                        self._processDocDecl(data[1], self._encoding)
                    self._parser.CommentHandler(data[1][9:-1], event=XmlPullParser.DOCDECL)
                    norm_docdecl = data[1]
                    self._lineoffset = norm_docdecl.count('\n')
                    self._coloffset = (len(norm_docdecl) - 1 - norm_docdecl.rfind('\n'))
                    self._byteoffset = len(data[1])
                    self.feed(data[2])
                elif len(data) > 3:
                    err = SyntaxError(
                        'Syntax error: More than one <!DOCTYPE> found'
                    )
                    raise err
                if self.features[3] and not self.validator:
                    err = SyntaxError(
                        'Syntax error: A validating Iterator is required but no validator has been defined'
                    )
                    raise err
            except SyntaxError as exc:
                self._error = exc
        else:
            parser = self._parser
            dmy = self._StateClass(self.CurrentByteIndex(),
                                   self.CurrentLineNumber(),
                                   self.CurrentColumnNumber(),
                                   self._depth,
                                   XmlPullParser.END_DOCUMENT,
                                   None)
            self._events.append(dmy)
            self._root = self.close()
            self._parser = None

    def _processDocDecl(self, data, encoding, **kwargs):
        from Android.reference.xmlpull.XmlPullParserValidator import XmlPullParserValidator
        Builder = XmlPullParserValidator.Factory
        builder = Builder.createFromString(data, encoding)
        self.setValidator(builder.newParserValidator())

    def __iter__(self):
        return self

    def _peekEvents(self):
        index = self._index
        if index < len(self._events):
            return self._events[index].event_type
