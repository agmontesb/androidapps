# -*- coding: utf-8 -*-

# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestEvent.java
# /**
#  * More complete test to verify paring.
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestEvent():

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
        assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    @classmethod
    def teardown_class(cls):
        pass

    def test_Event(self):
        factory = self.factory
        xpp = factory.newPullParser()
        xpp.setInput(TEST_XML)

        checkParserStateNs(xpp, 0, xpp.START_DOCUMENT, None, 0, None, None, None, False, -1)

        xpp.next()
        checkParserStateNs(xpp, 1, xpp.START_TAG, None, 0, "", "root", None, False, 0)
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.TEXT, None, 0, None, None, "\n", False, -1)

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.START_TAG, None, 0, "", "foo", None, False, 0)
        xpp.next()
        checkParserStateNs(xpp, 2, xpp.TEXT, None, 0, None, None, "bar", False, -1)
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.END_TAG, None, 0, "", "foo", None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.TEXT, None, 0, None, None, "\r\n", False, -1)

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.START_TAG,
                           None, 0, "http://www.xmlpull.org/temp", "hugo", None, False, 0)
        xpp.next()
        checkParserStateNs(xpp, 2, xpp.TEXT, None, 0, None, None, " \n\r \n  ", False, -1)

        xpp.next()
        checkParserStateNs(xpp, 3, xpp.START_TAG,
                           None, 0, "http://www.xmlpull.org/temp", "hugochild", None, False, 0)
        xpp.next()
        checkParserStateNs(xpp, 3, xpp.TEXT, None, 0, None, None,
                           "This is in a new namespace", False, -1)
        xpp.next()
        checkParserStateNs(xpp, 2, xpp.END_TAG,
                           None, 0, "http://www.xmlpull.org/temp", "hugochild", None, False, -1)

        xpp.next()
        checkParserStateNs(xpp, 1, xpp.END_TAG,
                           None, 0, "http://www.xmlpull.org/temp", "hugo", None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.TEXT, None, 0, None, None, "\t\n", False, -1)

        xpp.next()
        checkParserStateNs(xpp, 2, xpp.START_TAG, None, 0, "", "bar", None, True, 1)
        checkAttribNs(xpp, 0, None, "", "testattr", "123abc")
        xpp.next()
        checkParserStateNs(xpp, 1, xpp.END_TAG, None, 0, "", "bar", None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_TAG, None, 0, "", "root", None, False, -1)
        xpp.next()
        checkParserStateNs(xpp, 0, xpp.END_DOCUMENT, None, 0, None, None, None, False, -1)
