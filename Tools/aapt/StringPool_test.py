# -*- coding: utf-8 -*-
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/StringPool_test.cpp
#
import pytest
import io

import Tools.aapt.ResourcesTypes as rt
from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.StringPool import StringPool, StyleString, Span, pointee

@pytest.fixture
def pool():
    return StringPool()

def test_InsertOneString(pool):
    ref = pool.makeRef(u"wut")
    assert pointee(ref) == u"wut"

def test_InsertTwoUniqueStrings(pool):
    ref = pool.makeRef(u"wut")
    ref2 = pool.makeRef(u"hey")
    assert pointee(ref) == u"wut"
    assert pointee(ref2) == u"hey"

def test_DoNotInsertNewDuplicateString(pool):
    ref = pool.makeRef(u"wut")
    ref2 = pool.makeRef(u"wut")
    assert pointee(ref) == u"wut"
    assert pointee(ref2) == u"wut"
    assert pool.size() == 1

def test_MaintainInsertionOrderIndex(pool):
    ref = pool.makeRef(u"z")
    ref1 = pool.makeRef(u"a")
    ref2 = pool.makeRef(u"m")

    assert ref.getIndex() == 0
    assert ref1.getIndex() == 1
    assert ref2.getIndex() == 2

def test_PruneStringsWithNoReferences(pool):
    def dmyFcn(pool):
        ref = pool.makeRef(u"wut")
        assert pointee(ref) == u"wut"
        assert pool.size() == 2

    refA = pool.makeRef(u"foo")
    dmyFcn(pool)
    refB = pool.makeRef(u"bar")
    assert pool.size() == 3
    pool.prune()
    assert pool.size() == 2
    it = iter(pool)
    e = it.next()
    assert e.value == u"foo"
    assert e.index < 2
    e = it.next()
    assert e.value == u"bar"
    assert e.index < 2

def test_SortAndMaintainIndexesInReferences(pool):
    ref = pool.makeRef(u"z")
    ref2 = pool.makeRef(StyleString(u"a", []))
    ref3 = pool.makeRef(u"m")

    assert pointee(ref) == u"z"
    assert ref.getIndex() == 0

    assert pointee(ref2.str) == u"a"
    assert ref2.getIndex() == 1

    assert pointee(ref3) == u"m"
    assert ref3.getIndex() == 2

    pool.sort(lambda a, b: cmp(a.value, b.value))

    assert pointee(ref) == u"z"
    assert ref.getIndex() == 2

    assert pointee(ref2.str) == u"a"
    assert ref2.getIndex() == 0

    assert pointee(ref3) == u"m"
    assert ref3.getIndex() == 1

def test_SortAndStillDedupe(pool):
    ref = pool.makeRef(u"z")
    ref2 = pool.makeRef(u"a")
    ref3 = pool.makeRef(u"m")

    pool.sort(lambda a, b: cmp(a.value, b.value))

    ref4 = pool.makeRef(u"z")
    ref5 = pool.makeRef(u"a")
    ref6 = pool.makeRef(u"m")

    assert ref4.getIndex() == ref.getIndex()
    assert ref5.getIndex() == ref2.getIndex()
    assert ref6.getIndex() == ref3.getIndex()

def test_AddStyles(pool):
    str = StyleString(
        u"android",
        [
            Span(u"b", 2, 6),
        ]
    )

    ref = pool.makeRef(str)

    assert ref.getIndex() == 0
    assert pointee(ref.str) == u"android"
    assert len(ref.spans) == 1

    span = ref.spans[0]
    assert pointee(span.name) == u"b"
    assert span.firstChar == 2
    assert span.lastChar == 6

def test_DoNotDedupeStyleWithSameStringAsNonStyle(pool):
    ref = pool.makeRef(u"android")
    styleRef = pool.makeRef(StyleString(u"android", []))

    assert ref.getIndex() != styleRef.getIndex()

def test_FlattenEmptyStringPoolUtf8(pool):
    buffer = BigBuffer(1024)
    StringPool.flattenUtf8(pool, buffer)
    buffer = io.BytesIO(reduce(lambda t, x: t + x, buffer, bytearray()))
    test = rt.ResStringPool(buffer)

def test_FlattenUtf8(pool):
    sLongString = u"バッテリーを長持ちさせるため、バッテリーセーバーは端末のパフォーマンスを抑え、バイブレーション、位置情報サービス、大半のバックグラウンドデータを制限します。メール、SMSや、同期を使 用するその他のアプリは、起動しても更新されないことがあります。バッテリーセーバーは端末の充電中は自動的にOFFになります。"

    ref1 = pool.makeRef(u"hello")
    ref2 = pool.makeRef(u"goodbye")
    ref3 = pool.makeRef(sLongString)
    ref4 = pool.makeRef(StyleString(u"style", [Span(u"b", 0, 1), Span(u"i", 2, 3 )]))

    assert ref1.getIndex() == 0
    assert ref2.getIndex() == 1
    assert ref3.getIndex() == 2
    assert ref4.getIndex() == 3

    # buffer = io.BytesIO()
    buffer = BigBuffer(1024)
    StringPool.flattenUtf8(pool, buffer)
    buffer = io.BytesIO(reduce(lambda t, x: t + x, buffer, bytearray()))
    test = rt.ResStringPool(buffer)

    assert test.stringAt(0) == u"hello"
    assert test.stringAt(1) == u"goodbye"
    assert test.stringAt(2) == sLongString
    assert test.stringAt(3) == u"style"

    spans = test.styleAt(3)
    assert spans is not None
    span = spans[0]
    assert test.stringAt(span.name.index) == u"b"
    assert span.firstChar == 0
    assert span.lastChar == 1

    span = spans[1]
    assert span.name.index != rt.ResStringPool_span.END
    assert test.stringAt(span.name.index) == u"i"
    assert span.firstChar == 2
    assert span.lastChar == 3

    span = spans[2]
    assert span.name.index == rt.ResStringPool_span.END




