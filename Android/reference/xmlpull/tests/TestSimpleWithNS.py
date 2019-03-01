# -*- coding: utf-8 -*-
# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestSimpleWithNs.java
# /**
#  * Simple test ot verify pull parser factory
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import StringIO
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestSimpleWithNS:
    factory = None

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assertEquals(True, factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))

    @classmethod
    def teardown_class(cls):
        pass

    def testSimpleWithNs(self):
        factory = self.factory
        xpp = factory.newPullParser()
        assertEquals(True, xpp.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))

        # check setInput semantics
        with pytest.raises(Exception):
            xpp.getEventType()
        with pytest.raises(Exception):
            xpp.next()
        xpp.setInput(None)
        with pytest.raises(Exception):
            xpp.getEventType()
        with pytest.raises(Exception):
            xpp.next()

        # check the simplest possible XML document - just one root element
        for i in range(2):
            xmlStr = "<foo/>" if i == 1 else "<foo></foo>"
            xpp.setInput(xmlStr)
            assertEquals(1, xpp.getLineNumber())
            assertEquals(0, xpp.getColumnNumber())
            empty = (i == 1)
            checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)
            xpp.next()
            checkParserStateNs(xpp, 1, xpp.START_TAG, None, 0, "", "foo", None, empty, 0)
            xpp.next()
            checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "", "foo", None, False, -1)
            xpp.next()
            checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)

        # one step further - it has content ...
        xmlStr = "<foo attrName='attrVal'>bar</foo>"
        xpp.setInput(xmlStr)
        checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.START_TAG, None, 0, "", "foo", None, False, 1)
        checkAttribNs(xpp, 0, None, "", "attrName", "attrVal")
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.TEXT, None, 0, None, None, "bar", False, -1)
        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "", "foo", None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)

        xmlStr = \
        "<foo xmlns='n' xmlns:ns1='n1' xmlns:ns2='n2'>" + \
        "<ns1:bar xmlns:ns1='x1' xmlns:ns3='n3' xmlns='n1'>" + \
        "<ns2:gugu a1='v1' ns2:a2='v2' xml:lang='en' ns1:a3=\"v3\"/>" + \
        "<baz xmlns:ns1='y1'></baz>" + \
        "</ns1:bar></foo>"
        xpp.setInput(xmlStr)
        checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)

        xpp.next()
        checkParserStateNs(xpp, 1, xpp.START_TAG, None, 2, "n", "foo", None, False, 0)
        assertEquals(0, xpp.getNamespaceCount(0))
        assertEquals(2, xpp.getNamespaceCount(1))
        checkNamespace(xpp, 0, "ns1", "n1", True)
        checkNamespace(xpp, 1, "ns2", "n2", True)

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.START_TAG, "ns1", 4, "x1", "bar", None, False, 0)
        assertEquals(0, xpp.getNamespaceCount(0))
        assertEquals(2, xpp.getNamespaceCount(1))
        assertEquals(4, xpp.getNamespaceCount(2))
        checkNamespace(xpp, 2, "ns1", "x1", True)
        checkNamespace(xpp, 3, "ns3", "n3", True)

        xpp.next()
        checkParserStateNs(xpp, 3, xpp.START_TAG, "ns2", 4, "n2", "gugu", None, True, 4)
        assertEquals(4, xpp.getNamespaceCount(2))
        assertEquals(4, xpp.getNamespaceCount(3))
        assertEquals("x1", xpp.getNamespace("ns1"))
        assertEquals("n2", xpp.getNamespace("ns2"))
        assertEquals("n3", xpp.getNamespace("ns3"))
        checkAttribNs(xpp, 0, None, "", "a1", "v1")
        checkAttribNs(xpp, 1, "ns2", "n2", "a2", "v2")
        checkAttribNs(xpp, 2, "xml", "http://www.w3.org/XML/1998/namespace", "lang", "en")
        checkAttribNs(xpp, 3, "ns1", "x1", "a3", "v3")

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.END_TAG, "ns2", 4, "n2", "gugu", None, False, -1)

        xpp.next()
        checkParserStateNs(xpp, 3, xpp.START_TAG, None, 5, "n1", "baz", None, False, 0)
        assertEquals(0, xpp.getNamespaceCount(0))
        assertEquals(2, xpp.getNamespaceCount(1))
        assertEquals(4, xpp.getNamespaceCount(2))
        assertEquals(5, xpp.getNamespaceCount(3))
        checkNamespace(xpp, 4, "ns1", "y1", True)
        assertEquals("y1", xpp.getNamespace("ns1"))
        assertEquals("n2", xpp.getNamespace("ns2"))
        assertEquals("n3", xpp.getNamespace("ns3"))

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.END_TAG, None, 4, "n1", "baz", None, False, -1)
        assertEquals("x1", xpp.getNamespace("ns1"))
        assertEquals("n2", xpp.getNamespace("ns2"))
        assertEquals("n3", xpp.getNamespace("ns3"))

        xpp.next()
        checkParserStateNs(xpp, 1, xpp.END_TAG, "ns1", 2, "x1", "bar", None, False, -1)
        assertEquals("n1", xpp.getNamespace("ns1"))
        assertEquals("n2", xpp.getNamespace("ns2"))
        assertEquals(None, xpp.getNamespace("ns3"))

        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "n", "foo", None, False, -1)

        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)
        assertEquals(None, xpp.getNamespace("ns1"))
        assertEquals(None, xpp.getNamespace("ns2"))
        assertEquals(None, xpp.getNamespace("ns3"))