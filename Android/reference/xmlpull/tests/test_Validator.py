# -*- coding: utf-8 -*-
import pytest
import xml.parsers.expat
import StringIO

from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from Android.reference.xmlpull.XmlPullParserValidator import XmlPullParserValidator

DOCTYPESTR = """<?xml version="1.0"?>
<!DOCTYPE person [
  <!ELEMENT seq1 (#PCDATA)>
  <!ELEMENT seq2 (#PCDATA)>
  <!ELEMENT seq3 (#PCDATA)>
  <!ELEMENT seq (seq1, seq3)>
  <!ELEMENT opt (opt1 | opt2 | opt3)>
  <!ELEMENT pcdata (#PCDATA)>
  <!ELEMENT atag (#PCDATA)>
  <!ELEMENT mixed (#PCDATA | atag | pcdata)*>
  <!ELEMENT empty EMPTY>
  <!ELEMENT any ANY>
  <!ELEMENT first_name (#PCDATA)>
  <!ELEMENT middle_name (#PCDATA)>
  <!ELEMENT last_name  (#PCDATA)>
  <!ELEMENT profession (#PCDATA)>
  <!ELEMENT name (first_name, middle_name*, last_name?)>
  <!ELEMENT person     (name, profession*)>
  <!ELEMENT methodResponse (params | fault)>
  <!ELEMENT circle (center, (radius | diameter))>
  <!ELEMENT center ((x, y) | (y, x) | (r, theta ) | (theta , r))>
  <!ELEMENT x (#PCDATA)>
  <!ELEMENT y (#PCDATA)>
  <!ELEMENT r (#PCDATA)>
  <!ELEMENT theta (#PCDATA)>  
  <!ELEMENT radius (#PCDATA)>  
  <!ELEMENT diameter (#PCDATA)>  
]>
<person />"""

@pytest.fixture(scope='module')
def factory():
    factory = XmlPullParserFactory.newInstance()
    factory.setValidating(True)
    assert factory.getFeature(XmlPullParser.FEATURE_VALIDATION)
    return factory

@pytest.fixture(scope='module')
def builder():
    return XmlPullParserValidator.Factory.createFromString(DOCTYPESTR)

def testElementEmpty(factory):
    pp = factory.newPullParser()
    XML_EMPTY_TAG = """<?xml version="1.0"?>
    <!DOCTYPE any [
    <!ELEMENT empty EMPTY>
    <!ELEMENT any ANY>
    ]>    
    <any str="test_empty_tag">
        <empty str="open_close_tag"></empty>
        <empty str="self_close_tag"/>
    </any>"""
    pp.setInput(XML_EMPTY_TAG)
    while pp.next() != XmlPullParser.END_DOCUMENT:
        pass
    assert pp.getEventType() == XmlPullParser.END_DOCUMENT

    XML_EMPTY_TAG = """<?xml version="1.0"?>
    <!DOCTYPE any [
    <!ELEMENT empty EMPTY>
    <!ELEMENT any ANY>
    ]>    
    <any str="test_empty_tag">
        <empty str = "error_empty_tag_with_child" >
            <theta>10</theta>
        </empty >
    </any>"""
    pp.setInput(XML_EMPTY_TAG)
    errmessage = 'ValidatorError: Element type "theta" must be declared.'
    checkExcInfo(pp, 256, (8, 12), errmessage)

def testElementMixed(factory, builder):
    xmlStr = """<?xml version="1.0"?>
    <any str="mixed content">
    <mixed>The <atag>Turing Machine</atag> is an abstract finite
    state automaton with infinite memory that can be proven equivalent
    to any any other <pcdata>finite state automaton</pcdata> with arbitrarily large memory.
    Thus what is true for a <atag>Turing machine</atag> is true for all equivalent
    machines no matter how implemented.
    </mixed></any>"""
    pp = factory.newPullParser()
    pp.setInput(xmlStr, None, builder.setRoot('any').newParserValidator())
    while pp.next() != XmlPullParser.END_DOCUMENT:
        pass
    assert pp.getEventType() == XmlPullParser.END_DOCUMENT

def testElementSequence(factory, builder):
    xmlStr = """<?xml version="1.0"?>
    <any str="well formed">
        <name>
          <first_name>Madonna</first_name>
          <last_name>Ciconne</last_name>
        </name>
        <name>
          <first_name>Madonna</first_name>
          <middle_name>Louise</middle_name>
          <last_name>Ciconne</last_name>
        </name>
        <name>
          <first_name>Madonna</first_name>
          <middle_name>Louise</middle_name>
          <middle_name>Marie</middle_name>
          <last_name>Ciconne</last_name>
        </name>
        <name>
          <first_name>Madonna</first_name>
        </name>
    </any>"""
    pp = factory.newPullParser()
    pp.setInput(xmlStr, None, builder.setRoot('any').newParserValidator())
    while pp.next() != XmlPullParser.END_DOCUMENT:
        pass
    assert pp.getEventType() == XmlPullParser.END_DOCUMENT

    seqStr = """<?xml version="1.0"?>
    <seq str="invalid elements flipped">
        <seq3>dos</seq3>
        <seq1>uno</seq1>
    </seq>"""
    pp.setInput(seqStr, None, builder.setRoot('seq').newParserValidator())
    errmessage = u'ValidatorError: Tag "seq3" not in sequence or a valid option for "seq"'
    checkExcInfo(pp, 256, (3, 8), errmessage)

    seqStr = """<?xml version="1.0"?>
    <seq str="invalid elements flipped">
        <seq1>uno</seq1>
    </seq>"""
    pp.setInput(seqStr, None, builder.setRoot('seq').newParserValidator())
    errmessage = u'ValidatorError: Tag "seq" requires "seq3" tag(s)'
    checkExcInfo(pp, 256, (4, 4), errmessage)

