# -*- coding: utf-8 -*-
'''
ported from:
https://android.googlesource.com/platform/frameworks/base/+/4afa0352d6c1046f9e9b67fbf0011bcd751fcbb5/core/tests/coretests/src/android/net/UriTest.java
'''
import pytest

from Android.Os.Parcel import Parcel
from Android.Uri import Uri
Builder = Uri.Builder

def assertEquals(x, y):
    assert x == y

def assertNotNull(x):
    assert x is not None
    
def assertNull(x):
    assert x is None
    
def assertTrue(x):
    assert bool(x)
    
def assertFalse(x):
    assert not bool(x)

def test_ToStringWithPathOnly():
    builder = Builder()
    builder.path('//foo')
    uri = builder.build()
    assert uri.toString() == '//foo'

def parcelAndUnparcel(u):
    p = Parcel()
    Uri.writeToParcel(p, u)
    p.setDataPosition(0)
    assert u == Uri.CREATOR.createFromParcel(p)

    p.setDataPosition(0)
    u = u.buildUpon().build()
    Uri.writeToParcel(p, u)
    p.setDataPosition(0)
    assert u == Uri.CREATOR.createFromParcel(p)


def test_Parceling():
    parcelAndUnparcel(Uri.parse("foo:bob%20lee"))
    parcelAndUnparcel(Uri.fromParts("foo", "bob lee", "fragment"))
    parcelAndUnparcel(
        Builder()
            .scheme("http")
            .authority("crazybob.org")
            .path("/rss/")
            .encodedQuery("a=b")
            .fragment("foo")
            .build()
    )
    
def test_BuildUponOpaqueStringUri():
    u = Uri.parse("bob:lee").buildUpon().scheme("robert").build()
    assertEquals("robert", u.getScheme())
    assertEquals("lee", u.getEncodedSchemeSpecificPart())
    assertEquals("lee", u.getSchemeSpecificPart())
    assertNull(u.getQuery())
    assertNull(u.getPath())
    assertNull(u.getAuthority())
    assertNull(u.getHost())

def test_StringUri():
    assertEquals("bob lee",
            Uri.parse("foo:bob%20lee").getSchemeSpecificPart())
    assertEquals("bob%20lee",
            Uri.parse("foo:bob%20lee").getEncodedSchemeSpecificPart())
    assertEquals("/bob%20lee",
            Uri.parse("foo:/bob%20lee").getEncodedPath())
    assertNull(Uri.parse("foo:bob%20lee").getPath())
    assertEquals("bob%20lee",
            Uri.parse("foo:?bob%20lee").getEncodedQuery())
    assertNull(Uri.parse("foo:bar#?bob%20lee").getQuery())
    assertEquals("bob%20lee",
            Uri.parse("foo:#bob%20lee").getEncodedFragment())
    
def test__StringUriIsHierarchical():
    assertTrue(Uri.parse("bob").isHierarchical())
    assertFalse(Uri.parse("bob:").isHierarchical())
    
def test_NullUriString():
    with pytest.raises(Exception) as excinfo:
        Uri.parse(None)
    assert str(excinfo.value) == "NullPointerException"

def test_NullFile():
    with pytest.raises(Exception) as excinfo:
        Uri.fromFile(None)
    assert str(excinfo.value) == "NullPointerException"

def test_CompareTo():
    a = Uri.parse("foo:a")
    b = Uri.parse("foo:b")
    b2 = Uri.parse("foo:b")
    assertTrue(a.compareTo(b) < 0)
    assertTrue(b.compareTo(a) > 0)
    assertEquals(0, b.compareTo(b2))

def test_EqualsAndHashCode():
    a = Uri.parse("http://crazybob.org/test/?foo=bar#tee")
    b = Builder()\
        .scheme("http")\
        .authority("crazybob.org")\
        .path("/test/")\
        .encodedQuery("foo=bar")\
        .fragment("tee")\
        .build()
    # Try alternate builder methods.
    c = Builder()\
        .scheme("http")\
        .encodedAuthority("crazybob.org")\
        .encodedPath("/test/")\
        .encodedQuery("foo=bar")\
        .encodedFragment("tee")\
        .build()
    assertFalse(Uri.EMPTY.equals(None))
    assertEquals(a, b)
    assertEquals(b, c)
    assertEquals(c, a)
    assertEquals(a.hashCode(), b.hashCode())
    assertEquals(b.hashCode(), c.hashCode())

