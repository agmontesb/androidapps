# -*- coding: utf-8 -*-
# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestSimple.java
# /**
#  * Simple test ot verify pull parser factory
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestSimple:
    factory = None

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        assertEquals(False, factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))
        assertEquals(False, factory.getFeature(XmlPullParser.FEATURE_VALIDATION))

    @classmethod
    def teardown_class(cls):
        pass

    def test_Simple(self):
        xpp = self.factory.newPullParser()
        assertEquals(False, xpp.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))

        # this SHOULD always be OK
        assertEquals("START_DOCUMENT", xpp.TYPES[xpp.START_DOCUMENT])
        assertEquals("END_DOCUMENT", xpp.TYPES[xpp.END_DOCUMENT])
        assertEquals("START_TAG", xpp.TYPES[xpp.START_TAG])
        assertEquals("END_TAG", xpp.TYPES[xpp.END_TAG])
        assertEquals("TEXT", xpp.TYPES[xpp.TEXT])
        assertEquals("CDSECT", xpp.TYPES[xpp.CDSECT])
        assertEquals("ENTITY_REF", xpp.TYPES[xpp.ENTITY_REF])
        assertEquals("IGNORABLE_WHITESPACE", xpp.TYPES[xpp.IGNORABLE_WHITESPACE])
        assertEquals("PROCESSING_INSTRUCTION", xpp.TYPES[xpp.PROCESSING_INSTRUCTION])
        assertEquals("COMMENT", xpp.TYPES[xpp.COMMENT])
        assertEquals("DOCDECL", xpp.TYPES[xpp.DOCDECL])

        # check setInput semantics
        assertEquals(XmlPullParser.START_DOCUMENT, xpp.getEventType())
        with pytest.raises(Exception, message="exception was expected of next() if no input was set on parser"):
            xpp.next()
        xpp.setInput(None)
        assertEquals(XmlPullParser.START_DOCUMENT, xpp.getEventType())
        with pytest.raises(Exception, message="exception was expected of next() if no input was set on parser"):
            xpp.next()
        assertEquals(1, xpp.getLineNumber())
        assertEquals(0, xpp.getColumnNumber())

        # check the simplest possible XML document - just one root element
        for i in range(2):
            xmlStr = "<foo/>" if i == 1 else "<foo></foo>"
            xpp.setInput(xmlStr)
            assertEquals(1, xpp.getLineNumber())
            assertEquals(0, xpp.getColumnNumber())
            empty = (i == 1)
            checkParserState(xpp, 0, xpp.START_DOCUMENT, None, None, False, -1)
            xpp.next()
            checkParserState(xpp, 1, xpp.START_TAG, "foo", None, empty, 0)
            xpp.next()
            checkParserState(xpp, 0, xpp.END_TAG, "foo", None, False, -1)
            xpp.next()
            checkParserState(xpp, 0, xpp.END_DOCUMENT, None, None, False, -1)

        # one step further - it has content ...
        xmlStr = "<foo attrName='attrVal'>bar<p:t>\r\n\t </p:t></foo>"
        xpp.setInput(xmlStr)
        checkParserState(xpp, 0, xpp.START_DOCUMENT, None, None, False, -1)
        xpp.next()
        checkParserState(xpp, 1, xpp.START_TAG, "foo", None, False, 1)
        checkAttrib(xpp, 0, "attrName", "attrVal")
        xpp.next()
        checkParserState(xpp, 1, xpp.TEXT, None, "bar", False, -1)
        assertEquals(False, xpp.isWhitespace())
        xpp.next()
        checkParserState(xpp, 2, xpp.START_TAG, "p:t", None, False, 0)
        # xpp.next()
        # checkParserState(xpp, 2, xpp.TEXT, None, "\n\t ", False, -1)
        # assert xpp.isWhitespace()
        xpp.next()
        checkParserState(xpp, 1, xpp.END_TAG, "p:t", None, False, -1)
        xpp.next()
        checkParserState(xpp, 0, xpp.END_TAG, "foo", None, False, -1)
        xpp.next()
        checkParserState(xpp, 0, xpp.END_DOCUMENT, None, None, False, -1)
