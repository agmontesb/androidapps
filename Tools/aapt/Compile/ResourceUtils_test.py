# -*- coding: utf-8 -*-

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Compile.ResourceUtils import ObjRef, tryParseReferenceB
from Tools.aapt.Resource import ResourceNameRef, ResourceType, ResourceName


def test_ParseReferenceWithNoPackage():
    expected = ResourceNameRef('', ResourceType.kColor, "foo")
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("@color/foo", actual, create, priv)
    assert bFlag
    assert expected == actual
    assert not create._value
    assert not priv._value

def test_ParseReferenceWithPackage():
    expected = ResourceNameRef("android", ResourceType.kColor, "foo")
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("@android:color/foo", actual, create, priv)
    assert bFlag
    assert expected == actual
    assert not create._value
    assert not priv._value

def test_ParseReferenceWithSurroundingWhitespace():
    expected = ResourceNameRef("android", ResourceType.kColor, "foo")
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("\t @android:color/foo\n \n\t", actual, create, priv)
    assert bFlag
    assert expected == actual
    assert not create._value
    assert not priv._value

def test_ParseAutoCreateIdReference():
    expected = ResourceNameRef("android", ResourceType.kId, "foo")
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("@+android:id/foo", actual, create, priv)
    assert bFlag
    assert expected == actual
    assert create._value
    assert not priv._value

def test_ParsePrivateReference():
    expected = ResourceNameRef("android", ResourceType.kId, "foo")
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("@*android:id/foo", actual, create, priv)
    assert bFlag
    assert expected == actual
    assert not create._value
    assert priv._value

def test_FailToParseAutoCreateNonIdReference():
    actual = ResourceNameRef()
    create = ObjRef(False)
    priv = ObjRef(False)
    bFlag = tryParseReferenceB("@+android:color/foo", actual, create, priv)
    assert not bFlag

def test_ParseStyleParentReference():
    kAndroidStyleFooName = ResourceName("android", ResourceType.kStyle, "foo")
    kStyleFooName = ResourceName('', ResourceType.kStyle, "foo")
    errStr = ObjRef('')
    ref = ResourceUtils.parseStyleParentReference("@android:style/foo", errStr)
    assert ref
    assert ref.name == kAndroidStyleFooName
    ref = ResourceUtils.parseStyleParentReference("@style/foo", errStr)
    assert ref
    assert ref.name == kStyleFooName
    ref = ResourceUtils.parseStyleParentReference("?android:style/foo", errStr)
    assert ref
    assert ref.name == kAndroidStyleFooName
    ref = ResourceUtils.parseStyleParentReference("?style/foo", errStr)
    assert ref
    assert ref.name == kStyleFooName
    ref = ResourceUtils.parseStyleParentReference("android:style/foo", errStr)
    assert ref
    assert ref.name == kAndroidStyleFooName
    ref = ResourceUtils.parseStyleParentReference("android:foo", errStr)
    assert ref
    assert ref.name == kAndroidStyleFooName
    ref = ResourceUtils.parseStyleParentReference("foo", errStr)
    assert ref
    assert ref.name == kStyleFooName