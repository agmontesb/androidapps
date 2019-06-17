# -*- coding: utf-8 -*-
import StringIO
import collections
import itertools
import bisect
import re
from collections import namedtuple

from Android import overload
from XmlPullParser import XmlPullParser
from XmlTokenIterator import XmlTokenIterator


class XmlPullParserImpl(XmlPullParser):

    def __init__(self, tokenIterator=None):
        super(XmlPullParserImpl, self).__init__()
        # self.setInput(None)
        self._validator = None
        self.setTokenIterator(tokenIterator)

    def setTokenIterator(self, tokenIterator):
        self._state = None
        self._tokenizer = tokenIterator or XmlTokenIterator()
        self.nextToken()

    def defineEntityReplacementText(self, entityName, replacementText):
        if any(map(self.getFeature, (self.FEATURE_PROCESS_DOCDECL, self.FEATURE_VALIDATION))):
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

    def next(self, isCoarse=False):
        self._state = self._tokenizer.next(isCoarse)
        return self.getEventType()

    def nextTag(self):
        etype = self.next(True)
        if etype == self.TEXT and self.isWhitespace():
            etype = self.next(True)
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
                        self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES,
                        self.FEATURE_VALIDATION]:
            raise Exception('XmlPullParserException:"unsupported feature: %s"' % name)
        if hasattr(self, '_parser'):
            raise Exception('XmlPullParserException:"feature: %s can be set after calling setInput"' % name)
        if not hasattr(self, '_features'):
            self._features = {}
        self._features[name] = state

    @overload('@str')
    def setInput(self, reader_in):
        if reader_in is None:
            self.setTokenIterator(None)
            # self._state = None
            # self._tokenizer = XmlPullParserImpl.TokenIterator()
            # self.nextToken()
        else:
            source = StringIO.StringIO(reader_in)
            self._setInput(source, None)

    @setInput.adddef('str', '@str')
    def setInput(self, source, encoding):
        self._setInput(source, encoding, None)

    @setInput.adddef('str', '@str', '@XmlPullParserValidator')
    def setInput(self, source, encoding, validator):
        source = StringIO.StringIO(source)
        self._setInput(source, encoding, validator)

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

    def _setInput(self, source, encoding, validator=None):
        features = [self.getFeature(self.FEATURE_PROCESS_NAMESPACES),
                    self.getFeature(self.FEATURE_PROCESS_DOCDECL),
                    self.getFeature(self.FEATURE_REPORT_NAMESPACE_ATTRIBUTES),
                    self.getFeature(self.FEATURE_VALIDATION) or bool(validator)]
        self._tokenizer._setInput(source, encoding, features)
        if validator:
            self._tokenizer.setValidator(validator)
        self.nextToken()

