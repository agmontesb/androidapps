# -*- coding: utf-8 -*-

# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestSimpleToken.java
# /**
#  * Simple test for minimal XML tokenizing
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestSimpleToken:
    factory = None

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setFeature(XmlPullParser.FEATURE_PROCESS_DOCDECL, True)
        assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_DOCDECL)
        assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    @classmethod
    def teardown_class(cls):
        pass


    def testSimpleToken(self):
        factory = self.factory
        xpp = factory.newPullParser()
        assertEquals(True, xpp.getFeature(XmlPullParser.FEATURE_PROCESS_DOCDECL))

        # check setInput semantics
        assertEquals(XmlPullParser.START_DOCUMENT, xpp.getEventType())
        with pytest.raises(Exception, message="exception was expected of nextToken() if no input was set on parser"):
            xpp.nextToken()

        xpp.setInput(None)
        assertEquals(XmlPullParser.START_DOCUMENT, xpp.getEventType())
        with pytest.raises(Exception, message="exception was expected of next() if no input was set on parser"):
            xpp.nextToken()

        xpp.setInput(None) # reset parser
        FEATURE_XML_ROUNDTRIP="http://xmlpull.org/v1/doc/features.html#xml-roundtrip"
        # attempt to set roundtrip
        try:
            xpp.setFeature(FEATURE_XML_ROUNDTRIP, True)
        except Exception as ex:
            pass
        # did we succeeded?
        roundtripSupported = xpp.getFeature(FEATURE_XML_ROUNDTRIP)


        # check the simplest possible XML document - just one root element
        for i in range(2):
            xmlStr = "<foo/>" if i == 1 else "<foo></foo>"
            xpp.setInput(xmlStr)
            empty = (i == 1)
            checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)
            xpp.nextToken()
            checkParserStateNs(xpp, 1, xpp.START_TAG, None, 0, "", "foo", None, empty, 0)
            if roundtripSupported:
                if empty:
                    #              System.out.println("tag='" + \xpp.getText()+"'")
                    #              foo ="<foo/>"
                    #              foo2 = xpp.getText()
                    #              System.out.println(foo.equals(foo2))
                    assertEquals("empty tag roundtrip",
                                 printable("<foo/>"),
                                 printable(xpp.getText()))
                else:
                    assertEquals("start tag roundtrip",
                                 printable("<foo>"),
                                 printable(xpp.getText()))
            xpp.nextToken()
            checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "", "foo", None, False, -1)
            if roundtripSupported:
                if empty:
                    assertEquals("empty tag roundtrip",
                                 printable("<foo/>"),
                                 printable(xpp.getText()))
                else:
                    assertEquals("end tag roundtrip",
                                 printable("</foo>"),
                                 printable(xpp.getText()))
            xpp.nextToken()
            checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)


        # one step further - it has content ...

        MISC_XML = \
            "\n \r\n \n\r<!DOCTYPE titlepage SYSTEM \"http://www.foo.bar/dtds/typo.dtd\" " + \
            "[<!ENTITY % active.links \"INCLUDE\">" + \
            "  <!ENTITY   test \"This is test! Do NOT Panic!\" >" + \
            "]>" + \
            "<!--c-->  \r\n<foo attrName='attrVal'>bar<!--comment-->" + \
            "&test;&lt;&#32;" + \
            "<?pi ds?><![CDATA[ vo<o ]]></foo> \r\n"
        xpp.setInput(MISC_XML)
        checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.IGNORABLE_WHITESPACE, None, 0, None, None,
                           "\n \r\n \n\r", False, -1)
        assert xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.DOCDECL, None, 0, None, None,
                           " titlepage SYSTEM \"http://www.foo.bar/dtds/typo.dtd\" " + \
                               "[<!ENTITY % active.links \"INCLUDE\">" + \
                               "  <!ENTITY   test \"This is test! Do NOT Panic!\" >]", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.COMMENT, None, 0, None, None, "c", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.IGNORABLE_WHITESPACE, None, 0, None, None, "  \r\n", False, -1)
        assert xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.START_TAG, None, 0, "", "foo", None, False, 1)
        if roundtripSupported:
            assertEquals("start tag roundtrip", "<foo attrName='attrVal'>", xpp.getText())

        checkAttribNs(xpp, 0, None, "", "attrName", "attrVal")
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.TEXT, None, 0, None, None, "bar", False, -1)
        assertEquals(False, xpp.isWhitespace())

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.COMMENT, None, 0, None, None, "comment", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs( xpp, 1, xpp.ENTITY_REF, None, 0, None, "test", "This is test! Do NOT Panic!", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.ENTITY_REF, None, 0, None, "lt", "<", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.ENTITY_REF, None, 0, None, "#32", " ", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.PROCESSING_INSTRUCTION, None, 0, None, None, "pi ds", False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 1, xpp.CDSECT, None, 0, None, None, " vo<o ", False, -1)
        assertEquals(False, xpp.isWhitespace())

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "", "foo", None, False, -1)
        if roundtripSupported:
            assertEquals("end tag roundtrip", "</foo>", xpp.getText())

        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.IGNORABLE_WHITESPACE, None, 0, None, None,
                           " \r\n", False, -1)
        assert xpp.isWhitespace()

        xpp.nextToken()
        checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)
        with pytest.raises(Exception, message="whitespace function must fail for START_DOCUMENT"):
            xpp.isWhitespace()

        # reset parser
        xpp.setInput(None)

        if not roundtripSupported:
            return

        xpp.setInput(MISC_XML)
        holderForStartAndLength = [0, 0]
        sw = ''
        while xpp.nextToken() != xpp.END_DOCUMENT:
            case = xpp.getEventType()
            # case xpp.START_DOCUMENT:
            # case xpp.END_DOCUMENT:
            #  break LOOP
            if case == XmlPullParser.START_TAG:
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip START_TAG", xpp.getText(), s)
                sw += s
            elif case == XmlPullParser.END_TAG:
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip END_TAG", xpp.getText(), s)
                sw += s
            elif case == XmlPullParser.TEXT:
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip TEXT", xpp.getText(), s)
                sw += s
            elif case == XmlPullParser.IGNORABLE_WHITESPACE:
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip IGNORABLE_WHITESPACE", xpp.getText(), s)
                sw += s
            elif case == XmlPullParser.CDSECT:
                sw += "<![CDATA["
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip CDSECT", xpp.getText(), s)
                sw += s
                sw += "]]>"
            elif case == XmlPullParser.PROCESSING_INSTRUCTION:
                sw += "<?"
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip PROCESSING_INSTRUCTION", xpp.getText(), s)
                sw += s
                sw += "?>"
            elif case == XmlPullParser.COMMENT:
                sw += "<!--"
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip COMMENT", xpp.getText(), s)
                sw += s
                sw += "-->"
                pass
            elif case == XmlPullParser.ENTITY_REF:
                sw += "&"
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip ENTITY_REF", xpp.getText(), s)
                sw += s
                sw += ";"
                pass
            elif case == XmlPullParser.DOCDECL:
                sw += "<!DOCTYPE"
                buf = xpp.getTextCharacters(holderForStartAndLength)
                s = ''.join(buf)
                assertEquals("roundtrip DOCDECL", xpp.getText(), s)
                sw += s
                sw += ">"
                pass
            else:
                raise Exception('RuntimeException: "unknown token type"')

        RESULT_XML_BUF = sw
        assertEquals("rountrip XML", printable(MISC_XML), printable(RESULT_XML_BUF))

