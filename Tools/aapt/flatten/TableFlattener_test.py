# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/flatten/TableFlattener_test.cpp
#
import Tools.aapt.test.Context as cntx
from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.Resource import ResourceName, ResourceId
from Tools.aapt.ResourcesTypes import Res_value, ResTable_config
from Tools.aapt.ResourcesValues import BinaryPrimitive, RawString
from Tools.aapt.flatten.TableFlattener import TableFlattenerOptions, TableFlattener
from Tools.aapt.test.Common import parseNameOrDie, parseConfigOrDie, getValue
from Tools.aapt.test.Builders import ResourceTableBuilder, buildReference, StyleBuilder
from Tools.aapt.unflatten.BinaryResourceParser import BinaryResourceParser


class TableFlattenerTest(object):

    mContext = None

    @classmethod
    def setup_class(cls):
        cls.mContext = cntx.ContextBuilder() \
        .setCompilationPackage(u"com.app.test") \
        .setPackageId(0x7f) \
        .build()

    def flattenToResTable(self, table, resTable):
        buffer = BigBuffer(1024)
        options = TableFlattenerOptions()
        options.useExtendedChunks = True
        flattener = TableFlattener(buffer, options)
        if not flattener.consume(self.mContext, table):
            return False    # "failed to flatten ResourceTable"

        if resTable.add(buffer, buffer.size(), -1, True):
            return False    # "flattened ResTable is corrupt"
        return True

    def flattenToResourceTable(self, table, resourceTable):
        buffer = BigBuffer(1024)
        options = TableFlattenerOptions()
        options.useExtendedChunks = True
        flattener = TableFlattener(buffer, options)
        if not flattener.consume(self.mContext, table):
            return False    # "failed to flatten ResourceTable"

        parser = BinaryResourceParser(self.mContext, resourceTable, None, buffer, buffer.size())
        if not parser.parse():
            return False    # "flattened ResTable is corrupt"
        return True

    def exists(self, table, expectedName, expectedId, expectedConfig, expectedDataType,
               expectedData, expectedSpecFlags):
        expectedResName = ResourceName(parseNameOrDie(expectedName))
        table.setParameters(expectedConfig)
        config = ResTable_config()
        val = Res_value()
        specFlags = 0
        if table.getResource(expectedId.id, val, False, 0, specFlags, config) < 0:
            return False    # "could not find resource with"
        
        if expectedDataType != val.dataType:
            return  False    # "expected data type "
                    # << std.hex << (int) expectedDataType << " but got data type "
                    # << (int) val.dataType << std.dec << " instead"
        
        if expectedData != val.data:
            return False    # "expected data "
                    # << std.hex << expectedData << " but got data "
                    # << val.data << std.dec << " instead"

        if expectedSpecFlags != specFlags:
            return  False    # "expected specFlags "
                    # << std.hex << expectedSpecFlags << " but got specFlags "
                    # << specFlags << std.dec << " instead"

        actualName = ResTable.resource_name
        if not table.getResourceName(expectedId.id, False, actualName):
            return False    # "failed to find resource name"

        package16 = StringPiece16(actualName.package, actualName.packageLen)
        if package16 != expectedResName.package:
            return  False    # "expected package '" << expectedResName.package << "' but got '"
                    # << package16 << "'"

        type16 = StringPiece16(actualName.type, actualName.typeLen)
        if type16 != toString(expectedResName.type):
            return False    # "expected type '" << expectedResName.type
                    # << "' but got '" << type16 << "'"

        name16 = StringPiece16(actualName.name, actualName.nameLen)
        if name16 != expectedResName.entry:
            return False    # "expected name '" << expectedResName.entry
                    # << "' but got '" << name16 << "'"

        if expectedConfig != config:
            return False    # "expected config '" << expectedConfig << "' but got '"
                    # << ConfigDescription(config) << "'"

        return True


    def test_FlattenFullyLinkedTable(self):
        table = ResourceTableBuilder() \
            .setPackageId(
                u"com.app.test", 0x7f
            ).addSimple(
                u"@com.app.test:id/one",
                ResourceId(0x7f020000)
            ).addSimple(
                u"@com.app.test:id/two",
                ResourceId(0x7f020001),
            ).addValue(
                u"@com.app.test:id/three", \
                ResourceId(0x7f020002), \
                buildReference(u"@com.app.test:id/one", ResourceId(0x7f020000))
            ).addValue(
                u"@com.app.test:integer/one",
                ResourceId(0x7f030000),
                BinaryPrimitive(Res_value.TYPE_INT_DEC, 1),
            ).addValue(
                u"@com.app.test:integer/one", ResourceId(0x7f030000), \
                parseConfigOrDie("v1"),
                BinaryPrimitive(Res_value.TYPE_INT_DEC, 2)
            ).addString(
                u"@com.app.test:string/test",
                ResourceId(0x7f040000), u"foo"
            ).addString(
                u"@com.app.test:layout/bar",
                ResourceId(0x7f050000),
                u"res/layout/bar.xml"
            ).build()
        resTable = ResTable()
        assert self.flatten(table, resTable)
        assert self.exists(resTable, u"@com.app.test:id/one", ResourceId(0x7f020000), None,
                      Res_value.TYPE_INT_BOOLEAN, 0, 0)
        assert self.exists(resTable, u"@com.app.test:id/two", ResourceId(0x7f020001), None,
                      Res_value.TYPE_INT_BOOLEAN, 0, 0)
        assert self.exists(resTable, u"@com.app.test:id/three", ResourceId(0x7f020002), None,
                      Res_value.TYPE_REFERENCE, 0x7f020000, 0)
        assert self.exists(resTable, u"@com.app.test:integer/one", ResourceId(0x7f030000),
                      None, Res_value.TYPE_INT_DEC, 1, ResTable_config.CONFIG_VERSION)
        assert self.exists(resTable, u"@com.app.test:integer/one", ResourceId(0x7f030000),
                      parseConfigOrDie("v1"), Res_value.TYPE_INT_DEC, 2,
                      ResTable_config.CONFIG_VERSION)
        fooStr = u"foo"
        idx = resTable.getTableStringBlock(0).indexOfString(fooStr.data(), fooStr.size())
        assert idx >= 0
        assert self.exists(resTable, u"@com.app.test:string/test", ResourceId(0x7f040000),
                      None, Res_value.TYPE_STRING, idx, 0)
        barPath = u"res/layout/bar.xml"
        idx = resTable.getTableStringBlock(0).indexOfString(barPath.data(), barPath.size())
        assert idx >= 0
        assert self.exists(resTable, u"@com.app.test:layout/bar", ResourceId(0x7f050000), None,
                      Res_value.TYPE_STRING, idx, 0)
    
    def test_FlattenEntriesWithGapsInIds(self):
        table = ResourceTableBuilder() \
            .setPackageId(u"com.app.test", 0x7f) \
            .addSimple(u"@com.app.test:id/one", ResourceId(0x7f020001)) \
            .addSimple(u"@com.app.test:id/three", ResourceId(0x7f020003)) \
            .build()
        resTable = ResTable()
        assert self.flatten(table, resTable)
        assert self.exists(resTable, u"@com.app.test:id/one", ResourceId(0x7f020001), None,
                      Res_value.TYPE_INT_BOOLEAN, 0, 0)
        assert self.exists(resTable, u"@com.app.test:id/three", ResourceId(0x7f020003), None,
                      Res_value.TYPE_INT_BOOLEAN, 0, 0)
    
    def tes_FlattenUnlinkedTable(self):
        table = ResourceTableBuilder() \
            .setPackageId(u"com.app.test", 0x7f) \
            .addValue(u"@com.app.test:integer/one", ResourceId(0x7f020000), \
                      buildReference(u"@android:integer/foo")) \
            .addValue(u"@com.app.test:style/Theme", ResourceId(0x7f030000), StyleBuilder() \
                      .setParent(u"@android:style/Theme.Material") \
                      .addItem(u"@android:attr/background", None) \
                      .addItem(u"@android:attr/colorAccent", \
                               buildReference(u"@com.app.test:color/green")) \
                      .build()) \
            .build()
        
        #  Need access to stringPool to make RawString.
        style = getValue(table, u"@com.app.test:style/Theme")
        style.entries[0].value = RawString(table.stringPool.makeRef(u"foo"))
        
        finalTable = ResourceTable()
        assert self.flatten(table, finalTable)
        ref = getValue(finalTable, u"@com.app.test:integer/one")
        assert ref
        assert ref.name
        assert ref.name == parseNameOrDie(u"@android:integer/foo")
        style = getValue(finalTable, u"@com.app.test:style/Theme")
        assert style
        assert style.parent
        assert style.parent.name
        assert style.parent.name == parseNameOrDie(u"@android:style/Theme.Material")
        assert len(style.entries) == 2
        assert style.entries[0].key.name
        assert style.entries[0].key.name == parseNameOrDie(u"@android:attr/background")
        raw = style.entries[0].value
        assert raw
        assert raw.value.__pointee__() == u"foo"
        assert style.entries[1].key.name
        assert style.entries[1].key.name == parseNameOrDie(u"@android:attr/colorAccent")
        ref = style.entries[1].value
        assert ref
        assert ref.name
        assert ref.name == parseNameOrDie(u"@com.app.test:color/green")