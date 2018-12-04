# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/IntentFilter"""
import itertools

from Android import overload, Object
from Android.Os.PatternMatcher import PatternMatcher
from Android.Uri import Uri
from Android.content.Intent import Intent
from Android.interface.IParcelable import IParcelable, ICreator

"""
public static final int MATCH_ADJUSTMENT_MASK:
The part of a match constant that applies a quality adjustment to the
basic category of match.  The value MATCH_ADJUSTMENT_NORMAL
is no adjustment; higher numbers than that improve the quality, while
lower numbers reduce it.
"""
MATCH_ADJUSTMENT_MASK = 0x0000ffff

"""
public static final int MATCH_ADJUSTMENT_NORMAL:
Quality adjustment applied to the category of match that signifies
the default, base value; higher numbers improve the quality while
lower numbers reduce it.
"""
MATCH_ADJUSTMENT_NORMAL = 0x00008000

"""
public static final int MATCH_CATEGORY_EMPTY:
The filter matched an intent that had no data specified.
"""
MATCH_CATEGORY_EMPTY = 0x00100000

"""
public static final int MATCH_CATEGORY_HOST:
The filter matched an intent with the same data URI scheme and
authority host.
"""
MATCH_CATEGORY_HOST = 0x00300000

"""
public static final int MATCH_CATEGORY_MASK:
The part of a match constant that describes the category of match
that occurred.  May be either MATCH_CATEGORY_EMPTY,
MATCH_CATEGORY_SCHEME, MATCH_CATEGORY_SCHEME_SPECIFIC_PART,
MATCH_CATEGORY_HOST, MATCH_CATEGORY_PORT,
MATCH_CATEGORY_PATH, or MATCH_CATEGORY_TYPE.  Higher
values indicate a better match.
"""
MATCH_CATEGORY_MASK = 0x0fff0000

"""
public static final int MATCH_CATEGORY_PATH:
The filter matched an intent with the same data URI scheme,
authority, and path.
"""
MATCH_CATEGORY_PATH = 0x00500000

"""
public static final int MATCH_CATEGORY_PORT:
The filter matched an intent with the same data URI scheme and
authority host and port.
"""
MATCH_CATEGORY_PORT = 0x00400000

"""
public static final int MATCH_CATEGORY_SCHEME:
The filter matched an intent with the same data URI scheme.
"""
MATCH_CATEGORY_SCHEME = 0x00200000

"""
public static final int MATCH_CATEGORY_SCHEME_SPECIFIC_PART:
The filter matched an intent with the same data URI scheme and
scheme specific part.
"""
MATCH_CATEGORY_SCHEME_SPECIFIC_PART = 0x00580000

"""
public static final int MATCH_CATEGORY_TYPE:
The filter matched an intent with the same data MIME type.
"""
MATCH_CATEGORY_TYPE = 0x00600000

"""
public static final int NO_MATCH_ACTION:
The filter didn't match due to different actions.
"""
NO_MATCH_ACTION = 0xfffffffd

"""
public static final int NO_MATCH_CATEGORY:
The filter didn't match because it required one or more categories
that were not in the Intent.
"""
NO_MATCH_CATEGORY = 0xfffffffc

"""
public static final int NO_MATCH_DATA:
The filter didn't match due to different data URIs.
"""
NO_MATCH_DATA = 0xfffffffe

"""
public static final int NO_MATCH_TYPE:
The filter didn't match due to different MIME types.
"""
NO_MATCH_TYPE = 0xffffffff

"""
public static final int SYSTEM_HIGH_PRIORITY:
The filter setPriority(int) value at which system high-priority
receivers are placed; that is, receivers that should execute before
application code. Applications should never use filters with this or
higher priorities.See also:setPriority(int)
"""
SYSTEM_HIGH_PRIORITY = 0x000003e8

"""
public static final int SYSTEM_LOW_PRIORITY:
The filter setPriority(int) value at which system low-priority
receivers are placed; that is, receivers that should execute after
application code. Applications should never use filters with this or
lower priorities.See also:setPriority(int)
"""
SYSTEM_LOW_PRIORITY = 0xfffffc18


