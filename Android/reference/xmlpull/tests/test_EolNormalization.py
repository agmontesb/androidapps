# -*- coding: utf-8 -*-
# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestEolNormalization.java
# /**
#  * Test end-of-line normalization
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestEolNormalization:

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
        assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    @classmethod
    def teardown_class(cls):
        pass

    def testNormalizeLine(self):
        factory = self.factory

        # -----------------------
        #  ---- simple tests for end of line normalization

        simpleR = "-\n-\r-\r\n-\n\r-"

        #  element content EOL normalizaton

        tagSimpleR = "<test>"+simpleR+"</test>"

        expectedSimpleN = "-\n-\n-\n-\n\n-"

        pp = self.parseOneElement(factory, tagSimpleR, True)
        assertEquals(XmlPullParser.TEXT, pp.next())
        assertEquals(printable(expectedSimpleN), printable(pp.getText()))

        #  attribute content normalization

        attrSimpleR = "<test a=\""+simpleR+"\"/>"

        normalizedSimpleN = "- - - -  -"

        pp = self.parseOneElement(factory, attrSimpleR, True)
        attrVal = pp.getAttributeValue("","a")

        # TODO Xerces2
        assertEquals(printable(normalizedSimpleN), printable(attrVal))

        # -----------------------
        #  --- more complex example with more line engins together

        firstR = \
            "\r \r\n \n\r \n\n \r\n\r \r\r \r\n\n \n\r\r\n\r" + ""

        #  element content

        tagR = \
            "<m:test xmlns:m='Some-Namespace-URI'>" + \
            firstR + \
            "</m:test>\r\n"

        expectedN = \
            "\n \n \n\n \n\n \n\n \n\n \n\n \n\n\n\n"

        pp = self.parseOneElement(factory, tagR, True)
        assertEquals(XmlPullParser.TEXT, pp.next())
        assertEquals(printable(expectedN), printable(pp.getText()))

        #  attribute value

        attrR = "<m:test xmlns:m='Some-Namespace-URI' fifi='" + firstR+"'/>"

        normalizedN = "                       "

        pp = self.parseOneElement(factory, attrR, True)
        attrVal = pp.getAttributeValue("","fifi")
        # System.err.println("attrNormalized.len="+normalizedN.length())
        # System.err.println("attrVal.len="+attrVal.length())

        # TODO Xerces2
        assertEquals(printable(normalizedN), printable(attrVal))


        # -----------------------
        #  --- even more complex

        manyLineBreaks = "fifi\r&amp;\r&amp;\r\n foo &amp;\r bar \n\r\n&quot;" + firstR

        manyTag = \
            "<m:test xmlns:m='Some-Namespace-URI'>" + \
            manyLineBreaks + \
            "</m:test>\r\n"

        manyExpected = \
            "fifi\n&\n&\n foo &\n bar \n\n\"" + \
            expectedN
        # "\r \r\n \n\r \n\n \r\n\r \r\r \r\n\n \n\r\r\n\r"

        pp = self.parseOneElement(factory, manyTag, True)
        assertEquals(XmlPullParser.TEXT, pp.next())
        assertEquals(manyExpected, pp.getText())

        assertEquals(pp.next(), XmlPullParser.END_TAG)
        assertEquals("test", pp.getName())

        #  having \r\n as last characters is the hardest case
        # assertEquals(XmlPullParser.CONTENT, pp.next())
        # assertEquals("\n", pp.readContent())
        assertEquals(pp.next(), XmlPullParser.END_DOCUMENT)


        manyAttr = "<m:test xmlns:m='Some-Namespace-URI' fifi='"+manyLineBreaks+"'/>"

        manyNormalized = "fifi & &  foo &  bar   \""+ normalizedN

        pp = self.parseOneElement(factory, manyAttr, True)
        attrVal = pp.getAttributeValue("","fifi")
        # TODO Xerces2
        assertEquals(printable(manyNormalized), printable(attrVal))

    def parseOneElement(self, factory, buf, supportNamespaces):
        factory.setNamespaceAware(supportNamespaces)
        pp = factory.newPullParser()
        pp.setInput(buf)
        pp.next()
        if supportNamespaces:
            assertEquals("test", pp.getName())
        else:
            assertEquals("m:test", pp.getName())
        return pp