def testElementOption(factory):
    pp = factory.newPullParser()

    XML_OPTION_1 = """<?xml version="1.0"?>
    <!DOCTYPE circle [
    <!ELEMENT x (#PCDATA)>
    <!ELEMENT y (#PCDATA)>
    <!ELEMENT r (#PCDATA)>
    <!ELEMENT theta (#PCDATA)>  
    <!ELEMENT radius (#PCDATA)>  
    <!ELEMENT diameter (#PCDATA)>  
    <!ELEMENT circle (center, (radius | diameter))>
    <!ELEMENT center ((x, y) | (y, x) | (r, theta ) | (theta , r))>
    ]>
    <circle>
      <center>
        <y>10.0</y>
        <x>2.5</x>
      </center>
      <radius>30</radius>
    </circle>"""
    pp.setInput(XML_OPTION_1)
    while pp.next() != XmlPullParser.END_DOCUMENT:
        pass
    assert pp.getEventType() == XmlPullParser.END_DOCUMENT

    XML_OPTION_2 = """<?xml version="1.0"?>
    <!DOCTYPE circle [
    <!ELEMENT x (#PCDATA)>
    <!ELEMENT y (#PCDATA)>
    <!ELEMENT r (#PCDATA)>
    <!ELEMENT theta (#PCDATA)>  
    <!ELEMENT radius (#PCDATA)>  
    <!ELEMENT diameter (#PCDATA)>  
    <!ELEMENT circle (center, (radius | diameter))>
    <!ELEMENT center ((x, y) | (y, x) | (r, theta ) | (theta , r))>
    ]>
    <circle>
      <center>
        <theta>10.0</theta>
        <r>2.5</r>
      </center>
      <diameter>30</diameter>
    </circle>"""
    pp.setInput(XML_OPTION_2)
    while pp.next() != XmlPullParser.END_DOCUMENT:
        pass
    assert pp.getEventType() == XmlPullParser.END_DOCUMENT

def checkExcInfo(pp, errcode, position, errmessage):
    with pytest.raises(SyntaxError) as exc_info:
        while pp.next() != XmlPullParser.END_DOCUMENT:
            pass
    assert exc_info.typename is 'ParseError'
    assert exc_info.value.code == errcode
    assert exc_info.value.position == position
    assert exc_info.value.args[0].message == errmessage

def validatorEvaluator():
    def testStr(xmlValidator, xmlStr, root=None):
        xmlValidator.setInput(xmlStr)
        if root:
            xmlValidator.setRoot(root)
        while True:
            event = xmlValidator.next()
            print event
            if event.event_type == XmlPullParser.END_DOCUMENT:
                break
        assert event.event_type == XmlPullParser.END_DOCUMENT

    factory = XmlPullParserValidator.Factory()
    xmlValidator = factory.newXmlValidator(DOCTYPESTR)

    xmlStr = """<?xml version="1.0"?>
    <opt str="invalid elements flipped">
        <opt1>dos</opt1>
    </opt>"""
    testStr(xmlValidator, xmlStr, 'opt')
    print 80*'='

    xmlStr = """<?xml version="1.0"?>
    <opt str="invalid elements flipped">
        <seq1>dos</seq1>
    </opt>"""
    testStr(xmlValidator,xmlStr)
    print 80*'='

    xmlStr = """<?xml version="1.0"?>
    <seq str="invalid elements flipped">
        <seq1>dos</seq1>
        <seq2>uno</seq2>
    </seq>"""
    testStr(xmlValidator,xmlStr, 'seq')
    print 80*'='

    xmlStr = """<?xml version="1.0"?>
    <seq str="invalid elements flipped">
        <seq3>dos</seq3>
        <seq1>uno</seq1>
    </seq>"""
    testStr(xmlValidator,xmlStr)
    print 80*'='

    xmlStr = """<?xml version="1.0"?>
    <seq str="invalid elements flipped">
        <seq1>uno</seq1>
    </seq>"""
    testStr(xmlValidator,xmlStr)
    print 80*'='

    xmlStr = """<?xml version="1.0"?>
    <!DOCTYPE any [
      <!ELEMENT any ANY>
      <!ELEMENT seq1 (#PCDATA)>
      <!ELEMENT seq2 (#PCDATA)>
      <!ELEMENT seq3 (#PCDATA)>
      <!ELEMENT seq (seq1, seq3)>
    ]>
    <any>
        <seq str="invalid elements flipped">
            <seq1>
                <seq2>dos</seq2>
            </seq1>
            <seq3>dos</seq3>
        </seq>
        <seq str="invalid elements flipped">
            <seq1>uno</seq1>
            <seq3>dos</seq3>
            <seq2>dos</seq2>
        </seq>
        <seq str="invalid elements flipped">
            <seq3>dos</seq3>
            <seq1>uno</seq1>
        </seq>
        <seq str="invalid elements flipped">
            <seq1>uno</seq1>
        </seq>
    </any>"""
    xmlValidator = factory.newXmlValidator()
    testStr(xmlValidator,xmlStr)
    print 80*'='
    pass


