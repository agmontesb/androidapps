# -*- coding: utf-8 -*-
''''''
import pytest

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.ConfigDescription import ConfigDescription
from Tools.aapt.Resource import ResourceNameRef, ResourceType
from Tools.aapt import ResourcesTypes, ResourcesValues
from Tools.aapt.test import Common

mDiagnostics = ResourceUtils.Diagnostics()

def test_FailToAddResourceWithBadName():
    table = ResourceTable()
    assert not table.addResource(
        ResourceNameRef("android", ResourceType.kId, "hey,there"),
        None, "test.xml:21", ResourcesValues.Id(), diag=mDiagnostics
    )

def test_AddOneResource():
    table = ResourceTable()
    assert table.addResource(
        Common.parseNameOrDie("@android:attr/id"),
        None, "test.xml:23", ResourcesValues.Id()
    )
    assert Common.getValue(table, "@android:attr/id")

def test_AddMultipleResources():
    table = ResourceTable()
    config = ConfigDescription()
    languageConfig = ConfigDescription()
    languageConfig.language = "pl"
    assert table.addResource(
        Common.parseNameOrDie("@android:attr/layout_width"),
        config, "test/path/file.xml:10",
        ResourcesValues.Id())
    assert table.addResource(
        Common.parseNameOrDie("@android:attr/id"),
        config, "test/path/file.xml:12",
        ResourcesValues.Id())
    assert table.addResource(
        Common.parseNameOrDie("@android:string/ok"),
        config, "test/path/file.xml14",
        ResourcesValues.Id())
    assert table.addResource(
        Common.parseNameOrDie("@android:string/ok"),
        languageConfig, "test/path/file.xml:20",
        ResourcesValues.BinaryPrimitive(ResourcesTypes.Res_value()))
        
    assert Common.getValue(table, "@android:attr/layout_width")
    assert Common.getValue(table, "@android:attr/id")
    assert Common.getValue(table, "@android:string/ok")
    assert Common.getValueForConfig(table, "@android:string/ok", languageConfig)

def test_OverrideWeakResourceValue():
    table = ResourceTable()
    assert table.addResource(
        Common.parseNameOrDie("@android:attr/foo"), None, '',
        ResourcesValues.Attribute(True))
    attr = Common.getValue(table, "@android:attr/foo")
    assert attr
    assert attr.isWeak()
    assert table.addResource(
        Common.parseNameOrDie("@android:attr/foo"), None, None,
        ResourcesValues.Attribute(False))
    attr = Common.getValue(table, "@android:attr/foo");
    assert attr
    assert not attr.isWeak()