def test_AuthorityParsing():
    uri = Uri.parse("http://localhost:42")
    assertEquals("localhost", uri.getHost())
    assertEquals(42, uri.getPort())
    uri = Uri.parse("http://bob@localhost:42")
    assertEquals("bob", uri.getUserInfo())
    assertEquals("localhost", uri.getHost())
    assertEquals(42, uri.getPort())
    uri = Uri.parse("http://bob%20lee@localhost:42")
    assertEquals("bob lee", uri.getUserInfo())
    assertEquals("bob%20lee", uri.getEncodedUserInfo())
    uri = Uri.parse("http://bob%40lee%3ajr@local%68ost:4%32")
    assertEquals("bob@lee:jr", uri.getUserInfo())
    assertEquals("localhost", uri.getHost())
    assertEquals(42, uri.getPort())
    uri = Uri.parse("http://localhost")
    assertEquals("localhost", uri.getHost())
    assertEquals(-1, uri.getPort())
    uri = Uri.parse("http://a:a@example.com:a@example2.com/path")
    assertEquals("a:a@example.com:a@example2.com", uri.getAuthority())
    assertEquals("example2.com", uri.getHost())
    assertEquals(-1, uri.getPort())
    
def test_BuildUponOpaqueUri():
    a = Uri.fromParts("foo", "bar", "tee")
    b = a.buildUpon().fragment("new").build()
    assertEquals("new", b.getFragment())
    assertEquals("bar", b.getSchemeSpecificPart())
    assertEquals("foo", b.getScheme())

def test_BuildUponEncodedOpaqueUri():
    a = Builder()\
        .scheme("foo")\
        .encodedOpaquePart("bar")\
        .fragment("tee")\
        .build()
    b = a.buildUpon().fragment("new").build()
    assertEquals("new", b.getFragment())
    assertEquals("bar", b.getSchemeSpecificPart())
    assertEquals("foo", b.getScheme())

def test_PathSegmentDecoding():
    uri = Uri.parse("foo://bar/a%20a/b%20b")
    assertEquals("a a", uri.getPathSegments()[0])
    assertEquals("b b", uri.getPathSegments()[1])

def test_Sms():
    base = Uri.parse("content://sms")
    appended = base.buildUpon()\
        .appendEncodedPath("conversations/addr=555-1212")\
        .build()
    assertEquals("content://sms/conversations/addr=555-1212",
            appended.toString())
    assertEquals(2, len(appended.getPathSegments()))
    assertEquals("conversations", appended.getPathSegments()[0])
    assertEquals("addr=555-1212", appended.getPathSegments()[1])

def test_EncodeWithAllowedChars():
    def indexOf(aStr, aSubStr):
        try:
            return aStr.index(aSubStr)
        except:
            return -1

    encoded = Uri.encode("Bob:/", "/")
    assertEquals(-1, indexOf(encoded, ':'))
    assertTrue(indexOf(encoded, '/') > -1)

def test_EncodeDecode():
    def code(s):
        assertEquals(s, Uri.decode(Uri.encode(s, '')))
    code(None)
    code("")
    code("Bob")
    code(":Bob")
    code("::Bob")
    code("Bob::Lee")
    code("Bob:Lee")
    code("Bob::")
    code("Bob:")
    code("::Bob::")

def test_File():
    f = "/tmp/bob"
    uri = Uri.fromFile(f)
    assertEquals("file:///tmp/bob", uri.toString())

def test_QueryParameters():
    uri = Uri.parse("content://user")
    assertEquals(None, uri.getQueryParameter("a"))
    uri = uri.buildUpon().appendQueryParameter("a", "b").build()
    assertEquals("b", uri.getQueryParameter("a"))
    uri = uri.buildUpon().appendQueryParameter("a", "b2").build()
    assertEquals(["b", "b2"], uri.getQueryParameters("a"))
    uri = uri.buildUpon().appendQueryParameter("c", "d").build()
    assertEquals(["b", "b2"], uri.getQueryParameters("a"))
    assertEquals("d", uri.getQueryParameter("c"))

