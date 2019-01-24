# -*- coding: utf-8 -*-
import pytest

from Android.java.Locale import Locale
from Android.java.LanguageTag import LanguageTag


def test_localekey():
    LocaleKey = Locale.LocaleKey
    key1 = LocaleKey('lAnGuAge', 'sCrIpt', 'ReGiOn', 'variANT')
    key2 = LocaleKey('lAnGuAge', 'sCrIpt', 'ReGiOn', 'variANT')
    assert key1 == key2, 'LocaleKey: equality ERROR'
    key3 = LocaleKey.normalize(key1)
    assert key3.lang == 'language', 'LocaleKey: normalize error'
    assert key3.scrt == 'Script', 'LocaleKey: normalize error'
    assert key3.regn == 'REGION', 'LocaleKey: normalize error'
    assert key3.vart == 'variANT', 'LocaleKey: normalize error'
    map = {}
    map[key1] = 1
    map[key3] = 3
    assert len(map) == 2, 'LocaleKey: map key error'
    assert map[key1] == map[key2], 'LocaleKey: map key error'

def test_localetag():
    langtag, status = LanguageTag.parse('de')             # Simple language
    assert langtag.language == 'de'
    langtag, status = LanguageTag.parse('i-enochian')     # grandfathered tag
    assert not langtag.language and langtag.privateuse == 'x-i-enochian'
    langtag, status = LanguageTag.parse('zh-Hant')        # Language subtag plus Script
    assert langtag.language == 'zh' and langtag.script == 'Hant'
    langtag, status = LanguageTag.parse('zh-cmn-Hans-CN')
    assert langtag.language == 'zh' and langtag.script == 'Hans'
    assert langtag.extlangs == ['cmn'] and langtag.region == 'CN'
    langtag, status = LanguageTag.parse('sl-rozaj')
    assert langtag.language == 'sl' and langtag.variants == ['rozaj']
    langtag, status = LanguageTag.parse('zh-CN-a-myext-x-private')
    assert langtag.language == 'zh' and langtag.extensions == ['a-myext']
    assert langtag.region == 'CN' and langtag.privateuse == 'x-private'
    langtag, status = LanguageTag.parse('en-a-myext-b-another')
    assert langtag.language == 'en' and langtag.extensions == ['a-myext', 'b-another']
    # Tags with errors
    langtag, status = LanguageTag.parse('de-419-DE')  # two region tags
    assert status == 'Region has 2 tags'
    langtag, status = LanguageTag.parse('a-DE')       # single char subtag in priary pos.
    assert status == 'Invalid subtag: a'
    langtag, status = LanguageTag.parse('ar-a-aaa-b-bbb-a-ccc')  # two extensions with same single-letter
    assert status == 'two extensions with "a" single-letter'

def test_getters():
    loc1 = Locale('es', 'co', 'costa')
    assert loc1.getLanguage() == 'es', 'Locale: getLanguage error'
    assert loc1.getScript() == '', 'Locale: getScript error'
    assert loc1.getCountry() == 'CO', 'Locale: getCountry error'
    assert loc1.getVariant() == 'costa', 'Locale: getVariant error'