# -*- coding: utf-8 -*-
import StringIO
import abc
from Android import Object, overload
from XmlTokenIterator import XmlTokenIterator


class XmlPullParserValidator(Object):
    __metaclass__ = abc.ABCMeta

    XML_CQUANT_NONE = 0
    XML_CQUANT_OPT = 1
    XML_CQUANT_PLUS = 3
    XML_CQUANT_REP = 2
    XML_CTYPE_ANY = 2
    XML_CTYPE_CHOICE = 5
    XML_CTYPE_EMPTY = 1
    XML_CTYPE_MIXED = 3
    XML_CTYPE_NAME = 4
    XML_CTYPE_SEQ = 6

    @abc.abstractmethod
    def start_tag(self, tag):
        pass

    @abc.abstractmethod
    def end_tag(self, tag):
        pass

    class Factory(Object):

        def _ParserImpl(self, *args, **kwargs):
            class ValidatorImpl(XmlPullParserValidator):

                def __init__(self):
                    self.stack = None
                    self.elements = None

                def reportError(self, tag, errMessage, endtag):
                    raise Exception(errMessage)

                def start_tag(self, tag, attribs):
                    # TODO agregar la logica para validar los atributos
                    if not self.elements.get(tag):
                        errMessage = 'ValidatorError: Element type "%s" must be declared.' % tag
                        return self.reportError(tag, errMessage, endtag=False)
                    while True:
                        ptype, pquant, pname, pndx, pchildren = self.stack[-1]
                        if ptype == self.XML_CTYPE_EMPTY:
                            errMessage = 'ValidatorError: The content of element type "%s" must match "EMPTY"' % pname
                            return self.reportError(tag, errMessage, endtag=False)
                        if ptype == self.XML_CTYPE_ANY and self.elements.get(tag):
                            break
                        else:
                            try:
                                ctype = pchildren[pndx][0]
                            except IndexError:
                                errMessage = 'ValidatorError: All tags for "%s" has been processed' % pname
                                return self.reportError(tag, errMessage, endtag=False)
                            if ctype in [self.XML_CTYPE_SEQ, self.XML_CTYPE_CHOICE]:
                                ctype, cquant, cname, children = pchildren[pndx]
                                self.stack.append((ctype, cquant, cname, 0, children))
                            else:
                                answ, pndx = self.checkStartTag(ptype, pchildren, pndx, tag)
                                if answ == -1:
                                    ptype, pquant, pname, pndx, pchildren = self.popStack(False)
                                    if ptype == self.XML_CTYPE_SEQ or pndx == len(pchildren):
                                        errMessage = 'ValidatorError: Tag "%s" not in sequence or a valid ' \
                                                     'option for "%s"' % (tag, pname)
                                        return self.reportError(tag, errMessage, endtag=False)
                                self.stack[-1] = (ptype, pquant, pname, pndx, pchildren)
                                if answ != -1:
                                    break
                    self.stack.append(self.elements[tag])
                    pass

                def checkStartTag(self, ptype, pchildren, pndx, tag):
                    while pndx < len(pchildren):
                        ctype, cquant, cname, children = pchildren[pndx]
                        if cname == tag:
                            if cquant in [self.XML_CQUANT_NONE, self.XML_CQUANT_OPT]:
                                answ = 1
                            elif cquant == self.XML_CQUANT_REP:  # '*'
                                answ = 2
                            elif cquant == self.XML_CQUANT_PLUS:  # '+'
                                answ = 3
                            pndx = pndx if ptype != self.XML_CTYPE_MIXED else 0
                            return answ, pndx
                        if cquant == self.XML_CQUANT_PLUS:
                            return -1, pndx
                        if ptype == self.XML_CTYPE_SEQ and cquant == self.XML_CQUANT_NONE:
                            return -1, pndx
                        pndx += 1
                    return -1, pndx

                def end_tag(self, tag):
                    ptype, pquant, pname, pndx, pchildren = self.stack.pop()
                    if pname != tag:
                        errMessage = 'ValidatorError: Expecting end tag for "%s" instead ' \
                                     'receive end tag for "%s"' % (pname, tag)
                        return self.reportError(tag, errMessage, endtag=True)
                    if ptype != self.XML_CTYPE_MIXED and pchildren[pndx:] and not all(
                            map(lambda x: x[1] in (self.XML_CQUANT_OPT, self.XML_CQUANT_REP), pchildren[pndx:])):
                        tags = ', '.join(map(lambda x: x[2], pchildren[pndx:]))
                        errMessage = 'ValidatorError: Tag "%s" requires "%s" tag(s)' % (pname, tags)
                        return self.reportError(tag, errMessage, endtag=True)
                    self.stack[-1] = self.popStack(True)

                def popStack(self, isSuccess):
                    while True:
                        ptype, pquant, pname, pndx, pchildren = self.stack[-1]
                        if ptype == self.XML_CTYPE_ANY:
                            break
                        if ptype == self.XML_CTYPE_MIXED:
                            pndx = 0 if isSuccess else len(pchildren)
                        elif ptype == self.XML_CTYPE_CHOICE:
                            pndx = len(pchildren) if isSuccess else (pndx + 1)
                        elif not isSuccess:
                            pndx = len(pchildren)
                        elif ptype == self.XML_CTYPE_SEQ:
                            if pndx < len(pchildren) and pchildren[pndx][1] in [self.XML_CQUANT_NONE,
                                                                                self.XML_CQUANT_OPT]:
                                pndx += 1
                        if pname or (not pname and pndx < len(pchildren)):
                            break
                        self.stack.pop()
                    return ptype, pquant, pname, pndx, pchildren

                def isCtypeMixed(self):
                    return self.stack[-1][0] == self.XML_CTYPE_MIXED
            return ValidatorImpl(*args, **kwargs)

        def __init__(self, root=None):
            super(XmlPullParserValidator.Factory, self).__init__()
            self._elements = {}
            self.entity = {}
            if root:
                self.setRoot(root)

        @classmethod
        def createFromString(cls, doctypestr, encoding=None):
            from xml.parsers import expat
            doctype_parser = expat.ParserCreate(encoding, None)
            doctype_parser.ordered_attributes = True
            doctype_parser.UseForeignDTD(True)
            doctype_parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_ALWAYS)
            doctype_parser.buffer_text = 1
            bd = cls()

            def handler(entityName, is_parameter_entity, value, base, systemId, publicId, notationName, builder=bd):
                if not is_parameter_entity:
                    builder.entity[entityName] = value
                pass
            doctype_parser.EntityDeclHandler = handler

            def start_doctype(doctypeName, systemId, publicId, has_internal_subset, builder=bd):
                builder.setRoot(doctypeName)
                pass
            doctype_parser.StartDoctypeDeclHandler = start_doctype

            def end_doctype(builder=bd):
                pass
            doctype_parser.EndDoctypeDeclHandler = end_doctype

            def element(name, model, builder=bd):
                builder.setElement(name, model)
            doctype_parser.ElementDeclHandler = element

            # doctype_parser.AttlistDeclHandler = handler
            # doctype_parser.NotationDeclHandler = handler

            try:
                doctype_parser.Parse(doctypestr, 0)
            except expat.error, value:
                err = SyntaxError(value)
                err.code = value.code
                err.position = value.lineno, value.offset
                raise err
            return bd

        def setRoot(self, root):
            self.root = root
            return self

        def setElement(self, entityname, value):
            ptype, pquant, pname, pchildren = value
            ndx = 0
            self._elements[entityname] = (ptype, pquant, entityname, ndx, pchildren)
            return self

        def newParserValidator(self):
            validator = self._ParserImpl()
            validator.stack = [(6, 0, 'root', 0, ((4, 0, self.root, ()),))]
            validator.elements = self._elements
            validator.entity = self.entity
            return validator

        def newXmlValidator(self, docDeclStr=None):
            class EvaluatorBuilder(XmlPullParserValidator.Factory):
                def __init__(self):
                    super(EvaluatorBuilder, self).__init__()
                    pass

                def _ParserImpl(self, *args, **kwargs):
                    anInst = super(EvaluatorBuilder, self)._ParserImpl(*args, **kwargs)

                    def reportError(tag, errMessage, endtag):
                        if not endtag:
                            anInst.stack.append(
                                anInst.elements.get(tag, (XmlPullParserValidator.XML_CTYPE_ANY, 0, tag, 0, ()))
                            )
                        return errMessage

                    anInst.reportError = reportError
                    return anInst

            class XmlValidator(XmlTokenIterator):
                def __init__(self, docDeclStr=None):
                    super(XmlValidator, self).__init__()
                    self.features = [False, False, False, True]
                    self.validator = None
                    self._depth = 0
                    self._init_parser_(None)
                    if docDeclStr:
                        self.setValidator(docDeclStr)
                    pass

                def _setParserCallbacks(self):
                    # callbacks
                    self._parser.XmlDeclHandler = self._decl
                    if self.validator:
                        self.setValidator()

                @overload('XmlPullParserValidator')
                def setValidator(self, validator):
                    if not (validator or isinstance(validator, XmlPullParserValidator)):
                        raise AttributeError('validator must be an instance of XmlPullParserValidator')
                    self.validator = validator
                    parser = self._parser

                    def validatorDecorator(valfunc, taginc):
                        def handler(*args, **kwargs):
                            self._depth = self._depth + taginc
                            errMessage = valfunc(*args)
                            if errMessage:
                                lineno = self.CurrentLineNumber()
                                columnno = self.CurrentColumnNumber()
                                errMessage = errMessage.replace('ValidatorError:',
                                                                'ValidatorError (%s, %s):' % (lineno, columnno))
                                self._appendEvent(256, errMessage)
                        return handler

                    parser.StartElementHandler = validatorDecorator(self.validator.start_tag, 1)
                    parser.EndElementHandler = validatorDecorator(self.validator.end_tag, -1)

                    def handler(*args, **kwargs):
                        pass
                    parser.CommentHandler = handler

                @setValidator.adddef('str')
                def setValidator(self, docDeclStr):
                    self._processDocDecl(docDeclStr, None)
                    pass

                def setRoot(self, root):
                    if len(self.validator.stack) > 1:
                        raise Exception('DocDecl root can only be set after processing data')
                    self.validator.stack = [(6, 0, 'root', 0, ((4, 0, root, ()),))]

                def getRoot(self):
                    if self.validator:
                        pchildren = self.validator.stack[0][4]
                        return pchildren[0][2]

                def setInput(self, xmlStr, validator=None):
                    validator = validator or self.validator
                    source = StringIO.StringIO(xmlStr)
                    self._setInput(source, features=[False, False, False, True])
                    if validator:
                        self.setValidator(validator)
                    else:
                        self._loadData()
                    self.next()

                def _processDocDecl(self, data, encoding):
                    builder = EvaluatorBuilder.createFromString(data, encoding)
                    self.setValidator(builder.newParserValidator())

            return XmlValidator(docDeclStr)