def test_HostWithTrailingDot():
    uri = Uri.parse("http://google.com./b/c/g")
    assertEquals("google.com.", uri.getHost())
    assertEquals("/b/c/g", uri.getPath())

def test_SchemeOnly():
    uri = Uri.parse("empty:")
    assertEquals("empty", uri.getScheme())
    assertTrue(uri.isAbsolute())
    # assertNull(uri.getPath())

def test_EmptyPath():
    uri = Uri.parse("content://user")
    assertEquals(0, len(uri.getPathSegments()))

def test_PathOperations():
    uri = Uri.parse("content://user/a/b")
    assertEquals(2, len(uri.getPathSegments()))
    assertEquals("b", uri.getLastPathSegment())
    first = uri
    uri = uri.buildUpon().appendPath("c").build()
    assertEquals(3, len(uri.getPathSegments()))
    assertEquals("c", uri.getLastPathSegment())
    assertEquals("content://user/a/b/c", uri.toString())
    # uri = ContentUris.withAppendedId(uri, 100)
    uri = uri.buildUpon().appendPath("100").build()
    assertEquals(4, len(uri.getPathSegments()))
    assertEquals("100", uri.getLastPathSegment())
    assertEquals(100, int(uri.getLastPathSegment()))
    # assertEquals(100, ContentUris.parseId(uri))
    assertEquals("content://user/a/b/c/100", uri.toString())
    # Make sure the original URI is still intact.
    assertEquals(2, len(first.getPathSegments()))
    assertEquals("b", first.getLastPathSegment())
    with pytest.raises(IndexError) as excinfo:
        first.getPathSegments()[2]
    assert str(excinfo.value) == "list index out of range"

    assertEquals(None, Uri.EMPTY.getLastPathSegment())
    withC = Uri.parse("foo:/a/b/").buildUpon().appendPath("c").build()
    assertEquals("/a/b/c", withC.getPath())

def test_OpaqueUri():
    def testOpaqueUri(uri):
        assertEquals("mailto", uri.getScheme())
        assertEquals("nobody", uri.getSchemeSpecificPart())
        assertEquals("nobody", uri.getEncodedSchemeSpecificPart())
        assertNull(uri.getFragment())
        assertTrue(uri.isAbsolute())
        assertTrue(uri.isOpaque())
        assertFalse(uri.isRelative())
        assertFalse(uri.isHierarchical())
        assertNull(uri.getAuthority())
        assertNull(uri.getEncodedAuthority())
        assertNull(uri.getPath())
        assertNull(uri.getEncodedPath())
        assertNull(uri.getUserInfo())
        assertNull(uri.getEncodedUserInfo())
        assertNull(uri.getQuery())
        assertNull(uri.getEncodedQuery())
        assertNull(uri.getHost())
        assertEquals(-1, uri.getPort())
        assertTrue(uri.getPathSegments() == [])
        assertNull(uri.getLastPathSegment())
        assertEquals("mailto:nobody", uri.toString())
        withFragment = uri.buildUpon().fragment("top").build()
        assertEquals("mailto:nobody#top", withFragment.toString())
    uri = Uri.parse("mailto:nobody")
    testOpaqueUri(uri)
    uri = uri.buildUpon().build()
    testOpaqueUri(uri)
    uri = Uri.fromParts("mailto", "nobody", None)
    testOpaqueUri(uri)
    uri = uri.buildUpon().build()
    testOpaqueUri(uri)
    uri = Builder()\
        .scheme("mailto")\
        .opaquePart("nobody")\
        .build()
    testOpaqueUri(uri)
    uri = uri.buildUpon().build()
    testOpaqueUri(uri)

