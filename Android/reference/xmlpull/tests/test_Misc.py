# -*- coding: utf-8 -*-

# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestMisc.java
# /**
#  * Tests checking miscellaneous features.
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */

import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestMisc:
    factory = None

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assertEquals(True, factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))

    @classmethod
    def teardown_class(cls):
        pass


    def testReadText(self):
        factory = self.factory
        INPUT_XML = "<test>foo</test>"
        pp = factory.newPullParser()
        pp.setInput(INPUT_XML)
        # assertEquals( "", pp.readText() )
        pp.next()
        # assertEquals( "", pp.readText() )
        pp.next()
        pp.next()
        # assertEquals( "foo", pp.readText() )
        assertEquals( pp.TYPES[ pp.END_TAG ], pp.TYPES[ pp.getEventType() ])

    def testRequire(self):
        # public void require (int type, namespace, name)
        factory = self.factory
        INPUT_XML = "<test><t>foo</t><m:s xmlns:m='URI'>\t</m:s></test>"
        pp = factory.newPullParser()
        pp.setInput(INPUT_XML)
        pp.require( pp.START_DOCUMENT, None, None)
        pp.next()
        pp.require( pp.START_TAG, None, "test")
        pp.require( pp.START_TAG, "", None)
        pp.require( pp.START_TAG, "", "test")
        pp.next()
        pp.require( pp.START_TAG, "", "t")
        pp.next()
        pp.require( pp.TEXT, None, None)
        pp.next()
        pp.require( pp.END_TAG, "", "t")

        pp.next()
        pp.require( pp.START_TAG, "URI", "s")

        pp.next()
        #  this call will skip white spaces
        pp.require( pp.END_TAG, "URI", "s")

        pp.next()
        pp.require( pp.END_TAG, "", "test")
        pp.next()
        pp.require( pp.END_DOCUMENT, None, None)

    def testReportNamespaceAttributes(self):
        factory = self.factory
        pp = factory.newPullParser()
        assertEquals(True, pp.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES))

        try:
            pp.setFeature(XmlPullParser.FEATURE_REPORT_NAMESPACE_ATTRIBUTES, True)
        except Exception as ex:
            #  skip rest of test if parser does nto support reporting
            return
    
        #  see XML Namespaces spec for namespace URIs for 'xml' and 'xmlns'
        #    xml is bound to http://www.w3.org/XML/1998/namespace
        #    "(...) The prefix xmlns is used only for namespace bindings
        #      and is not itself bound to any namespace name. (...)
        #  however it is typically bound to "http://www.w3.org/2000/xmlns/"
        #    in some contexts such as DOM
        #  http://www.w3.org/TR/REC-xml-names/#ns-using
        XML_MISC_ATTR = \
            "<test xmlns='Some-Namespace-URI' xmlns:n='Some-Other-URI'" + \
            " a='a' b='b' xmlns:m='Another-URI' m:a='c' n:b='d' n:x='e' xml:lang='en'" + \
            "/>\n" + \
            ""
        pp.setInput(XML_MISC_ATTR)
        pp.next()
        # pp.readStartTag(stag)
        assertEquals("test", pp.getName())
        assertEquals("Some-Namespace-URI", pp.getNamespace())

        assertEquals("a", pp.getAttributeValue("","a"))
        assertEquals("b", pp.getAttributeValue("","b"))
        assertEquals(None, pp.getAttributeValue("", "m:a"))
        assertEquals(None, pp.getAttributeValue("", "n:b"))
        assertEquals(None, pp.getAttributeValue("", "n:x"))

        assertEquals("c", pp.getAttributeValue("Another-URI", "a"))
        assertEquals("d", pp.getAttributeValue("Some-Other-URI", "b"))
        assertEquals("e", pp.getAttributeValue("Some-Other-URI", "x"))
        assertEquals("en", pp.getAttributeValue("http://www.w3.org/XML/1998/namespace", "lang"))


        checkAttribNs(pp, 0, None, "", "xmlns", "Some-Namespace-URI")
        checkAttribNs(pp, 1, "xmlns", "http://www.w3.org/2000/xmlns/","n","Some-Other-URI")
        checkAttribNs(pp, 2, None, "", "a", "a")
        checkAttribNs(pp, 3, None, "", "b", "b")
        checkAttribNs(pp, 4, "xmlns", "http://www.w3.org/2000/xmlns/","m","Another-URI")
        checkAttribNs(pp, 5, "m", "Another-URI","a","c")
        checkAttribNs(pp, 6, "n", "Some-Other-URI","b","d")
        checkAttribNs(pp, 7, "n", "Some-Other-URI","x","e")
        checkAttribNs(pp, 8, "xml", "http://www.w3.org/XML/1998/namespace", "lang", "en")
