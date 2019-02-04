# -*- coding: utf-8 -*-
import pytest
import itertools
from operator import methodcaller as mcall

from Android.java.Locale import Locale
from Android.java.LanguageTag import LanguageTag
from Android.java.LocaleMatcher import LocaleMatcher


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

def test_languagetag():
    langtag, status = LanguageTag.parse('de')             # Simple language
    assert langtag.getLanguage() == 'de'
    langtag, status = LanguageTag.parse('i-enochian')     # grandfathered tag
    assert not langtag.getLanguage() and langtag.getPrivateuse() == 'x-i-enochian'
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

def test_localematcher():
    locRngStr = ["zh", "zh-CN", "en", "zh-TW", "zh-HK"]
    locRngWgh = [0.9, 0.8, 0.7, 0.6, 0.5]
    priorityList = itertools.imap(Locale.LanguageRange, locRngStr, locRngWgh)
    amap = {"zh": ["zh", "zh-Hans"],
           "zh-HK": ["zh-HK"],
           "zh-TW": ["zh-TW"]}
    reqRngStr = ["zh", "zh-hans", "zh-cn", "zh-hans-cn", "en", "zh-tw", "zh-hk"]
    reqRngWgh = [0.9, 0.9, 0.8, 0.8, 0.7, 0.6, 0.5]
    answ = LocaleMatcher.mapEquivalents(priorityList, amap)
    assert map(lambda x: x.getRange(), answ) == reqRngStr
    assert map(lambda x: x.getWeight(), answ) == reqRngWgh

    ranges1 = "Accept-Language: ja,en;q=0.4"
    pList1 = LocaleMatcher.parse(ranges1)
    ranges2 = "ja,en;q=0.4"
    pList2 = LocaleMatcher.parse(ranges2)
    assert pList1 == pList2
    ranges = "ja,en"
    pList = LocaleMatcher.parse(ranges)
    assert map(lambda x: x.getRange(), pList) == ['ja', 'en']
    assert map(lambda x: x.getWeight(), pList) == [1.0, 1.0]
    ranges = "Accept-Language: iw,en-us;q=0.7,en;q=0.3"
    pList = LocaleMatcher.parse(ranges)
    assert map(lambda x: x.getRange(), pList) == ['iw', 'he', 'en-us', 'en']
    assert map(lambda x: x.getWeight(), pList) == [1.0, 1.0, 0.7, 0.3]

    ranges = "zh-hant-tw, en-us"
    priorityList = LocaleMatcher.parse(ranges)
    tags = ['zh-Hant-TW', 'zh-Hant', 'zh', 'en-US', 'en']
    answ = LocaleMatcher.lookupTag(priorityList, tags)
    assert answ == 'zh-Hant-TW'
    pass


def test_from_languagetag_to_locale():
    loc = Locale.forLanguageTag('zh-CN-a-myext-x-private')
    assert loc.getLanguage() == 'zh' and loc.getCountry() == 'CN'
    assert loc.hasExtensions()
    assert loc.getExtensionKeys() == set(['a', 'x'])
    assert map(loc.getExtension, sorted(loc.getExtensionKeys())) == ['myext', 'private']

    loc = Locale.forLanguageTag("en-US-x-lvariant-POSIX")
    assert loc.getVariant() == "POSIX"
    assert not loc.getExtension('x')

    loc = Locale.forLanguageTag("de-POSIX-x-URP-lvariant-Abc-Def")
    assert loc.getVariant() == "posix_Abc_Def"
    assert loc.getExtension('x') == "urp"

def test_toLanguageTag():
    loc = Locale('')
    assert loc.toLanguageTag() == 'und'
    loc = Locale('e2')
    assert loc.toLanguageTag() == 'und'
    loc = Locale('en', 'd12')
    assert loc.toLanguageTag() == 'en'
    loc = Locale('en', 'US', 'WIN')
    assert loc.toLanguageTag() == 'en-US-x-lvariant-WIN'
    loc = Locale('en', 'US', 'Oracle_JDK_Standard_Edition')
    assert loc.toLanguageTag() == 'en-US-oracle-x-lvariant-JDK-Standard-Edition'
    loc = Locale('en', 'US', 'Solaris_isjustthecoolestthing')
    assert loc.toLanguageTag() == 'en-US-x-lvariant-Solaris'
    locs = map(Locale, ('iw', 'ji', 'in'))
    assert map(mcall('toLanguageTag'), locs) == ['he', 'yi', 'id']
    loc = Locale('no', 'NO', 'NY')
    assert loc.toLanguageTag() == 'nn-NO'
    loc = Locale('en', 'Us', 'abcde_fghij_1key_lmnop_WIN')
    assert loc.toLanguageTag() == 'en-US-abcde-fghij-1key-lmnop-x-lvariant-WIN'

def test_builder():
    builder = Locale.Builder()
    loc = Locale('en', 'Us', 'AbCdE_fghIJ_1key_lmnop')
    builder.setLocale(loc)
    aloc = builder.build()
    assert aloc.getLanguage() == 'en'
    assert aloc.getCountry() == 'US'
    assert aloc.getVariant() == 'abcde_fghij_1key_lmnop'

    builder.clear()
    ltag = 'en-US-abcde-fghij-1key-lmnop-x-lvariant-WIN'
    builder.setLanguageTag(ltag)
    aloc = builder.build()
    assert aloc.getLanguage() == 'en'
    assert aloc.getCountry() == 'US'
    assert aloc.getVariant() == 'abcde_fghij_1key_lmnop_WIN'
    assert aloc.toLanguageTag() == 'en-US-abcde-fghij-1key-lmnop-x-lvariant-WIN'

def test_getters():
    loc1 = Locale('es', 'co', 'costa')
    assert loc1.getLanguage() == 'es', 'Locale: getLanguage error'
    assert loc1.getScript() == '', 'Locale: getScript error'
    assert loc1.getCountry() == 'CO', 'Locale: getCountry error'
    assert loc1.getVariant() == 'costa', 'Locale: getVariant error'

    loc2 = Locale.forLanguageTag('en-US-abcde-fghij-1key-lmnop-x-POSIX-lvariant-WIN')
    assert loc2.toString() == 'en_US_abcde_fghij_1key_lmnop_WIN_#x_posix'
    dflt = loc2.getDefault()