def test_HierarchicalUris():
    def compareHierarchical(uriString, ssp, uri, scheme, authority, path, query, fragment):
        assertEquals(scheme, uri.getScheme())
        assertEquals(authority, uri.getAuthority())
        assertEquals(authority, uri.getEncodedAuthority())
        assertEquals(path, uri.getPath())
        assertEquals(path, uri.getEncodedPath())
        assertEquals(query, uri.getQuery())
        assertEquals(query, uri.getEncodedQuery())
        assertEquals(fragment, uri.getFragment())
        assertEquals(fragment, uri.getEncodedFragment())
        assertEquals(ssp, uri.getSchemeSpecificPart())
        if (scheme != None):
            assertTrue(uri.isAbsolute())
            assertFalse(uri.isRelative())
        else:
            assertFalse(uri.isAbsolute())
            assertTrue(uri.isRelative())

        assertFalse(uri.isOpaque())
        assertTrue(uri.isHierarchical())
        assertEquals(uriString, uri.toString())

    def testHierarchical(scheme, authority, path, query, fragment):
        sb = ''
        if (authority != None):
            sb += "//" + authority
    
        if (path != None):
            sb += path
    
        if (query != None):
            sb += '?' + query
    
        ssp = sb
        if (scheme != None):
            sb = scheme + ":" + sb
    
        if (fragment != None):
            sb += '#' + fragment
    
        uriString = sb
        uri = Uri.parse(uriString)
        # Run these twice to test caching.
        compareHierarchical(
                uriString, ssp, uri, scheme, authority, path, query, fragment)
        compareHierarchical(
                uriString, ssp, uri, scheme, authority, path, query, fragment)
        # Test rebuilt version.
        uri = uri.buildUpon().build()
        #Run these twice to test caching.
        compareHierarchical(
                uriString, ssp, uri, scheme, authority, path, query, fragment)
        compareHierarchical(
                uriString, ssp, uri, scheme, authority, path, query, fragment)
        # The decoded and encoded versions of the inputs are all the same.
        # We'll test the actual encoding decoding separately.
        # Test building with encoded versions.
        built =Builder()\
            .scheme(scheme)\
            .encodedAuthority(authority)\
            .encodedPath(path)\
            .encodedQuery(query)\
            .encodedFragment(fragment)\
            .build()
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)
        #Test building with decoded versions.
        built = Builder()\
            .scheme(scheme)\
            .authority(authority)\
            .path(path)\
            .query(query)\
            .fragment(fragment)\
            .build()
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)
        #Rebuild.
        built = built.buildUpon().build()
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)
        compareHierarchical(
                uriString, ssp, built, scheme, authority, path, query, fragment)

    testHierarchical("http", "google.com", "/p1/p2", "query", "fragment")
    testHierarchical("file", None, "/p1/p2", None, None)
    testHierarchical("content", "contact", "/p1/p2", None, None)
    testHierarchical("http", "google.com", "/p1/p2", None, "fragment")
    testHierarchical("http", "google.com", "", None, "fragment")
    testHierarchical("http", "google.com", "", "query", "fragment")
    testHierarchical("http", "google.com", "", "query", None)
    testHierarchical("http", None, "/", "query", None)


def test_EmptyToStringNotNull():
    assertNotNull(Uri.EMPTY.toString())

def test_ParcellingWithoutFragment():
    parcelAndUnparcel(Uri.parse("foo:bob%20lee"))
    parcelAndUnparcel(Uri.fromParts("foo", "bob lee", "fragment"))
    parcelAndUnparcel(Builder()
        .scheme("http")
        .authority("crazybob.org")
        .path("/rss/")
        .encodedQuery("a=b")
        .build())

def test_GetQueryParameter():
    nestedUrl = "http://crazybob.org/?a=1&b=2"
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("foo", "bar")\
        .appendQueryParameter("nested", nestedUrl).build()
    assertEquals(nestedUrl, uri.getQueryParameter("nested"))
    assertEquals(nestedUrl, uri.getQueryParameters("nested")[0])

def test_GetQueryParameterWorkaround():
    # This was a workaround for a bug where getQueryParameter called
    # getQuery() instead of getEncodedQuery().
    
    nestedUrl = "http://crazybob.org/?a=1&b=2"
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("foo", "bar")\
        .appendQueryParameter("nested", Uri.encode(nestedUrl)).build()
    assertEquals(nestedUrl, Uri.decode(uri.getQueryParameter("nested")))
    assertEquals(nestedUrl,
            Uri.decode(uri.getQueryParameters("nested")[0]))

