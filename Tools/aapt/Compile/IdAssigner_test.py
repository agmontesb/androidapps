# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/compile/IdAssigner_Builders.cpp
#
from Tools.aapt.Compile.IdAssigner import IdAssigner
from Tools.aapt.Resource import ResourceId
from Tools.aapt.test import Builders
from Tools.aapt.test import Context



def test_AssignIds():
    table = Builders.ResourceTableBuilder()\
        .addSimple("@android:attr/foo")\
        .addSimple("@android:attr/bar")\
        .addSimple("@android:id/foo")\
        .setPackageId("android", 0x01)\
        .build()
    context = Context.ContextBuilder().build()
    assigner = IdAssigner()
    assert assigner.consume(context, table)
    assert verifyIds(table)

def test_AssignIdsWithReservedIds():
    table = Builders.ResourceTableBuilder()\
        .addSimple("@android:attr/foo", ResourceId(0x01040006))\
        .addSimple("@android:attr/bar")\
        .addSimple("@android:id/foo")\
        .addSimple("@app:id/biz")\
        .setPackageId("android", 0x01)\
        .setPackageId("app", 0x7f)\
        .build()
    context = Context.ContextBuilder().build()
    assigner = IdAssigner()
    assert assigner.consume(context, table)
    assert verifyIds(table)

def test_FailWhenNonUniqueIdsAssigned():
    table = Builders.ResourceTableBuilder()\
        .addSimple("@android:attr/foo", ResourceId(0x01040006))\
        .addSimple("@android:attr/bar", ResourceId(0x01040006))\
        .setPackageId("android", 0x01)\
        .setPackageId("app", 0x7f)\
        .build()
    context = Context.ContextBuilder().build()
    assigner = IdAssigner()
    assert not assigner.consume(context, table)
    pass

def verifyIds(table):
    for package in table.packages:
        packageIds = set()
        if not package.id:
            return False    # << "package " << package.name << " has no ID"
        if package.id in packageIds:
            return False    #  << "package " << package.name << " has non-unique ID " << std.hex << (int) package.id << std.dec
        packageIds.add(package.id)
    for package in table.packages:
        typeIds = set()
        for atype in package.types:
            if not atype.id:
                return False    #  << "type " << type.type << " of package " << package.name << " has no ID"
            if atype.id in typeIds:
                return False    # << "type " << type.type << " of package " << package.name << " has non-unique ID "<< std.hex << (int) type.id << std.dec
            typeIds.add(atype.id)
        for atype in package.types:
            entryIds = set()
            for entry in atype.entries:
                if entry.id is None:
                    return False    # << "entry " << entry.name << " of type " << type.type << " of package " << package.name << " has no ID"
                if entry.id in entryIds:
                    return False    # << "entry " << entry.name << " of type " << type.type << " of package " << package.name << " has non-unique ID " << std.hex << (int) entry.id << std.dec
                entryIds.add(entry.id)
    return True # << "all IDs are unique and assigned"