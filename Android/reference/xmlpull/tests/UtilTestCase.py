# -*- coding: utf-8 -*-
# Ported from:
# http://www.xmlpull.org/v1/download/unpacked/src/java/tests/org/xmlpull/v1/tests/UtilTestCase.java
#
# /**
#  * Some common utilities to help with XMLPULL tests.
#  *
#  * @author <a href="http://www.extreme.indiana.edu/~aslom/">Aleksander Slominski</a>
#  */
import pytest

def assertEquals(*args):
    if len(args) == 3:
        msg, x, y = args
    else:
        (x, y), msg = args, ''
    assert x == y, msg

factory = None
TEST_XML = \
    "<root>\n" + \
    "<foo>bar</foo>\r\n" + \
    "<hugo xmlns=\"http://www.xmlpull.org/temp\"> \n\r \n" + \
    "  <hugochild>This is in a <!-- comment -->new namespace</hugochild>" + \
    "</hugo>\t\n" + \
    "<bar testattr='123abc' />" + \
    "</root>\n" + \
    "\n" + \
    "<!-- an xml sample document without meaningful content -->\n"

def checkParserState(xpp, depth, type, name, text, isEmpty, attribCount):
    assertEquals("PROCESS_NAMESPACES", False, xpp.getFeature(xpp.FEATURE_PROCESS_NAMESPACES))
    assertEquals("TYPES[getType()]", xpp.TYPES[type], xpp.TYPES[xpp.getEventType()])
    assertEquals("getType()", type, xpp.getEventType())
    assertEquals("getDepth()", depth, xpp.getDepth())
    assertEquals("getPrefix()", None, xpp.getPrefix())
    assertEquals("getNamespacesCount(getDepth())", 0, xpp.getNamespaceCount(depth))
    if xpp.getEventType() == xpp.START_TAG or xpp.getEventType() == xpp.END_TAG:
        assertEquals("getNamespace()", "", xpp.getNamespace())
    else:
        assertEquals("getNamespace()", None, xpp.getNamespace())
    assertEquals("getName()", name, xpp.getName())

    if xpp.getEventType() != xpp.START_TAG and xpp.getEventType() != xpp.END_TAG:
        assertEquals("getText()", printable(text), printable(xpp.getText()))

        holderForStartAndLength = [0, 0]
        buf = xpp.getTextCharacters(holderForStartAndLength)
        if buf != None:
            s = ''.join(buf)
            assertEquals("getText(holder)", printable(text), printable(s))
        else:
            assertEquals("getTextCharacters()", None, text)
    if type == xpp.START_TAG:
        assertEquals("isEmptyElementTag()", isEmpty, xpp.isEmptyElementTag())
    else:
        with pytest.raises(Exception):
            xpp.isEmptyElementTag()
    assertEquals("getAttributeCount()", attribCount, xpp.getAttributeCount())

def checkParserStateNs(xpp, depth, type, prefix, nsCount, namespace, name, text, isEmpty, attribCount):
    # this methid can be used with enabled and not enabled namespaces
    # assertEquals("PROCESS_NAMESPACES", True, xpp.getFeature(xpp.FEATURE_PROCESS_NAMESPACES))
    assertEquals("getType()", type, xpp.getEventType())
    assertEquals("TYPES[getType()]", xpp.TYPES[type], xpp.TYPES[xpp.getEventType()])
    assertEquals("getName()", name, xpp.getName())

    assertEquals("getDepth()", depth, xpp.getDepth())
    assertEquals("getPrefix()", prefix, xpp.getPrefix())
    assertEquals("getNamespacesCount(getDepth())", nsCount, xpp.getNamespaceCount(depth))
    assertEquals("getNamespace()", namespace, xpp.getNamespace())

    if xpp.getEventType() != xpp.START_TAG and xpp.getEventType() != xpp.END_TAG:
        assertEquals("getText()", printable(text), printable(xpp.getText()))

        holderForStartAndLength = [0, 0]
        buf = xpp.getTextCharacters(holderForStartAndLength)
        if buf != None:
            s = ''.join(buf)
            assertEquals("getText(holder)", printable(text), printable(s))
        else:
            assertEquals("getTextCharacters()", None, text)
    if type == xpp.START_TAG:
        assertEquals("isEmptyElementTag()", isEmpty, xpp.isEmptyElementTag())
    else:
        with pytest.raises(Exception):
            xpp.isEmptyElementTag()
    assertEquals("getAttributeCount()", attribCount, xpp.getAttributeCount())

def checkAttrib(xpp, pos, name, value):
    assertEquals("must be on START_TAG", xpp.START_TAG, xpp.getEventType())
    assertEquals("getAttributePrefix()",None, xpp.getAttributePrefix(pos))
    assertEquals("getAttributeNamespace()","", xpp.getAttributeNamespace(pos))
    assertEquals("getAttributeName()",name, xpp.getAttributeName(pos))
    assertEquals("getAttributeValue()",value, xpp.getAttributeValue(pos))
    assertEquals("getAttributeValue(name)",value, xpp.getAttributeValue(None, name))

def checkAttribNs(xpp, pos, prefix, namespace, name, value):
    assertEquals("must be on START_TAG", xpp.START_TAG, xpp.getEventType())
    assertEquals("getAttributePrefix()",prefix, xpp.getAttributePrefix(pos))
    assertEquals("getAttributeNamespace()",namespace, xpp.getAttributeNamespace(pos))
    assertEquals("getAttributeName()",name, xpp.getAttributeName(pos))
    assertEquals("getAttributeValue()",printable(value), printable(xpp.getAttributeValue(pos)))
    assertEquals("getAttributeValue(ns,name)",
                 printable(value), printable(xpp.getAttributeValue(namespace, name)))

def checkNamespace(xpp, pos, prefix, uri, checkMapping):
    assertEquals("getNamespacePrefix()",prefix, xpp.getNamespacePrefix(pos))
    assertEquals("getNamespaceUri()",uri, xpp.getNamespaceUri(pos))
    if checkMapping:
        assertEquals("getNamespace(prefix)", uri, xpp.getNamespace (prefix))

def printable(s):
    return s