def test_GetQueryParameterEdgeCases():
    # key at beginning of URL
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("key", "a b")\
        .appendQueryParameter("keya", "c d")\
        .appendQueryParameter("bkey", "e f")\
        .build()
    assertEquals("a b", uri.getQueryParameter("key"))
    #key in middle of URL
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("akeyb", "a b")\
        .appendQueryParameter("keya", "c d")\
        .appendQueryParameter("key", "e f")\
        .appendQueryParameter("bkey", "g h")\
        .build()
    assertEquals("e f", uri.getQueryParameter("key"))
    #key at end of URL
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("akeyb", "a b")\
        .appendQueryParameter("keya", "c d")\
        .appendQueryParameter("key", "y z")\
        .build()
    assertEquals("y z", uri.getQueryParameter("key"))
    #key is a substring of parameters, but not present
    uri = Uri.parse("http://test/").buildUpon()\
        .appendQueryParameter("akeyb", "a b")\
        .appendQueryParameter("keya", "c d")\
        .appendQueryParameter("bkey", "e f")\
        .build()
    assertNull(uri.getQueryParameter("key"))
    #key is a prefix or suffix of the query
    uri = Uri.parse("http://test/?qq=foo")
    assertNull(uri.getQueryParameter("q"))
    assertNull(uri.getQueryParameter("oo"))
    #escaped keys
    uri = Uri.parse("http://www.google.com/?a%20b=foo&c%20d=")
    assertEquals("foo", uri.getQueryParameter("a b"))
    assertEquals("", uri.getQueryParameter("c d"))
    assertNull(uri.getQueryParameter("e f"))
    assertNull(uri.getQueryParameter("b"))
    assertNull(uri.getQueryParameter("c"))
    assertNull(uri.getQueryParameter(" d"))
    #empty values
    uri = Uri.parse("http://www.google.com/?a=&b=&&c=")
    assertEquals("", uri.getQueryParameter("a"))
    assertEquals("", uri.getQueryParameter("b"))
    assertEquals("", uri.getQueryParameter("c"))

def test_GetQueryParameterEmptyKey():
    uri = Uri.parse("http://www.google.com/?=b")
    assertEquals("b", uri.getQueryParameter(""))

def test_GetQueryParameterEmptyKey2():
    uri = Uri.parse("http://www.google.com/?a=b&&c=d")
    assertEquals("", uri.getQueryParameter(""))

def test_GetQueryParameterEmptyKey3():
    uri = Uri.parse("http://www.google.com?")
    assertEquals("", uri.getQueryParameter(""))

def test_GetQueryParameterEmptyKey4():
    uri = Uri.parse("http://www.google.com?a=b&")
    assertEquals("", uri.getQueryParameter(""))

def test_GetQueryParametersEmptyKey():
    uri = Uri.parse("http://www.google.com/?=b&")
    values = uri.getQueryParameters("")
    assertEquals(2, len(values))
    assertEquals("b", values[0])
    assertEquals("", values[1])

def test_GetQueryParametersEmptyKey2():
    uri = Uri.parse("http://www.google.com?")
    values = uri.getQueryParameters("")
    assertEquals(1, len(values))
    assertEquals("", values[0])

def test_GetQueryParametersEmptyKey3():
    uri = Uri.parse("http://www.google.com/?a=b&&c=d")
    values = uri.getQueryParameters("")
    assertEquals(1, len(values))
    assertEquals("", values[0])

def test_GetQueryParameterNames():
    uri = Uri.parse("http://test?a=1")
    names = uri.getQueryParameterNames()
    assertEquals(1, len(names))
    assertEquals("a", iter(names).next())

def test_GetQueryParameterNamesEmptyKey():
    uri = Uri.parse("http://www.google.com/?a=x&&c=z")
    names = uri.getQueryParameterNames()
    iterator = iter(names)
    assertEquals(3, len(names))
    assertEquals("a", iterator.next())
    assertEquals("", iterator.next())
    assertEquals("c", iterator.next())

def test_GetQueryParameterNamesEmptyKey2():
    uri = Uri.parse("http://www.google.com/?a=x&=d&c=z")
    names = uri.getQueryParameterNames()
    iterator = iter(names)
    assertEquals(3, len(names))
    assertEquals("a", iterator.next())
    assertEquals("", iterator.next())
    assertEquals("c", iterator.next())

