# -*- coding: utf-8 -*-
import collections
import io

from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.flatten.XmlFlattener import XmlFlattenerOptions, XmlFlattener
from Tools.aapt.NameMangler import NameManglerPolicy
from Tools.aapt.Resource import ResourceId, ResourceFile
from Tools.aapt.test.Builders import AttributeBuilder, buildXmlDom
from Tools.aapt.test.Context import ContextBuilder, StaticSymbolTableBuilder
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory

import Tools.aapt.ResourcesLab as rl


class ExtResChunkHeader(rl.ResChunkHeader):
    typeMap = rl.ResChunkHeader.typeMap
    typeMap.update([
        (0x000c, 'RES_FILE_EXPORT_TYPE'),
        (0x000d, 'RES_TABLE_PUBLIC_TYPE'),
        (0x000e, 'RES_TABLE_SOURCE_POOL_TYPE'),
        (0x000f, 'RES_TABLE_SYMBOL_TABLE_TYPE'),
    ])


ResXml = collections.namedtuple('ResXml', 'file parser')
factory = XmlPullParserFactory.newInstance()
factory.setNamespaceAware(True)
assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)


class XmlFlattenerTest(object):

    @classmethod
    def setup_class(cls):
        cls.mContext = ContextBuilder()\
            .setCompilationPackage("com.app.test")\
            .setNameManglerPolicy(NameManglerPolicy("com.app.test"))\
            .setSymbolTable(
                StaticSymbolTableBuilder()
                    .addSymbol(
                        "@android:attr/id", 
                        ResourceId(0x010100d0),
                        AttributeBuilder().build()
                    ).addSymbol(
                        "@com.app.test:id/id", 
                        ResourceId(0x7f020000)
                    ).addSymbol(
                        "@android:attr/paddingStart", 
                        ResourceId(0x010103b3),
                        AttributeBuilder().build()
                    ).addSymbol(
                        "@android:attr/colorAccent", 
                        ResourceId(0x01010435),
                        AttributeBuilder().build()
                    ).build()
            ).build()

    def flatten(self, buffer, doc, parser, options=None, linker=None):
        options = options or XmlFlattenerOptions()
        parser.setInput(doc)
        resXml = ResXml(ResourceFile(), parser)
        flattener = XmlFlattener(buffer, options)
        if not flattener.consume(self.mContext, resXml, linker):
            return False    # "failed to flatten XML Tree"
        return True

    def dumpXmlTree(self, buffer):
        iobuffer = ''
        for blk in iter(buffer):
            iobuffer += blk.buffer[:blk.size]

        iobuffer = str(iobuffer)
        data = io.BytesIO(iobuffer)

        crawler = rl.dumpXmlTree(data, headerClass=ExtResChunkHeader)

        pass


    def test_FlattenXmlWithNoCompiledAttributes(self):
        doc = buildXmlDom(
            '<View xmlns:test="http://com.test" '
            'attr="hey">'
            '<Layout test:hello="hi" />'
            '<Layout>Some text</Layout>'
            '</View>'
        )
        buffer = BigBuffer(1024)
        xmlParser = factory.newPullParser()
        assert self.flatten(buffer, doc, xmlParser)

        self.dumpXmlTree(buffer)

        # ASSERT_EQ(tree.next(), android::ResXMLTree::START_NAMESPACE)
        # size_t len
        # const char16_t* namespacePrefix = tree.getNamespacePrefix(&len)
        # EXPECT_EQ(StringPiece16(namespacePrefix, len), "test")
        # const char16_t* namespaceUri = tree.getNamespaceUri(&len)
        # ASSERT_EQ(StringPiece16(namespaceUri, len), "http://com.test")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::START_TAG)
        # ASSERT_EQ(tree.getElementNamespace(&len), nullptr)
        # const char16_t* tagName = tree.getElementName(&len)
        # EXPECT_EQ(StringPiece16(tagName, len), "View")
        # ASSERT_EQ(1u, tree.getAttributeCount())
        # ASSERT_EQ(tree.getAttributeNamespace(0, &len), nullptr)
        # const char16_t* attrName = tree.getAttributeName(0, &len)
        # EXPECT_EQ(StringPiece16(attrName, len), "attr")
        # EXPECT_EQ(0, tree.indexOfAttribute(nullptr, 0, "attr", StringPiece16("attr").size()))
        # ASSERT_EQ(tree.next(), android::ResXMLTree::START_TAG)
        # ASSERT_EQ(tree.getElementNamespace(&len), nullptr)
        # tagName = tree.getElementName(&len)
        # EXPECT_EQ(StringPiece16(tagName, len), "Layout")
        # ASSERT_EQ(1u, tree.getAttributeCount())
        # const char16_t* attrNamespace = tree.getAttributeNamespace(0, &len)
        # EXPECT_EQ(StringPiece16(attrNamespace, len), "http://com.test")
        # attrName = tree.getAttributeName(0, &len)
        # EXPECT_EQ(StringPiece16(attrName, len), "hello")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::END_TAG)
        # ASSERT_EQ(tree.next(), android::ResXMLTree::START_TAG)
        # ASSERT_EQ(tree.getElementNamespace(&len), nullptr)
        # tagName = tree.getElementName(&len)
        # EXPECT_EQ(StringPiece16(tagName, len), "Layout")
        # ASSERT_EQ(0u, tree.getAttributeCount())
        # ASSERT_EQ(tree.next(), android::ResXMLTree::TEXT)
        # const char16_t* text = tree.getText(&len)
        # EXPECT_EQ(StringPiece16(text, len), "Some text")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::END_TAG)
        # ASSERT_EQ(tree.getElementNamespace(&len), nullptr)
        # tagName = tree.getElementName(&len)
        # EXPECT_EQ(StringPiece16(tagName, len), "Layout")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::END_TAG)
        # ASSERT_EQ(tree.getElementNamespace(&len), nullptr)
        # tagName = tree.getElementName(&len)
        # EXPECT_EQ(StringPiece16(tagName, len), "View")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::END_NAMESPACE)
        # namespacePrefix = tree.getNamespacePrefix(&len)
        # EXPECT_EQ(StringPiece16(namespacePrefix, len), "test")
        # namespaceUri = tree.getNamespaceUri(&len)
        # ASSERT_EQ(StringPiece16(namespaceUri, len), "http://com.test")
        # ASSERT_EQ(tree.next(), android::ResXMLTree::END_DOCUMENT)

    def test_FlattenCompiledXmlAndStripSdk21(self):
        doc = buildXmlDom(
            '<View xmlns:android="http://schemas.android.com/apk/res/android" '
            'android:paddingStart="1dp" '
            'android:colorAccent="#ffffff"/>'
        )
        buffer = BigBuffer(1024)
        # linker = XmlReferenceLinker()
        xmlParser = factory.newPullParser()
        options = XmlFlattenerOptions(False, 17)
        # options.maxSdkLevel = 17
        assert self.flatten(buffer, doc, xmlParser, options, linker=None)

        self.dumpXmlTree(buffer)

        # assert linker.getSdkLevels().count(17) == 1
        # assert linker.getSdkLevels().count(21) == 1
        # while tree.next() != XmlPullParser.START_TAG:
        #     assert tree.getEventType() != BAD_DOCUMENT
        #     assert tree.getEventType() != END_DOCUMENT
        # assert tree.getAttributeCount() == 1
        # assert tree.getAttributeNameResID(0) == 0x010103b3

    def test_AssignSpecialAttributeIndices(self):
        doc = buildXmlDom(
                '<View xmlns:android="http://schemas.android.com/apk/res/android" '
                'android:id="@id/id" '
                'class="str" '
                'style="@id/id"/>'
        )
        buffer = BigBuffer(1024)
        xmlParser = factory.newPullParser()
        assert self.flatten(buffer, doc, xmlParser)

        self.dumpXmlTree(buffer)
        # while tree.next() != XmlPullParser.START_TAG:
        #     assert tree.getEventType() != BAD_DOCUMENT
        #     assert tree.getEventType() != END_DOCUMENT
        # assert tree.indexOfClass() == 0
        # assert tree.indexOfStyle() == 1

    #
    #  The device ResXMLParser in libandroidfw differentiates between empty namespace and null
    #  namespace.
    #
    def test_NoNamespaceIsNotTheSameAsEmptyNamespace(self):
        doc = buildXmlDom("<View package=\"android\"/>")
        buffer = BigBuffer(1024)
        xmlParser = factory.newPullParser()
        assert self.flatten(buffer, doc, xmlParser)

        self.dumpXmlTree(buffer)
        # while tree.next() != XmlPullParser.START_TAG:
        #     assert tree.getEventType() != BAD_DOCUMENT
        #     assert tree.getEventType() != END_DOCUMENT
        # kPackage = "package"
        # assert tree.indexOfAttribute(None, 0, kPackage, len(kPackage)) >= 0

if __name__ == '__main__':
    dmy = XmlFlattenerTest()
    dmy.setup_class()
    dmy.test_FlattenCompiledXmlAndStripSdk21()