class IntentFilter(Object, IParcelable):
    """
    Structured description of Intent values to be matched. An IntentFilter
    can match against actions, categories, and data (either via its type,
    scheme, and/or path) in an Intent. It also includes a "priority" value
    which is used to order multiple matching filters.
    """

    """
    public static final Creator<IntentFilter> CREATOR:
    """
    CREATOR = type(
        'IntentFilterCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: IntentFilter()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * IntentFilter)()
        })()

    @overload
    def __init__(self):
        super(IntentFilter, self).__init__()
        self._action = []
        self._categories = []
        self._dataauthorities = []
        self._datapath = []
        self._datascheme = []
        self._datassp = []
        self._datatype = []
        self.setPriority(0)
        pass

    @__init__.adddef('str')
    def IntentFilter(self, action):
        """
        :param action: String.
        """
        self.__init__()
        self.addAction(action)
        pass

    @__init__.adddef('str', 'str')
    def IntentFilter(self, action, dataType):
        """
        :param action: String.
        :param dataType: String.
        """
        self.__init__(action)
        self.addDataType(dataType)
        pass

    @__init__.adddef('IntentFilter')
    def IntentFilter(self, o):
        """
        :param o: IntentFilter.
        """
        pass

    def actionsIterator(self):
        """
        Return an iterator over the filter's actions.  If there are no
        actions, returns null.
        :return: Iterator<String>.
        """
        return iter(self._action)

    def addAction(self, action):
        """
        Add a new Intent action to match against.  If any actions are included
        in the filter, then an Intent's action must be one of those values for
        it to match.  If no actions are included, the Intent action is ignored.
        :param action: String: Name of the action to match, such as
        Intent.ACTION_VIEW.
        """
        if not self.hasAction(action):
            self._action.append(action)

    def addCategory(self, category):
        """
        Add a new Intent category to match against.  The semantics of
        categories is the opposite of actions -- an Intent includes the
        categories that it requires, all of which must be included in the
        filter in order to match.  In other words, adding a category to the
        filter has no impact on matching unless that category is specified in
        the intent.
        :param category: String: Name of category to match, such as
        Intent.CATEGORY_EMBED.
        """
        if not self.hasCategory(category):
            self._categories.append(category)

    def addDataAuthority(self, host, port):
        """
        Add a new Intent data authority to match against.  The filter must
        include one or more schemes (via addDataScheme(String)) for the
        authority to be considered.  If any authorities are included in the
        filter, then an Intent's data must match one of them.  If no
        authorities are included, then only the scheme must match.  Note: host
        name in the Android framework is case-sensitive, unlike formal RFC
        host names.  As a result, you should always write your host names with
        lower case letters, and any host names you receive from outside of
        Android should be converted to lower case before supplying them here.
        :param host: String: The host part of the authority to match.  May
        start with a single '*' to wildcard the front of the host name.
        :param port: String: Optional port part of the authority to match.  If
        null, any port is allowed.
        See also:
        matchData(String, String, Uri)
        addDataScheme(String)
        """
        authority = AuthorityEntry(host, port)
        if authority not in self._dataauthorities:
            self._dataauthorities.append(authority)

    def addDataPath(self, path, type_):
        """
        Add a new Intent data path to match against.  The filter must include
        one or more schemes (via addDataScheme(String)) and one or more
        authorities (via addDataAuthority(String, String)) for the path to be
        considered.  If any paths are included in the filter, then an Intent's
        data must match one of them.  If no paths are included, then only the
        scheme/authority must match.  The path given here can either be a
        literal that must directly match or match against a prefix, or it can
        be a simple globbing pattern. If the latter, you can use '*' anywhere
        in the pattern to match zero or more instances of the previous
        character, '.' as a wildcard to match any character, and '\' to escape
        the next character.
        :param path: String: Either a raw string that must exactly match the
        file path, or a simple pattern, depending on type.
        :param type: int: Determines how path will be compared to determine a
        match: either PatternMatcher.PATTERN_LITERAL,
        PatternMatcher.PATTERN_PREFIX, or PatternMatcher.PATTERN_SIMPLE_GLOB.
        See also:
        matchData(String, String,Uri)
        addDataScheme(String)
        addDataAuthority(String, String)
        """
        patternmatcher = PatternMatcher(path, type_)
        if not self.hasDataPath(patternmatcher):
            self._datapath.append(patternmatcher)

    def addDataScheme(self, scheme):
        """
        Add a new Intent data scheme to match against.  If any schemes are
        included in the filter, then an Intent's data must be either one of
        these schemes or a matching data type.  If no schemes are included,
        then an Intent will match only if it includes no data.  Note: scheme
        matching in the Android framework is case-sensitive, unlike formal RFC
        schemes.  As a result, you should always write your schemes with lower
        case letters, and any schemes you receive from outside of Android
        should be converted to lower case before supplying them here.
        :param scheme: String: Name of the scheme to match, such as "http".
        See also: matchData(String, String, Uri)
        """
        if not self.hasDataScheme(scheme):
            self._datascheme.append(scheme)

    def addDataSchemeSpecificPart(self, ssp, datatype):
        """
        Add a new Intent data "scheme specific part" to match against.  The
        filter must include one or more schemes (via addDataScheme(String))
        for the scheme specific part to be considered.  If any scheme specific
        parts are included in the filter, then an Intent's data must match one
        of them.  If no scheme specific parts are included, then only the
        scheme must match.  The "scheme specific part" that this matches
        against is the string returned by Uri.getSchemeSpecificPart. For Uris
        that contain a path, this kind of matching is not generally of
        interest, since addDataAuthority(String, String) and
        addDataPath(String, int) can provide a better mechanism for matching
        them.  However, for Uris that do not contain a path, the authority and
        path are empty, so this is the only way to match against the
        non-scheme part.
        :param ssp: String: Either a raw string that must exactly match the
        scheme specific part path, or a simple pattern, depending on type.
        :param datatype: int: Determines how ssp will be compared to determine a
        match: either PatternMatcher.PATTERN_LITERAL,
        PatternMatcher.PATTERN_PREFIX, or PatternMatcher.PATTERN_SIMPLE_GLOB.
        See also: matchData(String, String, Uri)addDataScheme(String)
        """
        patternmatcher = PatternMatcher(ssp, datatype)
        if not self.hasDataSchemeSpecificPart(patternmatcher):
            self._datassp.append(patternmatcher)

    def addDataType(self, type_):
        """
        Add a new Intent data type to match against.  If any types are
        included in the filter, then an Intent's data must be either one of
        these types or a matching scheme.  If no data types are included, then
        an Intent will only match if it specifies no data.  Note: MIME type
        matching in the Android framework is case-sensitive, unlike formal RFC
        MIME types.  As a result, you should always write your MIME types with
        lower case letters, and any MIME types you receive from outside of
        Android should be converted to lower case before supplying them
        here.Throws IntentFilter.MalformedMimeTypeException if the given MIME
        type is not syntactically correct.
        :param type_: String: Name of the data type to match, such as
        "vnd.android.cursor.dir/person".
        :raises: IntentFilter.MalformedMimeTypeException
        See also: matchData(String, String, Uri)
        """
        if type_:
            if Intent.normalizeMimeType(type_) != type_:
                raise Exception('Malformed Mime Type')
            if not self.hasDataType(type_):
                self._datatype.append(type_)

    def authoritiesIterator(self):
        """
        Return an iterator over the filter's data authorities.
        :return: Iterator<IntentFilter.AuthorityEntry>.
        """
        return iter(self._dataauthorities)

    def categoriesIterator(self):
        """
        Return an iterator over the filter's categories.
        :return: Iterator<String>. Iterator if this filter has categories or
        null if none.
        """
        return iter(self._categories)

    def countActions(self):
        """
        Return the number of actions in the filter.
        :return: int.
        """
        return len(self._action)

    def countCategories(self):
        """
        Return the number of categories in the filter.
        :return: int.
        """
        return len(self._categories)

    def countDataAuthorities(self):
        """
        Return the number of data authorities in the filter.
        :return: int.
        """
        return len(self._dataauthorities)

    def countDataPaths(self):
        """
        Return the number of data paths in the filter.
        :return: int.
        """
        return len(self._datapath)

    def countDataSchemeSpecificParts(self):
        """
        Return the number of data scheme specific parts in the filter.
        :return: int.
        """
        return len(self._datassp)

    def countDataSchemes(self):
        """
        Return the number of data schemes in the filter.
        :return: int.
        """
        return len(self._datascheme)

    def countDataTypes(self):
        """
        Return the number of data types in the filter.
        :return: int.
        """
        return len(self._datatype)

    @classmethod
    def create(self, action, dataType):
        """
        Create a new IntentFilter instance with a specified action and MIME
        type, where you know the MIME type is correctly formatted.  This
        catches the IntentFilter.MalformedMimeTypeException exception that the
        constructor can call and turns it into a runtime exception.
        :param action: String: The action to match, such as Intent.ACTION_VIEW.
        :param dataType: String: The type to match, such as
        "vnd.android.cursor.dir/person".
        :return: IntentFilter. A new IntentFilter for the given action and
        type.
        See also: IntentFilter(String, String)
        """
        dataType = Intent.normalizeMimeType(dataType)
        return IntentFilter(action, dataType)

    def describeContents(self):
        """
        Describe the kinds of special objects contained in this Parcelable
        instance's marshaled representation. For example, if the object will
        include a file descriptor in the output of writeToParcel(Parcel, int),
        the return value of this method must include the
        CONTENTS_FILE_DESCRIPTOR bit.
        :return: int. a bitmask indicating the set of special object types
        marshaled by this Parcelable object instance.
        """
        return 0

    def dump(self, du, prefix):
        """
        :param du: Printer
        :param prefix: String
        """
        pass

    def getAction(self, index):
        """
        Return an action in the filter.
        :param index: int
        :return: String.
        """
        return self._action[index]

    def getCategory(self, index):
        """
        Return a category in the filter.
        :param index: int
        :return: String.
        """
        return self._categories[index]

    def getDataAuthority(self, index):
        """
        Return a data authority in the filter.
        :param index: int
        :return: IntentFilter.AuthorityEntry.
        """
        return self._dataauthorities[index]

    def getDataPath(self, index):
        """
        Return a data path in the filter.
        :param index: int
        :return: PatternMatcher.
        """
        return self._datapath[index]

    def getDataScheme(self, index):
        """
        Return a data scheme in the filter.
        :param index: int
        :return: String.
        """
        return self._datascheme[index]

    def getDataSchemeSpecificPart(self, index):
        """
        Return a data scheme specific part in the filter.
        :param index: int
        :return: PatternMatcher.
        """
        return self._datassp[index]

    def getDataType(self, index):
        """
        Return a data type in the filter.
        :param index: int
        :return: String.
        """
        return self._datatype[index]

    def getPriority(self):
        """
        Return the priority of this filter.
        :return: int. The priority of the filter.
        See also: setPriority(int)
        """
        return self._priority

    def hasAction(self, action):
        """
        Is the given action included in the filter?  Note that if the filter
        does not include any actions, false will always be returned.
        :param action: String: The action to look for.
        :return: boolean. True if the action is explicitly mentioned in the
        filter.
        """
        if action.startswith('android.app.action'): action = action.replace('.app.', '.intent.')
        return action in self._action

    def hasCategory(self, category):
        """
        Is the given category included in the filter?
        :param category: String: The category that the filter supports.
        :return: boolean. True if the category is explicitly mentioned in the
        filter.
        """
        if category.startswith('android.app.category'): category = category.replace('.app.', '.intent.')
        return category in self._categories

    def hasDataAuthority(self, data):
        """
        Is the given data authority included in the filter?  Note that if the
        filter does not include any authorities, false will always be returned.
        :param data: Uri: The data whose authority is being looked for.
        :return: boolean. Returns true if the data string matches an authority
        listed in the filter.
        """
        return data in self._dataauthorities

    def hasDataPath(self, data):
        """
        Is the given data path included in the filter?  Note that if the
        filter does not include any paths, false will always be returned.
        :param data: String: The data path to look for.  This is without the
        scheme prefix.
        :return: boolean. True if the data string matches a path listed in the
        filter.
        """
        return any(map(lambda x: x.match(data), self._datapath))

    def hasDataScheme(self, scheme):
        """
        Is the given data scheme included in the filter?  Note that if the
        filter does not include any scheme, false will always be returned.
        :param scheme: String: The data scheme to look for.
        :return: boolean. True if the scheme is explicitly mentioned in the
        filter.
        """
        return scheme in self._datascheme

    def hasDataSchemeSpecificPart(self, data):
        """
        Is the given data scheme specific part included in the filter?  Note
        that if the filter does not include any scheme specific parts, false
        will always be returned.
        :param data: String: The scheme specific part that is being looked for.
        :return: boolean. Returns true if the data string matches a scheme
        specific part listed in the filter.
        """
        return any(map(lambda x: x.match(data), self._datassp))

    def hasDataType(self, datatype):
        """
        Is the given data type included in the filter?  Note that if the
        filter does not include any type, false will always be returned.
        :param datatype: String: The data type to look for.
        :return: boolean. True if the type is explicitly mentioned in the
        filter.
        """
        return datatype in self._datatype

    @overload('str', 'str', 'str', 'Uri', 'set', 'str')
    def match(self, action, mimetype, scheme, data, categories, logTag):
        """
        Test whether this filter matches the given intent data.  A match is
        only successful if the actions and categories in the Intent match
        against the filter, as described in IntentFilter; in that case, the
        match result returned will be as per matchData(String, String, Uri).
        :param action: String: The intent action to match against
        (Intent.getAction).
        :param mimetype: String: The intent type to match against
        (Intent.resolveType()).
        :param scheme: String: The data scheme to match against
        (Intent.getScheme()).
        :param data: Uri: The data URI to match against (Intent.getData()).
        :param categories: Set: The categories to match against
        (Intent.getCategories()).
        :param logTag: String: Tag to use in debugging messages.
        :return: int. Returns either a valid match constant (a combination of
        MATCH_CATEGORY_MASK and MATCH_ADJUSTMENT_MASK), or one of the error
        codes NO_MATCH_TYPE if the type didn't match, NO_MATCH_DATA if the
        scheme/path didn't match, NO_MATCH_ACTION if the action didn't match,
        or NO_MATCH_CATEGORY if one or more categories didn't match.
        See also:
        matchData(String, String, Uri)
        Intent.getAction()
        Intent.resolveType(ContentResolver)
        Intent.getScheme()
        Intent.getData()
        Intent.getCategories()
        """
        bFlag = self.matchAction(action)
        if not bFlag: return NO_MATCH_ACTION
        retDataVal = self.matchData(mimetype, scheme, data)
        if retDataVal in (NO_MATCH_DATA, NO_MATCH_TYPE): return retDataVal
        retCatVal = self.matchCategories(categories or set())
        if not retCatVal: return retDataVal
        return NO_MATCH_CATEGORY

    @match.adddef('ContentResolver', 'Intent', 'bool', 'str')
    def match(self, resolver, intent, resolve, logTag):
        """
        Test whether this filter matches the given intent.
        :param resolver: ContentResolver
        :param intent: Intent: The Intent to compare against.
        :param resolve: boolean: If true, the intent's type will be resolved
        by calling Intent.resolveType(); otherwise a simple match against
        Intent.type will be performed.
        :param logTag: String: Tag to use in debugging messages.
        :return: int. Returns either a valid match constant (a combination of
        MATCH_CATEGORY_MASK and MATCH_ADJUSTMENT_MASK), or one of the error
        codes NO_MATCH_TYPE if the type didn't match, NO_MATCH_DATA if the
        scheme/path didn't match, NO_MATCH_ACTION if the action didn't match,
        or NO_MATCH_CATEGORY if one or more categories didn't match.
        See also: match(String, String, String, android.net.Uri, Set, String)
        """
        action = intent.getAction()
        mimetype = intent.resolveType(resolver) if resolve else intent.getType()
        scheme = intent.getScheme()
        data = intent.getData()
        categories = intent.getCategories()
        return self.match(action, mimetype, scheme, data, categories, logTag)

    def matchAction(self, action):
        """
        Match this filter against an Intent's action.  If the filter does not
        specify any actions, the match will always fail.
        :param action: String: The desired action to look for.
        :return: boolean. True if the action is listed in the filter.
        """
        if action:
            return self.hasAction(action)
        return not bool(self.countActions())

    def matchCategories(self, categories):
        """
        Match this filter against an Intent's categories.  Each category in
        the Intent must be specified by the filter; if any are not in the
        filter, the match fails.
        :param categories: Set: The categories included in the intent, as
        returned by Intent.getCategories().
        :return: String. If all categories match (success), null; else the
        name of the first category that didn't match.
        """
        it = itertools.dropwhile(lambda x: self.hasCategory(x), sorted(categories))
        try:
            return it.next()
        except:
            pass
        # diff = filter(lambda x: not self.hasCategory(x), categories)
        # if diff:
        #     return diff[0]

    def matchData(self, mimetype, scheme, data):
        """
        Match this filter against an Intent's data (type, scheme and path). If
        the filter does not specify any types and does not specify any
        schemes/paths, the match will only succeed if the intent does not also
        specify a type or data.  If the filter does not specify any schemes,
        it will implicitly match intents with no scheme, or the schemes
        "content:" or "file:" (basically performing a MIME-type only match).
        If the filter does not specify any MIME types, the Intent also must
        not specify a MIME type.  Be aware that to match against an authority,
        you must also specify a base scheme the authority is in.  To match
        against a data path, both a scheme and authority must be specified.
        If the filter does not specify any types or schemes that it matches
        against, it is considered to be empty (any authority or data path
        given is ignored, as if it were empty as well).  Note: MIME type, Uri
        scheme, and host name matching in the Android framework is
        case-sensitive, unlike the formal RFC definitions. As a result, you
        should always write these elements with lower case letters, and
        normalize any MIME types or Uris you receive from outside of Android
        to ensure these elements are lower case before supplying them here.
        :param mimetype: String: The desired data type to look for, as returned by
        Intent.resolveType().
        :param scheme: String: The desired data scheme to look for, as
        returned by Intent.getScheme().
        :param data: Uri: The full data string to match against, as supplied
        in Intent.data.
        :return: int. Returns either a valid match constant (a combination of
        MATCH_CATEGORY_MASK and MATCH_ADJUSTMENT_MASK), or one of the error
        codes NO_MATCH_TYPE if the type didn't match or NO_MATCH_DATA if the
        scheme/path didn't match.
        See also: match(ContentResolver, Intent, boolean, String)
        """
        assert isinstance(mimetype, basestring)
        assert isinstance(scheme, basestring)
        assert not data or isinstance(data, Uri)
        retValue = MATCH_ADJUSTMENT_NORMAL
        bFlag1 = not self.countDataTypes() and \
                 not (self.countDataSchemes() or self.countDataPaths())
        bFlag2 = not (mimetype or data)
        if bFlag1 and bFlag2:
            retValue |= MATCH_CATEGORY_TYPE
            return retValue + 1

        bFlag1 = not self.countDataTypes()
        bFlag2 = not mimetype
        if (bFlag1 and bFlag2): return retValue

        if mimetype and self.countDataTypes():
            isPattern = lambda x: x.endswith('/*')
            patterns = filter(isPattern, self.typesIterator())
            nopatterns = filter(lambda x: not isPattern(x), self.typesIterator())
            if isPattern(mimetype):
                bflag = mimetype in patterns
                bflag = bflag or itertools.dropwhile(lambda x: not x.startswith(mimetype[:-1]), nopatterns)
            else:
                bflag = mimetype in nopatterns
                bflag = bflag or itertools.dropwhile(lambda x: not mimetype.startswith(x[:-1]), patterns)
            if not isinstance(bflag, bool):
                try:
                    bflag.next()
                    bflag = True
                except:
                    bflag = False
            if not bflag:
                return NO_MATCH_TYPE
            retValue |= MATCH_CATEGORY_TYPE
            retValue += 1
        bFlag1 = not self.countDataSchemes()
        if bFlag1:
            bFlag2 = not scheme or scheme in ('content', 'file')
            bflag = (bFlag1 and bFlag2)
        else:
            if scheme:
                it = itertools.dropwhile(lambda x: x == scheme, self.schemesIterator())
                try:
                    it.next()
                    bflag = True
                except:
                    bflag = False
            else:
                bflag = False

        if not bflag:
            return NO_MATCH_DATA
        retValue |= MATCH_CATEGORY_SCHEME
        retValue += 1
        if not data:
            retValue |= MATCH_CATEGORY_EMPTY
            return retValue + 1
        ssp = data.getSchemeSpecificPart()
        if ssp:
            bFlag = self.hasDataSchemeSpecificPart(ssp)
            if bFlag:
                retValue |= MATCH_CATEGORY_SCHEME_SPECIFIC_PART
                return retValue + 1

        if not bFlag and data.isOpaque(): return NO_MATCH_DATA

        answ = self.matchDataAuthority(data)
        if answ == NO_MATCH_DATA: return answ
        retValue |= answ
        retValue += 1
        path = data.getPath()
        if path:
            bFlag = self.hasDataPath(path)
            if not bFlag: return NO_MATCH_DATA
            retValue |= MATCH_CATEGORY_PATH
            retValue += 1
        return retValue

    def matchDataAuthority(self, data):
        """
        Match this intent filter against the given Intent data.  This ignores
        the data scheme -- unlike matchData(String, String, Uri), the
        authority will match regardless of whether there is a matching scheme.
        :param data: Uri: The data whose authority is being looked for.
        :return: int. Returns either MATCH_CATEGORY_HOST, MATCH_CATEGORY_PORT,
        NO_MATCH_DATA.
        """
        it = itertools.dropwhile(lambda x: x.match(data) == NO_MATCH_DATA, self.authoritiesIterator())
        try:
            authority = it.next()
            return authority.match(data)
        except:
            return NO_MATCH_DATA
        # host, port = data.getHost(), data.getPort()
        # if self.countDataAuthorities():
        #     for dataAuthority in self.authoritiesIterator():
        #         dataHost, dataPort = dataAuthority
        #         if host == dataHost:
        #             retval = MATCH_CATEGORY_HOST
        #             if not dataPort:
        #                 return retval
        #         elif port == dataPort:
        #             return retval | MATCH_CATEGORY_PORT
        #     else:
        #         return NO_MATCH_DATA
        # return 0x0000000

    def pathsIterator(self):
        """
        Return an iterator over the filter's data paths.
        :return: Iterator<PatternMatcher>.
        """
        return iter(self._datapath)

    def readFromXml(self, parser):
        """
        :param parser: XmlPullParser
        :raises: XmlPullParserExceptionIOException
        """
        NS_MAP = "xmlns:map"
        for fcomponent in parser:
            xmlns = fcomponent.attrib.pop(NS_MAP)
            androidns = xmlns['android']
            if fcomponent.tag == 'data':
                host = port = None
                for key, value in fcomponent.attrib.items():
                    key = key.replace('{%s}' % androidns, 'android:')
                    if key == 'android:mimeType':
                        self.addDataType(value)
                    elif key == 'android:scheme':
                        self.addDataScheme(value)
                    elif key == 'android:ssp':
                        self.addDataSchemeSpecificPart(value, PatternMatcher.PATTERN_LITERAL)
                    elif key == 'android:sspPrefix':
                        self.addDataSchemeSpecificPart(value, PatternMatcher.PATTERN_PREFIX)
                    elif key == 'android:sspPattern':
                        self.addDataSchemeSpecificPart(value, PatternMatcher.PATTERN_SIMPLE_GLOB)
                    elif key == 'android:host':
                        host = value
                    elif key == 'android:port':
                        port = int(value)
                    elif key == 'android:path':
                        self.addDataPath(value, PatternMatcher.PATTERN_LITERAL)
                    elif key == 'android:pathPrefix':
                        self.addDataPath(value, PatternMatcher.PATTERN_PREFIX)
                    elif key == 'android:pathPattern':
                        self.addDataPath(value, PatternMatcher.PATTERN_SIMPLE_GLOB)
                    elif key == 'android:pathAdvancedPattern':
                        self.addDataPath(value, PatternMatcher.PATTERN_ADVANCED_GLOB)
                if host: self.addDataAuthority(host, port)
            else:
                key = '{%s}%s' % (androidns, 'name')
                value = fcomponent.get(key)
                if fcomponent.tag == 'action':
                    self.addAction(value)
                else:
                    self.addCategory(value)

    def schemeSpecificPartsIterator(self):
        """
        Return an iterator over the filter's data scheme specific parts.
        :return: Iterator<PatternMatcher>.
        """
        return iter(self._datassp)

    def schemesIterator(self):
        """
        Return an iterator over the filter's data schemes.
        :return: Iterator<String>.
        """
        return iter(self._datascheme)

    def setPriority(self, priority):
        """
        Modify priority of this filter.  This only affects receiver filters.
        The priority of activity filters are set in XML and cannot be changed
        programmatically. The default priority is 0. Positive values will be
        before the default, lower values will be after it. Applications should
        use a value that is larger than SYSTEM_LOW_PRIORITY and smaller than
        SYSTEM_HIGH_PRIORITY .
        :param priority: int: The new priority value.
        See also:
        getPriority()
        SYSTEM_LOW_PRIORITY
        SYSTEM_HIGH_PRIORITY
        """
        priority = min(SYSTEM_HIGH_PRIORITY, max(SYSTEM_LOW_PRIORITY, priority))
        self._priority = priority

    def typesIterator(self):
        """
        Return an iterator over the filter's data types.
        :return: Iterator<String>.
        """
        return iter(self._datatype)

    def writeToParcel(self, dest, flags):
        """
        Flatten this object in to a Parcel.
        :param dest: Parcel: The Parcel in which the object should be written.
        :param flags: int: Additional flags about how the object should be
        written. May be 0 or Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        pass

    def writeToXml(self, serializer):
        """
        Write the contents of the IntentFilter as an XML stream.
        :param serializer: XmlSerializer
        :raises IOException:
        """
        outstr = '<intent-filter>\n'
        for action in self.actionsIterator():
            outstr += '    ' + '<action android:name="%s" />\n' % action
        for category in self.categoriesIterator():
            outstr += '    ' + '<category android:name="%s" />\n' % category
        for mimetype in self.typesIterator():
            outstr += '    ' + '<data android:mimeType="%s" />\n' % mimetype
        for scheme in self.schemesIterator():
            outstr += '    ' + '<data android:scheme="%s" />\n' % scheme
        for ssp, ssptype in self.schemeSpecificPartsIterator():
            ssptype = ['ssp', 'sspprefix', 'sspPattern'][ssptype]
            outstr += '    ' + '<data android:%s="%s" />\n' % (ssptype, ssp)
        for host, port in self.authoritiesIterator():
            datastr = '    ' + '<data android:host="%s" />\n' % host
            if port:
                datastr = datastr.replace('/>', 'android:port="%s" />' % port)
            outstr += datastr
        for path, pathtype in self.pathsIterator():
            pathtype = ['path', 'pathprefix', 'pathPattern'][pathtype]
            outstr += '    ' + '<data android:%s="%s" />\n' % (pathtype, path)
        outstr += '</intent-filter>'
        serializer.write(outstr)
        serializer.seek(0)


class AuthorityEntry(Object):
    """
    This is an entry for a single authority in the Iterator returned by
    IntentFilter.authoritiesIterator() .
    """
    def __init__(self, host, port):
        """
        :param host: String.
        :param port: String.
        """
        self._host = host
        self._port = port

    def equals(self, obj):
        """
        Indicates whether some other object is "equal to" this one.  The
        equals method implements an equivalence relation on non-null object
        references: It is reflexive: for any non-null reference value x,
        x.equals(x) should return true. It is symmetric: for any non-null
        reference values x and y, x.equals(y) should return true if and only
        if y.equals(x) returns true. It is transitive: for any non-null
        reference values x, y, and z, if x.equals(y) returns true and
        y.equals(z) returns true, then x.equals(z) should return true. It is
        consistent: for any non-null reference values x and y, multiple
        invocations of x.equals(y) consistently return true or consistently
        return false, provided no information used in equals comparisons on
        the objects is modified. For any non-null reference value x,
        x.equals(null) should return false.  The equals method for class
        Object implements the most discriminating possible equivalence
        relation on objects; that is, for any non-null reference values x and
        y, this method returns true if and only if x and y refer to the same
        object (x == y has the value true).  Note that it is generally
        necessary to override the hashCode method whenever this method is
        overridden, so as to maintain the general contract for the hashCode
        method, which states that equal objects must have equal hash codes.
        :param obj: Object: the reference object with which to compare.
        :return: boolean. true if this object is the same as the obj argument;
        false otherwise.
        """
        return self.getHost() == obj.getHost() and self.getPort() == obj.getPort()

    def getHost(self):
        """
        :return: String.
        """
        return self._host

    def getPort(self):
        """
        :return: int.
        """
        return self._port

    def match(self, data):
        """
        Determine whether this AuthorityEntry matches the given data Uri. Note
        that this comparison is case-sensitive, unlike formal RFC host names.
        You thus should always normalize to lower-case.
        :param data: Uri: The Uri to match.
        :return: int. Returns either IntentFilter.NO_MATCH_DATA,
        IntentFilter.MATCH_CATEGORY_PORT, or IntentFilter.MATCH_CATEGORY_HOST.
        """
        host, port = data.getHost(), data.getPort()
        answ = 0
        if host and host == self.getHost():
            answ |= MATCH_CATEGORY_HOST
        if port and port == self.getPort():
            answ |= MATCH_CATEGORY_PORT
        return answ or NO_MATCH_DATA