def test_GetQueryParameterNamesEmptyValues():
    uri = Uri.parse("http://www.google.com/?a=foo&b=&c=")
    names = uri.getQueryParameterNames()
    iterator = iter(names)
    assertEquals(3, len(names))
    assertEquals("a", iterator.next())
    assertEquals("b", iterator.next())
    assertEquals("c", iterator.next())

def test_GetQueryParameterNamesEdgeCases():
    uri = Uri.parse("http://foo?a=bar&b=bar&c=&&d=baz&e&f&g=buzz&&&a&b=bar&h")
    names = uri.getQueryParameterNames()
    iterator = iter(names)
    assertEquals(9, len(names))
    assertEquals("a", iterator.next())
    assertEquals("b", iterator.next())
    assertEquals("c", iterator.next())
    assertEquals("", iterator.next())
    assertEquals("d", iterator.next())
    assertEquals("e", iterator.next())
    assertEquals("f", iterator.next())
    assertEquals("g", iterator.next())
    assertEquals("h", iterator.next())

def test_GetQueryParameterNamesEscapedKeys():
    uri = Uri.parse("http://www.google.com/?a%20b=foo&c%20d=")
    names = uri.getQueryParameterNames()
    assertEquals(2, len(names))
    iterator = iter(names)
    assertEquals("a b", iterator.next())
    assertEquals("c d", iterator.next())

def test_GetQueryParameterEscapedKeys():
    uri = Uri.parse("http://www.google.com/?a%20b=foo&c%20d=")
    value = uri.getQueryParameter("a b")
    assertEquals("foo", value)

def test_ClearQueryParameters():
    uri = Uri.parse("http://www.google.com/?a=x&b=y&c=z").buildUpon()\
        .clearQuery().appendQueryParameter("foo", "bar").build()
    names = uri.getQueryParameterNames()
    assertEquals(1, len(names))
    assertEquals("foo", iter(names).next())

#**
# * Query parameters may omit the '='. http://b/3124097
# */
def test_GetQueryParametersEmptyValue():
    assertEquals([""],
            Uri.parse("http://foo/path?abc").getQueryParameters("abc"))
    assertEquals([""],
            Uri.parse("http://foo/path?foo=bar&abc").getQueryParameters("abc"))
    assertEquals([""],
            Uri.parse("http://foo/path?abcd=abc&abc").getQueryParameters("abc"))
    assertEquals(["a", "", ""],
            Uri.parse("http://foo/path?abc=a&abc=&abc").getQueryParameters("abc"))
    assertEquals(["a", "", ""],
            Uri.parse("http://foo/path?abc=a&abc=&abc=").getQueryParameters("abc"))

#http://code.google.com/p/android/issues/detail?id=21064
def test_PlusCharacterInQuery():
    assertEquals("d e", Uri.parse("http://a/b?c=d%20e").getQueryParameter("c"))
    assertEquals("d e", Uri.parse("http://a/b?c=d+e").getQueryParameter("c"))

