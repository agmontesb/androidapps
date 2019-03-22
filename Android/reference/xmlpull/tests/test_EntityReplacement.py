# -*- coding: utf-8 -*-

# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/TestEntityReplacement.java
# /**
#  * Test if entity replacement works ok.
#  * This test is designe to work bboth for validating and non validating parsers!
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from UtilTestCase import *


class TestEntityReplacement:

    @classmethod
    def setup_class(cls):
        cls.factory = factory = XmlPullParserFactory.newInstance()
        factory.setNamespaceAware(True)
        assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
        assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    @classmethod
    def teardown_class(cls):
        pass

    def test_EntityReplacementInit(self):
        # taken from http://www.w3.org/TR/REC-xml#sec-entexpand
        XML_ENTITY_EXPANSION = \
            "<?xml version='1.0'?>\n" + \
            "<!DOCTYPE test [\n" + \
            "<!ELEMENT test (#PCDATA) >\n" + \
            "<!ENTITY % xx '&#37;zz;'>\n" + \
            "<!ENTITY % zz '&#60;!ENTITY tricky \"error-prone\" >' >\n" + \
            "%xx;\n" + \
            "]>" + \
            "<test>This sample shows a &tricky; method.</test>";

        pp = self.factory.newPullParser()
        # default parser must work!!!!
        pp.setInput(XML_ENTITY_EXPANSION )
        if not pp.getFeature( pp.FEATURE_PROCESS_DOCDECL ):
            pp.defineEntityReplacementText("tricky", "error-prone")
        self._EntityReplacementTest(pp)

        # now we try for no FEATURE_PROCESS_DOCDECL
        pp.setInput(XML_ENTITY_EXPANSION )
        try:
            pp.setFeature( pp.FEATURE_PROCESS_DOCDECL, False )
        except  Exception as ex:
            pass
        
        if not pp.getFeature( pp.FEATURE_PROCESS_DOCDECL ):
            pp.defineEntityReplacementText("tricky", "error-prone")
            self._EntityReplacementTest(pp)

        # try to use FEATURE_PROCESS_DOCDECL if supported
        pp.setInput(None)
        try:
            pp.setFeature( pp.FEATURE_PROCESS_DOCDECL, True )
            pp.setInput(XML_ENTITY_EXPANSION )
        except  Exception as ex:
            pass

        if  pp.getFeature( pp.FEATURE_PROCESS_DOCDECL ):
            self._EntityReplacementTest(pp)

    def _EntityReplacementTest(self, pp):
        pp.next()
        checkParserStateNs(pp, 1, pp.START_TAG,
                           None, 0, "", "test", None, False, 0)
        pp.next()
        checkParserStateNs(pp, 1, pp.TEXT, None, 0, None, None,
                           "This sample shows a error-prone method.", False, -1)
        pp.next()
        checkParserStateNs(pp, 0, pp.END_TAG,
                           None, 0, "", "test", None, False, -1)
        pp.nextToken()
        checkParserStateNs(pp, 0, pp.END_DOCUMENT, None, 0, None, None, None, False, -1)

