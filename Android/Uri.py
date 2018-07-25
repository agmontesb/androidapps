# -*- coding: utf-8 -*-
import re
import urllib
import urlparse


class Uri(object):
    def __init__(self, scheme, authority, path, params, query, fragments):
        userinfo, netloc = authority.split('@') if authority and '@' in authority else ('', authority)
        host, port = netloc.split(':') if netloc and ':' in netloc else (netloc, None) 
        self._userinfo = userinfo
        self._host = host
        self._port = port and int(port)
        self._uridata = urlparse.ParseResult(scheme, authority, path, params, query, fragments)

    def buildUpon(self):
        """Constructs a new builder, copying the attributes from this Uri."""
        pass

    def compareTo(self, other):
        """Compares the string representation of this Uri with that of another."""
        myString = self.toString()
        otherStr = other.toString()
        return -1*(myString < otherStr) or 1*(myString > otherStr)

    @classmethod
    def decode(cls, s):
        """Decodes '%'-escaped octets in the given string using the UTF-8 scheme."""
        return urllib.unquote(s)

    @classmethod
    def encode(self, s, allow=None):
        """Encodes characters in the given string as '%'-escaped octets using the UTF-8 scheme."""
        return urllib.quote(s, allow)

    def equals(self, other):
        """Compares this Uri to another object for equality."""
        return self.toString() == other.toString()

    @classmethod
    def fromFile(self, file):
        """Creates a Uri from a file."""
        uriString = 'file:' + urllib.pathname2url(file)
        return self.parse(uriString)

    @classmethod
    def fromParts(self, scheme, ssp, fragment):
        """Creates an opaque Uri from the given components."""
        uriString = '%s:%s#%s' % (scheme, ssp, fragment)
        uriString = self.encode(uriString)
        return Uri.parse(uriString)

    def getAuthority(self):
        """Gets the decoded authority part of this URI."""
        if self.isOpaque(): return ''
        return self._uridata.netloc

    def getBooleanQueryParameter(self, key, defaultValue):
        """Searches the query string for the first value with the given key and interprets it as a boolean value."""
        value = self.getQueryParameter(key)
        return value == 'true' if value else defaultValue

    def getEncodedAuthority(self):
        """Gets the encoded authority part of this URI."""
        if self.isOpaque(): return ''
        return self._uridata.netloc

    def getEncodedFragment(self):
        """Gets the encoded fragment part of this URI, everything after the '#'."""
        return self._uridata.fragment

    def getEncodedPath(self):
        """Gets the encoded path."""
        if self.isOpaque(): return ''
        return self._uridata.path

    def getEncodedQuery(self):
        """Gets the encoded query component from this URI."""
        if self.isOpaque(): return ''
        return self._uridata.query

    def getEncodedSchemeSpecificPart(self):
        """Gets the scheme-specific part of this URI, i.e.&nbsp;everything between the scheme separator ':' and the fragment separator '#'."""
        uriString = self.toString()
        uriString = uriString.split(':', 1)[-1]
        uriString = uriString.split('#')[0]
        return uriString

    def getEncodedUserInfo(self):
        """Gets the encoded user information from the authority."""
        if self.isOpaque(): return ''
        return self._userinfo

    def getFragment(self):
        """Gets the decoded fragment part of this URI, everything after the '#'."""
        return self.decode(self.getEncodedFragment())

    def getHost(self):
        """Gets the encoded host from the authority for this URI."""
        if self.isOpaque(): return ''
        return self._host

    def getLastPathSegment(self):
        """Gets the decoded last segment in the path."""
        path = self.getPathSegments()
        if path:
            path = path[-1]
        return path

    def getPath(self):
        """Gets the decoded path."""
        return self.decode(self.getEncodedPath())

    def getPathSegments(self):
        """Gets the decoded path segments."""
        path = self.getPath()
        if path:
            path = path[1:].split('/')
        return path

    def getPort(self):
        """Gets the port from the authority for this URI."""
        if self.isOpaque(): return ''
        return self._port

    def getQuery(self):
        """Gets the decoded query component from this URI."""
        return self.decode(self.getEncodedQuery())

    def getQueryParameter(self, key):
        """Searches the query string for the first value with the given key."""
        queryString = self.getEncodedQuery()
        pattern = r'&*%s=([^&]+)&*' % key
        m = re.search(pattern, queryString)
        try:
            return m.group(1)
        except:
            return ''

    def getQueryParameterNames(self):
        """Returns a set of the unique names of all query parameters."""
        queryString = self.getEncodedQuery()
        parse_qs = urlparse.parse_qs(queryString)
        return set(parse_qs)

    def getQueryParameters(self, key):
        """Searches the query string for parameter values with the given key."""
        queryString = self.getEncodedQuery()
        parse_qs = urlparse.parse_qs(queryString)
        return parse_qs.get(key, '')

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
        return self.isRelative() or self.getEncodedSchemeSpecificPart()[0] == '/'

    def isOpaque(self):
        """Returns true if this URI is opaque like "mailto:nobody@google.com"."""
        return self.isAbsolute() and self.getEncodedSchemeSpecificPart()[0] != '/'

    def isRelative(self):
        """Returns true if this URI is relative, i.e. if it doesn't contain an explicit scheme."""
        return not self.isAbsolute()

    def normalizeScheme(self):
        """Return an equivalent URI with a lowercase scheme component."""
        (scheme, netloc, path, params, query, fragments) = self._uridata
        scheme = self.getScheme().lower()
        return Uri(scheme, netloc, path, params, query, fragments)

    @classmethod
    def parse(self, uriString):
        """Creates a Uri which parses the given encoded URI string."""
        uridata = urlparse.urlparse(uriString)
        return Uri(*uridata)

    def toString(self):
        """Returns the encoded string representation of this URI."""
        return urlparse.urlunparse(self._uridata)

    @classmethod
    def withAppendedPath(self, baseUri, pathSegment):
        """Creates a new Uri by appending an already-encoded path segment to a base Uri."""
        uridata = urlparse.urlparse(baseUri)
        uridata = uridata._replace(path=pathSegment)
        return Uri(*uridata)


    @classmethod
    def writeToParcel(self, out, uri):
        """Writes a Uri to a Parcel."""
        pass