# def test_PathPrefixMatch():
#     #Exact match
#     assertTrue(Uri.parse("content://com.example/path").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     assertTrue(Uri.parse("content://com.example/path").isPathPrefixMatch(
#             Uri.parse("content://com.example/path")))
#     assertTrue(Uri.parse("content://com.example///path///").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     assertTrue(Uri.parse("content://com.example/path").isPathPrefixMatch(
#             Uri.parse("content://com.example///path///")))
#     #Child match
#     assertTrue(Uri.parse("content://com.example/path/to/child").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     assertTrue(Uri.parse("content://com.example/path/to/child").isPathPrefixMatch(
#             Uri.parse("content://com.example/path")))
#     #Extra parameters
#     assertTrue(Uri.parse("content://com.example/path#fragment").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     assertTrue(Uri.parse("content://com.example/path?q=v").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     assertTrue(Uri.parse("content://com.example/path/?q=v").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/")))
#     #Different path
#     assertFalse(Uri.parse("content://com.example/path").isPathPrefixMatch(
#             Uri.parse("content://com.example/path/deeper/")))
#     assertFalse(Uri.parse("content://com.example/path2").isPathPrefixMatch(
#             Uri.parse("content://com.example/path")))
#     #Top-level match
#     assertTrue(Uri.parse("content://com.example/path/").isPathPrefixMatch(
#             Uri.parse("content://com.example/")))
#     assertTrue(Uri.parse("content://com.example/path/").isPathPrefixMatch(
#             Uri.parse("content://com.example")))
#     #Different prefixes
#     assertFalse(Uri.parse("content://com.example/path/").isPathPrefixMatch(
#             Uri.parse("file://com.example/path/")))
#     assertFalse(Uri.parse("content://com.example/path/").isPathPrefixMatch(
#             Uri.parse("content://org.example/path/")))
#     #Escaping
#     assertTrue(Uri.parse("content://com.example/path path/").isPathPrefixMatch(
#             Uri.parse("content://com.example/path%20path/")))
#     assertFalse(Uri.parse("content://com.example/path/path").isPathPrefixMatch(
#             Uri.parse("content://com.example/path%2Fpath")))

def test_ToSafeString():
    checkToSafeString("tel:xxxxxx", "tel:Google")
    checkToSafeString("tel:xxxxxxxxxx", "tel:1234567890")
    checkToSafeString("tEl:xxx.xxx-xxxx", "tEl:123.456-7890")
    checkToSafeString("sms:xxxxxx", "sms:123abc")
    checkToSafeString("smS:xxx.xxx-xxxx", "smS:123.456-7890")
    checkToSafeString("smsto:xxxxxx", "smsto:123abc")
    checkToSafeString("SMSTo:xxx.xxx-xxxx", "SMSTo:123.456-7890")
    checkToSafeString("mailto:xxxxxxx@xxxxxxx.xxx", "mailto:android@android.com")
    checkToSafeString("Mailto:xxxxxxx@xxxxxxx.xxxxxxxxxx",
            "Mailto:android@android.com/secret")
    checkToSafeString("sip:xxxxxxx@xxxxxxx.xxxxxxxx", "sip:android@android.com:1234")
    checkToSafeString("sIp:xxxxxxx@xxxxxxx.xxx", "sIp:android@android.com")
    checkToSafeString("http://www.android.com/...", "http://www.android.com")
    checkToSafeString("HTTP://www.android.com/...", "HTTP://www.android.com")
    checkToSafeString("http://www.android.com/...", "http://www.android.com/")
    checkToSafeString("http://www.android.com/...", "http://www.android.com/secretUrl?param")
    checkToSafeString("http://www.android.com/...",
            "http://user:pwd@www.android.com/secretUrl?param")
    checkToSafeString("http://www.android.com/...",
            "http://user@www.android.com/secretUrl?param")
    checkToSafeString("http://www.android.com/...", "http://www.android.com/secretUrl?param")
    checkToSafeString("http:///...", "http:///path?param")
    checkToSafeString("http:///...", "http://")
    checkToSafeString("http://:12345/...", "http://:12345/")
    checkToSafeString("https://www.android.com/...", "https://www.android.com/secretUrl?param")
    checkToSafeString("https://www.android.com:8443/...",
            "https://user:pwd@www.android.com:8443/secretUrl?param")
    checkToSafeString("https://www.android.com/...", "https://user:pwd@www.android.com")
    checkToSafeString("Https://www.android.com/...", "Https://user:pwd@www.android.com")
    checkToSafeString("ftp://ftp.android.com/...", "ftp://ftp.android.com/")
    checkToSafeString("ftP://ftp.android.com/...", "ftP://anonymous@ftp.android.com/")
    checkToSafeString("ftp://ftp.android.com:2121/...",
            "ftp://root:love@ftp.android.com:2121/")
    checkToSafeString("unsupported://ajkakjah/askdha/secret?secret",
            "unsupported://ajkakjah/askdha/secret?secret")
    checkToSafeString("unsupported:ajkakjah/askdha/secret?secret",
            "unsupported:ajkakjah/askdha/secret?secret")

def checkToSafeString(expectedSafeString, original):
    assertEquals(expectedSafeString, Uri.parse(original).toSafeString())

