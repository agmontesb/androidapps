# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/net/Uri"""
import re
import abc
import urllib
import urlparse

from Android import overload, Object
from Android.interface.IParcelable import IParcelable


class Uri(IParcelable):
    """
    Immutable URI reference. A URI reference includes a URI and a fragment,
    the component of the URI following a '#'. Builds and parses URI references
    which conform to RFC 2396.
    In the interest of performance, this class performs little to no validation.
    Behavior is undefined for invalid input. This class is very forgiving--in the
    face of invalid input, it will return garbage rather than throw an exception
    unless otherwise specified.
    """
    """
    public static final Creator<Uri> CREATOR:

    """
    CREATOR = type(
        'UriCreator',
        (IParcelable.ICreator,),
        {
            'createFromParcel': lambda self, inparcel: Uri.EMPTY._createFromParcel(inparcel),
            'newArray': lambda self, size: (size * type(Uri.EMPTY))()
        }
    )()
    """
    public static final Uri EMPTY:
    The empty URI, equivalent to "".
    """
    EMPTY = None

    def buildUpon(self):
        """
        Constructs a new builder, copying the attributes from this Uri.
        :return: Uri.Builder.
        """
        pass

    def compareTo(self, other):
        """
        Compares the string representation of this Uri with that of another.
        :param other: Uri
        :return: int.
        """
        thisString = self.toString()
        otherStr = other.toString()
        return -1*(thisString < otherStr) or 1*(thisString > otherStr)

    def __cmp__(self, other):
        return self.compareTo()

    @classmethod
    def decode(self, s):
        """
        Decodes '%'-escaped octets in the given string using the UTF-8 scheme.
        Replaces invalid octets with the unicode replacement character
        ("\\uFFFD").
        :param s: String: encoded string to decode
        :return: String. the given string with escaped octets decoded, or null
        if s is null
        """
        if s is None: return
        return urllib.unquote(s)

    @classmethod
    def encode(cls, s, allow="_-!.~'()*"):
        """
        Encodes characters in the given string as '%'-escaped octets using the
        UTF-8 scheme. Leaves letters ("A-Z", "a-z"), numbers ("0-9"), and
        unreserved characters ("_-!.~'()*") intact. Encodes all other
        characters with the exception of those specified in the allow argument.
        :param s: String: string to encode
        :param allow: String: set of additional characters to allow in the
        encoded form, null if no characters should be skipped
        :return: String. an encoded version of s suitable for use as a URI
        component, or null if s is null
        """
        if s is None: return
        return urllib.quote(s, allow)

    def equals(self, o):
        """
        Compares this Uri to another object for equality. Returns true if the
        encoded string representations of this Uri and the given Uri are
        equal. Case counts. Paths are not normalized. If one Uri specifies a
        default port explicitly and the other leaves it implicit, they will
        not be considered equal.
        :param o: Object: the reference object with which to compare.
        :return: boolean. true if this object is the same as the obj argument;
        false otherwise.
        """
        try:
            return self.toString() == o.toString()
        except:
            return False

    def __eq__(self, other):
        return self.equals(other)

    @classmethod
    def fromFile(cls, file):
        """
        Creates a Uri from a file. The URI has the form "file://". Encodes
        path characters with the exception of '/'.  Example:
        "file:///tmp/android.txt"
        :param file: File
        :return: Uri. a Uri for the given file
        :raises: NullPointerExceptionif file is null
        """
        if file is None:
            raise Exception("NullPointerException")
        uriString = 'file://' + urllib.pathname2url(file)
        return cls.parse(uriString)

    @classmethod
    def fromParts(cls, scheme, ssp, fragment):
        """
        Creates an opaque Uri from the given components. Encodes the ssp which
        means this method cannot be used to create hierarchical URIs.
        :param scheme: String: of the URI
        :param ssp: String: scheme-specific-part, everything between the
        scheme separator (':') and the fragment separator ('#'), which will
        get encoded
        :param fragment: String: fragment, everything after the '#', null if
        undefined, will get encoded
        :return: Uri. Uri composed of the given scheme, ssp, and fragment
        :raises: NullPointerException if scheme or ssp is null
        See also: if you don't want the ssp and fragment to be encoded
        """
        if not scheme:
            raise Exception('NullPointerException: "scheme"')
        if not ssp:
            raise Exception('NullPointerException: "ssp"')
        uriString = '%s:%s' % (scheme, ssp)
        if fragment:
            uriString += '#%s' % fragment
        return cls.parse(uriString)

    def getAuthority(self):
        """
        Gets the decoded authority part of this URI. For server addresses, the
        authority is structured as follows: [ userinfo '@' ] host [ ':' port
        ]Examples: "google.com", "bob@google.com:80"
        :return: String. the authority for this URI or null if not present
        """
        pass

    def getBooleanQueryParameter(self, key, defaultValue):
        """
        Searches the query string for the first value with the given key and
        interprets it as a boolean value. "false" and "0" are interpreted as
        false, everything else is interpreted as true.
        :param key: String: which will be decoded
        :param defaultValue: boolean: the default value to return if there is
        no query parameter for key
        :return: boolean. the boolean interpretation of the query parameter key
        """
        pass

    def getEncodedAuthority(self):
        """
        Gets the encoded authority part of this URI. For server addresses, the
        authority is structured as follows: [ userinfo '@' ] host [ ':' port
        ]Examples: "google.com", "bob@google.com:80"
        :return: String. the authority for this URI or null if not present
        """
        pass

    def getEncodedFragment(self):
        """
        Gets the encoded fragment part of this URI, everything after the '#'.
        :return: String. the encoded fragment or null if there isn't one
        """
        pass

    def getEncodedPath(self):
        """
        Gets the encoded path.
        :return: String. the encoded path, or null if this is not a
        hierarchical URI (like "mailto:nobody@google.com") or the URI is
        invalid
        """
        pass

    def getEncodedQuery(self):
        """
        Gets the encoded query component from this URI. The query comes after
        the query separator ('?') and before the fragment separator ('#').
        This method would return "q=android" for
        "http://www.google.com/search?q=android".
        :return: String. the encoded query or null if there isn't one
        """
        pass

    def getEncodedSchemeSpecificPart(self):
        """
        Gets the scheme-specific part of this URI, i.e.&nbsp;everything
        between the scheme separator ':' and the fragment separator '#'. If
        this is a relative URI, this method returns the entire URI. Leaves
        escaped octets intact.  Example: "//www.google.com/search?q=android"
        :return: String. the decoded scheme-specific-part
        """
        pass

    def getEncodedUserInfo(self):
        """
        Gets the encoded user information from the authority. For example, if
        the authority is "nobody@google.com", this method will return "nobody".
        :return: String. the user info for this URI or null if not present
        """
        pass

    def getFragment(self):
        """
        Gets the decoded fragment part of this URI, everything after the '#'.
        :return: String. the decoded fragment or null if there isn't one
        """
        pass

    def getHost(self):
        """
        Gets the encoded host from the authority for this URI. For example, if
        the authority is "bob@google.com", this method will return
        "google.com".
        :return: String. the host for this URI or null if not present
        """
        pass

    def getLastPathSegment(self):
        """
        Gets the decoded last segment in the path.
        :return: String. the decoded last segment or null if the path is empty
        """
        pass

    def getPath(self):
        """
        Gets the decoded path.
        :return: String. the decoded path, or null if this is not a
        hierarchical URI (like "mailto:nobody@google.com") or the URI is
        invalid
        """
        pass

    def getPathSegments(self):
        """
        Gets the decoded path segments.
        :return: List<String>. decoded path segments, each without a leading
        or trailing '/'
        """
        pass

    def getPort(self):
        """
        Gets the port from the authority for this URI. For example, if the
        authority is "google.com:80", this method will return 80.
        :return: int. the port for this URI or -1 if invalid or not present
        """
        pass

    def getQuery(self):
        """
        Gets the decoded query component from this URI. The query comes after
        the query separator ('?') and before the fragment separator ('#').
        This method would return "q=android" for
        "http://www.google.com/search?q=android".
        :return: String. the decoded query or null if there isn't one
        """
        pass

    def getQueryParameter(self, key):
        """
        Searches the query string for the first value with the given key.
        Warning: Prior to Jelly Bean, this decoded the '+' character as '+'
        rather than ' '.
        :param key: String: which will be encoded
        :return: String. the decoded value or null if no parameter is found
        :raises: UnsupportedOperationExceptionif this isn't a hierarchical
        URINullPointerExceptionif key is null
        """
        pass

    def getQueryParameterNames(self):
        """
        Returns a set of the unique names of all query parameters. Iterating
        over the set will return the names in order of their first occurrence.
        :return: Set<String>. a set of decoded names
        :raises: UnsupportedOperationExceptionif this isn't a hierarchical URI
        """
        pass

    def getQueryParameters(self, key):
        """
        Searches the query string for parameter values with the given key.
        :param key: String: which will be encoded
        :return: List<String>. a list of decoded values
        :raises: UnsupportedOperationExceptionif this isn't a hierarchical
        URINullPointerExceptionif key is null
        """
        pass

    def getScheme(self):
        """
        Gets the scheme of this URI. Example: "http"
        :return: String. the scheme or null if this is a relative URI
        """
        pass

    def getSchemeSpecificPart(self):
        """
        Gets the scheme-specific part of this URI, i.e.&nbsp;everything
        between the scheme separator ':' and the fragment separator '#'. If
        this is a relative URI, this method returns the entire URI. Decodes
        escaped octets.  Example: "//www.google.com/search?q=android"
        :return: String. the decoded scheme-specific-part
        """
        pass

    def getUserInfo(self):
        """
        Gets the decoded user information from the authority. For example, if
        the authority is "nobody@google.com", this method will return "nobody".
        :return: String. the user info for this URI or null if not present
        """
        pass

    def hashCode(self):
        """
        Hashes the encoded string represention of this Uri consistently with
        equals(Object).
        :return: int. a hash code value for this object.
        """
        return self.toString().__hash__()

    def isAbsolute(self):
        """
        Returns true if this URI is absolute, i.e.&nbsp;if it contains an
        explicit scheme.
        :return: boolean. true if this URI is absolute, false if it's relative
        """
        return not self.isRelative()

    def isHierarchical(self):
        """
        Returns true if this URI is hierarchical like "http://google.com".
        Absolute URIs are hierarchical if the scheme-specific part starts with
        a '/'. Relative URIs are always hierarchical.
        :return: boolean.
        """
        pass

    def isOpaque(self):
        """
        Returns true if this URI is opaque like "mailto:nobody@google.com".
        The scheme-specific part of an opaque URI cannot start with a '/'.
        :return: boolean.
        """
        return not self.isHierarchical()

    def isRelative(self):
        """
        Returns true if this URI is relative, i.e.&nbsp;if it doesn't contain
        an explicit scheme.
        :return: boolean. true if this URI is relative, false if it's absolute
        """
        pass

    def normalizeScheme(self):
        """
        Return an equivalent URI with a lowercase scheme component. This
        aligns the Uri with Android best practices for intent filtering.  For
        example, "HTTP://www.android.com" becomes "http://www.android.com"
        All URIs received from outside Android (such as user input, or
        external sources like Bluetooth, NFC, or the Internet) should be
        normalized before they are used to create an Intent.  This method does
        not validate bad URI's, or 'fix' poorly formatted URI's - so do not
        use it for input validation. A Uri will always be returned, even if
        the Uri is badly formatted to begin with and a scheme component cannot
        be found.
        :return: Uri. normalized Uri (never null)
        See also: Intent.setData(Uri)Intent.setDataAndNormalize(Uri)
        """
        pass

    @staticmethod
    def _uriparse(uriString):
        scheme, authority, path, query, fragment = None, None, None, None, None
        try:
            scheme, uriString = uriString.split(':', 1)
        except:
            pass
        if uriString.startswith('//'):
            uriString = uriString[2:]
            try:
                authority, sep, uriString = re.split(r'([/?#\\])', uriString, 1)
                uriString = sep + uriString
            except:
                authority, uriString = uriString, ''

        try:
            path, sep, uriString = re.split(r'([?#])', uriString, 1)
            uriString = sep + uriString
        except:
            path, uriString = uriString, None

        if uriString:
            uriString = uriString.lstrip('?')
            try:
                query, fragment = uriString.split('#', 1)
                query = query.replace('+', '%20')
                query = query or None
            except:
                query = uriString.replace('+', '%20')
        return urlparse.ParseResult(scheme, authority, path, '', query, fragment)


    @classmethod
    def parse(cls, uriString):
        """
        Creates a Uri which parses the given encoded URI string.
        :param uriString: String: an RFC 2396-compliant, encoded URI
        :return: Uri. Uri for this given uri string
        :raises: NullPointerExceptionif uriString is null
        """
        if uriString is None:
            raise Exception("NullPointerException")
        uridata = cls._uriparse(uriString)
        return Uri.Builder()\
            .scheme(uridata.scheme)\
            .encodedAuthority(uridata.netloc)\
            .encodedPath(uridata.path)\
            .encodedQuery(uridata.query)\
            .encodedFragment(uridata.fragment)\
            .build()

    def toSafeString(self):
        """
        Returns the encoded string representation of this URI. Example:
        "http://google.com/"
        :return: String. a string representation of the object.
        """
        scheme = self.getScheme()
        ssp = self.getSchemeSpecificPart()
        builder = ''
        if scheme and scheme.lower() in ['tel', 'sip', 'sms', 'smsto', 'mailto', 'nfc']:
            builder += scheme + ':'
            if ssp: builder += re.sub(r'[^-@.]', 'x', ssp)
            return builder
        if scheme:
            if scheme.lower() in ['http', 'https', 'ftp']:
                host = self.getHost()
                port = self.getPort()
                ssp = '//'
                if host:
                    ssp += host
                if port != -1:
                    ssp += ':' + str(port)
                ssp += '/...'
            builder += scheme + ':'
        if ssp:
            builder += ssp
        return builder

    def toString(self):
        """
        Returns the encoded string representation of this URI. Example:
        "http://google.com/"
        :return: String. a string representation of the object.
        """
        pass

    @classmethod
    def withAppendedPath(cls, baseUri, pathSegment):
        """
        Creates a new Uri by appending an already-encoded path segment to a
        base Uri.
        :param baseUri: Uri: Uri to append path segment to
        :param pathSegment: String: encoded path segment to append
        :return: Uri. a new Uri based on baseUri with the given segment
        appended to the path
        :raises: NullPointerExceptionif baseUri is null
        """
        return baseUri.buildUpon().appendPath(pathSegment).build()

    @classmethod
    def writeToParcel(cls, out, uri):
        """
        Writes a Uri to a Parcel.
        :param out: Parcel: parcel to write to
        :param uri: Uri: to write, can be null
        """
        uriString = uri.toString() if uri else ''
        out.writeString(uriString)

    class Builder(Object):
        '''
        Helper class for building or manipulating URI references. Not safe for
        concurrent use.
        An absolute hierarchical URI reference follows the pattern:
                    <scheme>://<authority><absolute path>?<query>#<fragment>

        Relative URI references (which are always hierarchical) follow one of two
        patterns:
                    <relative or absolute path>?<query>#<fragment> or
                    //<authority><absolute path>?<query>#<fragment>

        An opaque URI follows this pattern:
                    <scheme>:<opaque part>#<fragment>

        Use Uri.buildUpon() to obtain a builder representing an existing URI.
        '''
        def _UriImpl(self, *args, **kwargs):
            class _UriImpl(Uri):
                def __init__(self, scheme, authority, path, query, fragments, params=''):
                    super(_UriImpl, self).__init__()
                    userinfo, netloc = authority.rsplit('@', 1) if authority and '@' in authority else ('', authority)
                    host, port = netloc.split(':', 1) if netloc and ':' in netloc else (netloc, '-1')
                    self._userinfo = userinfo
                    self._host = self.decode(host)
                    self._port = port and int(self.decode(port))
                    self._uridata = urlparse.ParseResult(scheme, authority, path, params, query, fragments)

                def buildUpon(self):
                    """Constructs a new builder, copying the attributes from this Uri."""
                    uriString = self.toString()
                    uridata = self._uriparse(uriString)
                    return Uri.Builder() \
                        .scheme(uridata.scheme) \
                        .encodedAuthority(uridata.netloc) \
                        .encodedPath(uridata.path) \
                        .encodedQuery(uridata.query) \
                        .encodedFragment(uridata.fragment)

                def getAuthority(self):
                    """Gets the decoded authority part of this URI."""
                    if self.isOpaque(): return None
                    return self._uridata.netloc

                def getBooleanQueryParameter(self, key, defaultValue):
                    """Searches the query string for the first value with the given key and interprets it as a boolean value."""
                    value = self.getQueryParameter(key)
                    return value == 'true' if value else defaultValue

                def getEncodedAuthority(self):
                    """Gets the encoded authority part of this URI."""
                    if self.isOpaque(): return
                    return self._uridata.netloc

                def getEncodedFragment(self):
                    """Gets the encoded fragment part of this URI, everything after the '#'."""
                    return self._uridata.fragment

                def getEncodedPath(self):
                    """Gets the encoded path."""
                    if self.isOpaque(): return
                    return self._uridata.path

                def getEncodedQuery(self):
                    """Gets the encoded query component from this URI."""
                    if self.isOpaque(): return
                    return self._uridata.query

                def getEncodedSchemeSpecificPart(self):
                    """Gets the scheme-specific part of this URI, i.e.&nbsp;everything between the scheme separator ':' and the fragment separator '#'."""
                    uriString = self.toString()
                    if uriString:
                        uriString = uriString.split(':', 1)[-1]
                        uriString = uriString.split('#')[0]
                        return uriString

                def getEncodedUserInfo(self):
                    """Gets the encoded user information from the authority."""
                    if self.isOpaque(): return None
                    return self._userinfo

                def getFragment(self):
                    """Gets the decoded fragment part of this URI, everything after the '#'."""
                    return self.decode(self.getEncodedFragment())

                def getHost(self):
                    """Gets the encoded host from the authority for this URI."""
                    if self.isOpaque(): return None
                    return self._host

                def getLastPathSegment(self):
                    """Gets the decoded last segment in the path."""
                    path = self.getPathSegments()
                    try:
                        answ = path[-1]
                    except:
                        answ = None
                    return answ

                def getPath(self):
                    """Gets the decoded path."""
                    return self.decode(self.getEncodedPath())

                def getPathSegments(self):
                    """Gets the decoded path segments."""
                    path = self.getPath() or []
                    if path:
                        path = path[1:].split('/')
                    return path

                def getPort(self):
                    """Gets the port from the authority for this URI."""
                    if self.isOpaque(): return -1
                    return self._port or -1

                def getQuery(self):
                    """Gets the decoded query component from this URI."""
                    return self.decode(self.getEncodedQuery())

                def getQueryParameter(self, key):
                    """Searches the query string for the first value with the given key."""
                    queryString = self.getEncodedQuery()
                    try:
                        queryString = '&' + queryString.lstrip('&') + '&'
                        pattern = r'&%s=*([^&=]+)*&' % (Uri.encode(key) or '')
                        m = re.search(pattern, queryString)
                        return Uri.decode(m.group(1)) or ''
                    except:
                        return None

                def getQueryParameterNames(self):
                    """Returns a set of the unique names of all query parameters."""
                    queryString = self.getEncodedQuery()
                    if queryString:
                        queryString = '&' + queryString.lstrip('&') + '&'
                        pattern = r'(?<=&)([^&=]+)*[=&]'
                        keys = re.findall(pattern, queryString)
                        keys = reduce(lambda t, x: (t + [x]) if x not in t else t, keys, [])
                        return map(lambda x: Uri.decode(x) or '', keys)

                def getQueryParameters(self, key):
                    """Searches the query string for parameter values with the given key."""
                    queryString = self.getEncodedQuery()
                    if queryString is not None:
                        queryString = '&' + queryString.lstrip('&') + '&'
                        pattern = r'(?<=&)%s=*([^&=]+)*&' % (Uri.encode(key) or '')
                        return map(lambda x: Uri.decode(x) or '', re.findall(pattern, queryString))
                    return []

                def getScheme(self):
                    """Gets the scheme of this URI."""
                    return self._uridata.scheme

                def getSchemeSpecificPart(self):
                    """Gets the scheme-specific part of this URI, i.e. everything between the scheme separator ':' and the fragment separator '#'."""
                    return self.decode(self.getEncodedSchemeSpecificPart())

                def getUserInfo(self):
                    """Gets the decoded user information from the authority."""
                    return self.decode(self.getEncodedUserInfo())

                def hashCode(self):
                    """Hashes the encoded string represention of this Uri consistently with equals(Object)."""
                    uriString = self.toString()
                    return uriString.__hash__()

                def isAbsolute(self):
                    """Returns true if this URI is absolute, i.e. if it contains an explicit scheme."""
                    return bool(self.getScheme())

                def isHierarchical(self):
                    """Returns true if this URI is hierarchical like "http://google.com"."""
                    ssp = self.getEncodedSchemeSpecificPart()
                    return self.isRelative() or (bool(ssp) and ssp[0] == '/')

                def isOpaque(self):
                    """Returns true if this URI is opaque like "mailto:nobody@google.com"."""
                    ssp = self.getEncodedSchemeSpecificPart()
                    return self.isAbsolute() and ssp and ssp[0] != '/' and '?' not in ssp

                def isRelative(self):
                    """Returns true if this URI is relative, i.e. if it doesn't contain an explicit scheme."""
                    return not self.isAbsolute()

                def normalizeScheme(self):
                    """Return an equivalent URI with a lowercase scheme component."""
                    (scheme, netloc, path, params, query, fragments) = self._uridata
                    scheme = self.getScheme().lower()
                    return Uri.Builder() \
                        .scheme(scheme) \
                        .authority(netloc) \
                        .path(path) \
                        .query(query) \
                        .fragment(fragments) \
                        .build()

                def toString(self):
                    """Returns the encoded string representation of this URI."""
                    scheme, authority, path, params, query, fragment = self._uridata
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

                    return sb
                    # return urlparse.urlunparse(self._uridata) or ''

                def _createFromParcel(cls, parcel):
                    uriString = parcel.readString()
                    return cls.parse(uriString) if uriString else None

                def describeContents(self):
                    return 0
            return _UriImpl(*args, **kwargs)

        def __init__(self):
            super(Uri.Builder, self).__init__()
            self._scheme = None
            self._authority = None
            self._path = None
            self._query = None
            self._fragment = None
            pass

        def appendEncodedPath(self, newSegment):
            """
            Appends the given segment to the path.
            :param newSegment: String
            :return: Uri.Builder.
            """
            if newSegment:
                newSegment = self._path.rstrip('/') + '/' + newSegment
                self._path = newSegment
            return self

        def appendPath(self, newSegment):
            """
            Encodes the given segment and appends it to the path.
            :param newSegment: String
            :return: Uri.Builder.
            """
            newSegment = Uri.encode(newSegment)
            return self.appendEncodedPath(newSegment)

        def appendQueryParameter(self, key, value):
            """
            Encodes the key and value and then appends the parameter to the query
            string.
            :param key: String: which will be encoded
            :param value: String: which will be encoded
            :return: Uri.Builder.
            """
            query = '{}={}'.format(*map(Uri.encode, (key, value)))
            self._query = (self._query + '&' + query) if self._query else query
            return self

        def authority(self, authority):
            """
            Encodes and sets the authority.
            :param authority: String
            :return: Uri.Builder.
            """
            authority = Uri.encode(authority)
            return self.encodedAuthority(authority)

        def build(self):
            """
            Constructs a Uri with the current attributes.
            :return: Uri.
            :raises: UnsupportedOperationException if the URI is opaque and the
            scheme is null
            """
            return self._UriImpl(self._scheme, self._authority, self._path, self._query, self._fragment)

        def clearQuery(self):
            """
            Clears the the previously set query.
            :return: Uri.Builder.
            """
            self._query = None
            return self

        def encodedAuthority(self, authority):
            """
            Sets the previously encoded authority.
            :param authority: String
            :return: Uri.Builder.
            """
            self._authority = authority
            return self

        def encodedFragment(self, fragment):
            """
            Sets the previously encoded fragment.
            :param fragment: String
            :return: Uri.Builder.
            """
            self._fragment = fragment
            return self

        def encodedOpaquePart(self, opaquePart):
            """
            Sets the previously encoded opaque scheme-specific-part.
            :param opaquePart: String: encoded opaque part
            :return: Uri.Builder.
            """
            uriString = '%s:%s' % (self._scheme, opaquePart)
            if self._fragment:
                uriString += '#%s' % self._fragment
            uridata = Uri._uriparse(uriString)
            self.scheme(uridata.scheme)
            self.encodedAuthority(uridata.netloc)
            self.encodedPath(uridata.path)
            self.encodedQuery(uridata.query)
            self.encodedFragment(uridata.fragment)
            return self

        def encodedPath(self, path):
            """
            Sets the previously encoded path.  If the path is not null and doesn't
            start with a '/', and if you specify a scheme and/or authority, the
            builder will prepend the given path with a '/'.
            :param path: String
            :return: Uri.Builder.
            """
            # if path and (self._scheme or self._authority):
            #     path = '/' + path.strip('/')
            self._path = path
            return self

        def encodedQuery(self, query):
            """
            Sets the previously encoded query.
            :param query: String
            :return: Uri.Builder.
            """
            self._query = query
            return self

        def fragment(self, fragment):
            """
            Encodes and sets the fragment.
            :param fragment: String
            :return: Uri.Builder.
            """
            fragment = Uri.encode(fragment)
            return self.encodedFragment(fragment)

        def opaquePart(self, opaquePart):
            """
            Encodes and sets the given opaque scheme-specific-part.
            :param opaquePart: String: decoded opaque part
            :return: Uri.Builder.
            """
            opaquePart = Uri.encode(opaquePart)
            return self.encodedOpaquePart(opaquePart)

        def path(self, path):
            """
            Sets the path. Leaves '/' characters intact but encodes others as
            necessary.  If the path is not null and doesn't start with a '/', and
            if you specify a scheme and/or authority, the builder will prepend the
            given path with a '/'.
            :param path: String
            :return: Uri.Builder.
            """
            path = Uri.encode(path, '/')
            return self.encodedPath(path)

        def query(self, query):
            """
            Encodes and sets the query.
            :param query: String
            :return: Uri.Builder.
            """
            query = Uri.encode(query)
            return self.encodedQuery(query)

        def scheme(self, scheme):
            """
            Sets the scheme.
            :param scheme: String: name or null if this is a relative Uri
            :return: Uri.Builder.
            """
            self._scheme = scheme
            return self

        def toString(self):
            """
            Returns a string representation of the object. In general, the
            toString method returns a string that "textually represents" this
            object. The result should be a concise but informative representation
            that is easy for a person to read. It is recommended that all
            subclasses override this method.  The toString method for class Object
            returns a string consisting of the name of the class of which the
            object is an instance, the at-sign character `@', and the unsigned
            hexadecimal representation of the hash code of the object. In other
            words, this method returns a string equal to the value of:
            getClass().getName() + '@' + Integer.toHexString(hashCode())
            :return: String. a string representation of the object.
            """
            return self.build().toString()

Uri.EMPTY = Uri.Builder().build()