# -*- coding: utf-8 -*-
''''''
from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.Compile.ResourceParser import ResourceParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from Tools.aapt.ResourcesValues import Reference, String, BinaryPrimitive
from Tools.aapt.test import Common
import Tools.aapt.StringPool as StringPool
import Tools.aapt.ResourcesTypes as ResourcesTypes

mDiagnostics = ResourceUtils.Diagnostics()
factory = XmlPullParserFactory.newInstance()
factory.setNamespaceAware(True)
xmlParser = factory.newPullParser()

kXmlPreamble = '<?xml version=\"1.0\" encoding=\"utf-8\"?>\n'
mTable = None

def test_FailToParseWithNoRootResourcesElement():
    input = kXmlPreamble
    input += '<attr name=\"foo\"/>'
    table = ResourceTable()
    parser = ResourceParser(mDiagnostics, table, "test", None)
    xmlParser.setInput(input)
    assert not parser.parse(xmlParser)
    
def parseInput(xmlStr):
    global mTable
    mTable = ResourceTable()
    input = kXmlPreamble
    input += '<resources>\n' + xmlStr + '\n</resources>'
    mDiagnostics = ResourceUtils.Diagnostics()
    parser = ResourceParser(mDiagnostics, mTable, "test", None)
    xmlParser.setInput(input)
    return parser.parse(xmlParser)
        
def test_ParseQuotedString():
    input = '<string name=\"foo\">   \"  hey there \" </string>'
    assert parseInput(input)
    aStr = Common.getValue(mTable, "@string/foo")
    assert aStr
    assert "  hey there " == StringPool.pointee(aStr.value)

def test_ParseEscapedString():
    input = '<string name="foo">\\?123</string>'
    assert parseInput(input)
    aStr = Common.getValue(mTable, u"@string/foo")
    assert aStr
    assert "?123" == StringPool.pointee(aStr.value)

def test_IgnoreXliffTags():
    input = '<string name="foo" \n' \
            '        xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">\n' \
            '  There are <xliff:g id="count">%1$d</xliff:g> apples</string>'
    assert parseInput(input)
    aStr = Common.getValue(mTable, u"@string/foo")
    assert aStr
    assert u"There are %1$d apples" ==  StringPool.pointee(aStr.value)

def test_ParseNull():
    input = '<integer name=\"foo\">@null</integer>'
    assert parseInput(input)
    integer = Common.getValue(mTable, u"@integer/foo")
    #  The Android runtime treats a value of android.Res_value.TYPE_NULL as
    #  a non-existing value, and this causes problems in styles when trying to resolve
    #  an attribute. Null values must be encoded as android.Res_value.TYPE_REFERENCE
    #  with a data value of 0.
    assert integer
    assert 0 ==  integer.value.data

def test_ParseEmpty():
    input = '<integer name=\"foo\">@empty</integer>'
    assert parseInput(input)
    integer = Common.getValue(mTable, u"@integer/foo")
    assert integer
    assert integer.value.dataType == ResourcesTypes.Res_value.TYPE_NULL
    assert integer.value.data == ResourcesTypes.Res_value.DATA_NULL_EMPTY

def test_ParseAttr():
    input = '<attr name="foo" format="string"/>\n<attr name="bar"/>'
    assert parseInput(input)
    attr = Common.getValue(mTable, u"@attr/foo")
    assert attr
    assert attr.typeMask == ResourcesTypes.ResTable_map.TYPE_STRING
    attr = Common.getValue(mTable, u"@attr/bar")
    assert attr
    assert attr.typeMask == ResourcesTypes.ResTable_map.TYPE_ANY


def test_ParseUseAndDeclOfAttr():
    input = '<declare-styleable name="Styleable">\n' \
            '  <attr name="foo" />\n' \
            '</declare-styleable>\n' \
            '<attr name="foo" format="string"/>'
    assert parseInput(input)
    attr = Common.getValue(mTable, u"@attr/foo")
    assert attr
    assert attr.typeMask == ResourcesTypes.ResTable_map.TYPE_STRING


