# -*- coding: utf-8 -*-

# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestAttributes.java
# /**
#  * Test attribute uniqueness is ensured.
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from UtilTestCase import *
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory


class TestAttributes:

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
        assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    @classmethod
    def teardown_class(cls):
        pass

    def test_attribs(self):
        factory = self.factory
        XML_ATTRS = \
            "<event xmlns:xsi='http://www.w3.org/1999/XMLSchema/instance' encodingStyle=\"test\">" + \
            "<type>my-event</type>" + \
            "<handback xsi:type='ns2:string' xmlns:ns2='http://www.w3.org/1999/XMLSchema' xsi:None='1'/>" + \
            "</event>"

        pp = factory.newPullParser()
        pp.setInput(XML_ATTRS)

        assertEquals(XmlPullParser.START_TAG, pp.next())
        assertEquals("event", pp.getName())
        assertEquals(XmlPullParser.START_TAG, pp.next())
        assertEquals("type", pp.getName())
        assertEquals(XmlPullParser.TEXT, pp.next())
        assertEquals("my-event", pp.getText())
        assertEquals(pp.next(), XmlPullParser.END_TAG)
        assertEquals("type", pp.getName())
        assertEquals(XmlPullParser.START_TAG, pp.next())
        assertEquals("handback", pp.getName())
        # //assertEquals(XmlPullParser.CONTENT, pp.next())
        # //assertEquals("", pp.readContent())

        xsiNone = pp.getAttributeValue(
            "http://www.w3.org/1999/XMLSchema/instance", "None")
        assertEquals("1", xsiNone)

        xsiType = pp.getAttributeValue(
            "http://www.w3.org/1999/XMLSchema/instance", "type")
        assertEquals("ns2:string", xsiType)


        typeName = self.getQNameLocal(xsiType)
        assertEquals("string", typeName)
        typeNS = self.getQNameUri(pp, xsiType)
        assertEquals("http://www.w3.org/1999/XMLSchema", typeNS)

        assertEquals(pp.next(), XmlPullParser.END_TAG)
        assertEquals("handback", pp.getName())
        assertEquals(pp.next(), XmlPullParser.END_TAG)
        assertEquals("event", pp.getName())

        assertEquals(pp.next(), XmlPullParser.END_DOCUMENT)

    @staticmethod
    def getQNameLocal(qname):
        if qname == None: return None
        pos = qname.find(':')
        return qname[pos + 1:]

    @staticmethod
    def getQNameUri(pp, qname):
        if qname == None: return None
        pos = qname.find(':')
        if pos == -1:
            raise Exception('XmlPullParserException:"qname des not have prefix"')
        prefix = qname[0:pos]
        return pp.getNamespace(prefix)

    def test_attribuniq(self):
        attribsOk = \
            "<m:test xmlns:m='Some-Namespace-URI' xmlns:n='Some-Namespace-URI'" + \
            " a='a' b='b' m:a='c' n:b='d' n:x='e'" + \
            "/>\n" + \
            ""

        duplicateAttribs = \
            "<m:test xmlns:m='Some-Namespace-URI' xmlns:n='Some-Namespace-URI'" + \
            " a='a' b='b' m:a='a' n:b='b' a='x'" + \
            "/>\n" + \
            ""

        duplicateNsAttribs = \
            "<m:test xmlns:m='Some-Namespace-URI' xmlns:n='Some-Namespace-URI'" + \
            " a='a' b='b' m:a='a' n:b='b' n:a='a'" + \
            "/>\n" + \
            ""

        duplicateXmlns = \
            "<m:test xmlns:m='Some-Namespace-URI' xmlns:m='Some-Namespace-URI'" + \
            "" + \
            "/>\n" + \
            ""

        duplicateAttribXmlnsDefault = \
            "<m:test xmlns='Some-Namespace-URI' xmlns:m='Some-Namespace-URI'" + \
            " a='a' b='b' m:b='b' m:a='x'" + \
            "/>\n" + \
            ""
        factory = self.factory
        pp = self.parseOneElement(factory, attribsOk, False)
        assertEquals("a", pp.getAttributeValue(None, "a"))
        assertEquals("b", pp.getAttributeValue(None, "b"))
        assertEquals("c", pp.getAttributeValue(None, "m:a"))
        assertEquals("d", pp.getAttributeValue(None, "n:b"))
        assertEquals("e", pp.getAttributeValue(None, "n:x"))

        pp = self.parseOneElement(factory, attribsOk, True)

        assertEquals("a", pp.getAttributeValue("","a"))
        assertEquals("b", pp.getAttributeValue("","b"))
        assertEquals(None, pp.getAttributeValue("", "m:a"))
        assertEquals(None, pp.getAttributeValue("", "n:b"))
        assertEquals(None, pp.getAttributeValue("", "n:x"))

        assertEquals("c", pp.getAttributeValue("Some-Namespace-URI", "a"))
        assertEquals("d", pp.getAttributeValue("Some-Namespace-URI", "b"))
        assertEquals("e", pp.getAttributeValue("Some-Namespace-URI", "x"))

        self.parseOneElement(factory, duplicateNsAttribs, False)
        self.parseOneElement(factory, duplicateAttribXmlnsDefault, False)
        self.parseOneElement(factory, duplicateAttribXmlnsDefault, True)

        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, duplicateAttribs, True)
        
        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, duplicateAttribs, False)

        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, duplicateXmlns, False)
        
        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, duplicateXmlns, True)

        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, duplicateNsAttribs, True)

        declaringEmptyNs  = \
            "<m:test xmlns:m='' />"

        # allowed when namespaces disabled
        pp = self.parseOneElement(factory, declaringEmptyNs, False)

        # otherwise it is error to declare '' for non-default NS as described in
        #   http://www.w3.org/TR/1999/REC-xml-names-19990114/#ns-decl

        with pytest.raises(Exception):
            pp = self.parseOneElement(factory, declaringEmptyNs, True)

    @staticmethod
    def parseOneElement(factory, buf, supportNamespaces):
        factory.setNamespaceAware(supportNamespaces)
        pp = factory.newPullParser()
        pp.setInput(buf)
        pp.next()
        if supportNamespaces:
            assertEquals("test", pp.getName())
        else:
            assertEquals("m:test", pp.getName())
        return pp