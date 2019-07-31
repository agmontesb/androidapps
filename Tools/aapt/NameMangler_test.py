# -*- coding: utf-8 -*-
from Tools.aapt.NameMangler import NameMangler

def test_MangleName():
    package = "android.appcompat"
    name = "Platform.AppCompat"
    assert NameMangler.mangle(package, name) == "android.appcompat$Platform.AppCompat"
    assert NameMangler.unmangle(name) == (package, name)

def test_IgnoreUnmangledName():
    name = "foo_bar"
    assert not NameMangler.unmangle(name)