def test_ParseDoubleUseOfAttr():
    input = '<declare-styleable name="Theme">' \
            '  <attr name="foo" />\n' \
            '</declare-styleable>\n' \
            '<declare-styleable name="Window">\n' \
            '  <attr name="foo" format="boolean"/>\n' \
            '</declare-styleable>'
    assert parseInput(input)
    attr = Common.getValue(mTable, u"@attr/foo")
    assert attr
    assert attr.typeMask == ResourcesTypes.ResTable_map.TYPE_BOOLEAN

def test_ParseEnumAttr():
    input = '<attr name="foo">\n' \
            '  <enum name="bar" value="0"/>\n' \
            '  <enum name="bat" value="1"/>\n' \
            '  <enum name="baz" value="2"/>\n' \
            '</attr>'
    assert parseInput(input)
    enumAttr = Common.getValue(mTable, u"@attr/foo")
    assert enumAttr
    assert enumAttr.typeMask == ResourcesTypes.ResTable_map.TYPE_ENUM
    assert len(enumAttr.symbols) == 3
    assert enumAttr.symbols[0].symbol.name
    assert enumAttr.symbols[0].symbol.name.entry == u"bar"
    assert enumAttr.symbols[0].value == 0
    assert enumAttr.symbols[1].symbol.name
    assert enumAttr.symbols[1].symbol.name.entry == u"bat"
    assert enumAttr.symbols[1].value == 1

    assert enumAttr.symbols[2].symbol.name
    assert enumAttr.symbols[2].symbol.name.entry == u"baz"
    assert enumAttr.symbols[2].value == 2


def test_ParseFlagAttr():
    input = '<attr name="foo">\n' \
            '  <flag name="bar" value="0"/>\n' \
            '  <flag name="bat" value="1"/>\n' \
            '  <flag name="baz" value="2"/>\n' \
            '</attr>'
    assert parseInput(input)
    flagAttr = Common.getValue(mTable, u"@attr/foo")
    assert flagAttr
    assert flagAttr.typeMask == ResourcesTypes.ResTable_map.TYPE_FLAGS
    assert len(flagAttr.symbols) == 3
    assert flagAttr.symbols[0].symbol.name
    assert flagAttr.symbols[0].symbol.name.entry == u"bar"
    assert flagAttr.symbols[0].value == 0
    assert flagAttr.symbols[1].symbol.name
    assert flagAttr.symbols[1].symbol.name.entry == u"bat"
    assert flagAttr.symbols[1].value == 1
    assert flagAttr.symbols[2].symbol.name
    assert flagAttr.symbols[2].symbol.name.entry == u"baz"
    assert flagAttr.symbols[2].value == 2
    flagValue = ResourceUtils.tryParseFlagSymbol(flagAttr,u"baz|bat")
    assert flagValue
    assert flagValue.value.data == 1 | 2

# def test_FailToParseEnumAttrWithNonUniqueKeys():
#     input = '<attr name="foo">\n' \
#             '  <enum name="bar" value="0"/>\n' \
#             '  <enum name="bat" value="1"/>\n' \
#             '  <enum name="bat" value="2"/>\n' \
#             '</attr>'
#     assert not parseInput(input)

def test_ParseStyle():
    input = '<style name="foo" parent="@style/fu">\n' \
            '  <item name="bar">#ffffffff</item>\n' \
            '  <item name="bat">@string/hey</item>\n' \
            '  <item name="baz"><b>hey</b></item>\n' \
            '</style>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo")
    assert style
    assert style.parent
    assert style.parent.name
    assert Common.parseNameOrDie(u"@style/fu") == style.parent.name
    assert len(style.entries) == 3
    assert style.entries[0].key.name
    assert Common.parseNameOrDie(u"@attr/bar") == style.entries[0].key.name
    assert style.entries[1].key.name
    assert Common.parseNameOrDie(u"@attr/bat") == style.entries[1].key.name
    assert style.entries[2].key.name
    assert Common.parseNameOrDie(u"@attr/baz") == style.entries[2].key.name


def test_ParseStyleWithShorthandParent():
    input = '<style name="foo" parent="com.app:Theme"/>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo")
    assert style
    assert style.parent
    assert style.parent.name
    assert Common.parseNameOrDie(u"@com.app:style/Theme") == style.parent.name

def test_ParseStyleWithPackageAliasedParent():
    input = '<style xmlns:app="http://schemas.android.com/apk/res/android"\n' \
            '       name="foo" parent="app:Theme"/>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo")
    assert style
    assert style.parent
    assert style.parent.name
    assert Common.parseNameOrDie(u"@android:style/Theme") == style.parent.name

def test_ParseStyleWithPackageAliasedItems():
    input = \
            '<style xmlns:app="http://schemas.android.com/apk/res/android" name="foo">\n' \
            '  <item name="app:bar">0</item>\n' \
            '</style>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo")
    assert style
    assert len(style.entries) == 1
    assert Common.parseNameOrDie(u"@android:attr/bar") == style.entries[0].key.name

def test_ParseStyleWithInferredParent():
    input = '<style name="foo.bar"/>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo.bar")
    assert style
    assert style.parent
    assert style.parent.name
    assert style.parent.name == Common.parseNameOrDie(u"@style/foo")
    assert style.parentInferred

def test_ParseStyleWithInferredParentOverridenByEmptyParentAttribute():
    input = '<style name="foo.bar" parent=""/>'
    assert parseInput(input)
    style = Common.getValue(mTable, u"@style/foo.bar")
    assert style
    assert not style.parent
    assert not style.parentInferred

def test_ParseAutoGeneratedIdReference():
    input = '<string name="foo">@+id/bar</string>'
    assert parseInput(input)
    id = Common.getValue(mTable, u"@id/bar")
    assert id

def test_ParseAttributesDeclareStyleable():
    input = '<declare-styleable name="foo">\n' \
            '  <attr name="bar" />\n' \
            '  <attr name="bat" format="string|reference"/>\n' \
            '</declare-styleable>'
    assert parseInput(input)
    attr = Common.getValue(mTable, u"@attr/bar")
    assert attr
    assert attr.isWeak()
    attr = Common.getValue(mTable, u"@attr/bat")
    assert attr
    assert attr.isWeak()
    styleable = Common.getValue(mTable, u"@styleable/foo")
    assert styleable
    assert len(styleable.entries) == 2
    assert Common.parseNameOrDie(u"@attr/bar") == styleable.entries[0].name
    assert Common.parseNameOrDie(u"@attr/bat") == styleable.entries[1].name

def test_ParseArray():
    input = '<array name="foo">\n' \
            '  <item>@string/ref</item>\n' \
            '  <item>hey</item>\n' \
            '  <item>23</item>\n' \
            '</array>'
    assert parseInput(input)
    array = Common.getValue(mTable, u"@array/foo")
    assert array
    assert 3 == len(array.items)
    assert isinstance(array.items[0], Reference)
    assert isinstance(array.items[1], String)
    assert isinstance(array.items[2], BinaryPrimitive)

def test_ParsePlural():
    input = '<plurals name="foo">\n' \
            '  <item quantity="other">apples</item>\n' \
            '  <item quantity="one">apple</item>\n' \
            '</plurals>'
    assert parseInput(input)
    pass

def test_ParseCommentsWithResource():
    input = '<!-- This is a comment -->\n' \
            '<string name="foo">Hi</string>'
    assert parseInput(input)
    result = mTable.findResource(Common.parseNameOrDie(u"@string/foo"))
    assert result
    entry = result.entry
    assert entry
    assert entry.values
    assert entry.values[0].comment == u"This is a comment"

# /*
#  * Declaring an ID as public should not require a separate definition
#  * (as an ID has no value).
#  */
def test_ParsePublicIdAsDefinition():
    input = '<public type="id" name="foo"/>'
    assert parseInput(input)
    id = Common.getValue(mTable, u"@id/foo")
    assert id

