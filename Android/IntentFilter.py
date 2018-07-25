# -*- coding: utf-8 -*-
import Intent
from Android.Uri import Uri


PATTERN_LITERAL = 0x00000000
PATTERN_PREFIX = 0x00000001
PATTERN_SIMPLE_GLOB = 0x00000002

MATCH_ADJUSTMENT_MASK = 0x0000ffff
MATCH_ADJUSTMENT_NORMAL = 0x00008000
MATCH_CATEGORY_EMPTY = 0x00100000
MATCH_CATEGORY_HOST = 0x00300000
MATCH_CATEGORY_MASK = 0x0fff0000
MATCH_CATEGORY_PATH = 0x00500000
MATCH_CATEGORY_PORT = 0x00400000
MATCH_CATEGORY_SCHEME = 0x00200000
MATCH_CATEGORY_SCHEME_SPECIFIC_PART = 0x00580000
MATCH_CATEGORY_TYPE = 0x00600000
NO_MATCH_ACTION = 0xfffffffd
NO_MATCH_CATEGORY = 0xfffffffc
NO_MATCH_DATA = 0xfffffffe
NO_MATCH_TYPE = 0xffffffff
SYSTEM_HIGH_PRIORITY = 0x000003e8
SYSTEM_LOW_PRIORITY = 0xfffffc18


class IntentFilter(object):
    def __init__(self, action=None, dataType=None):
        self._action = []
        self._categories = []
        self._dataauthorities = []
        self._datapath = []
        self._datascheme = []
        self._datassp = []
        self._datatype = []
        if action:
            self.addAction(action)
            if dataType:
                self.addDataType(dataType)

    def actionsIterator(self):
        """Return an iterator over the filter's actions"""
        return iter(self._action)

    def addAction(self, action):
        """Add a new Intent action to match against"""
        if not self.hasAction(action):
            self._action.append(action)

    def addCategory(self, category):
        """Add a new Intent category to match against"""
        if not self.hasCategory(category):
            self._categories.append(category)

    def addDataAuthority(self, host, port):
        """Add a new Intent data authority to match against"""
        if (host, port) not in self._dataauthorities:
            self._dataauthorities.append((host, port))

    def addDataPath(self, path, type_):
        """Add a new Intent data path to match against"""
        if not self.hasDataPath((path, type_)):
            self._datapath.append((path, type_))

    def addDataScheme(self, scheme):
        """Add a new Intent data scheme to match against"""
        if not self.hasDataScheme(scheme):
            self._datascheme.append(scheme)

    def addDataSchemeSpecificPart(self, ssp, datatype):
        """Add a new Intent data "scheme specific part" to match against"""
        if not self.hasDataSchemeSpecificPart((ssp, datatype)):
            self._datassp.append((ssp, datatype))

    def addDataType(self, type_):
        """Add a new Intent data type to match against"""
        if type_:
            if Intent.Intent.normalizeMimeType(type_) != type_:
                raise Exception('Malformed Mime Type')
            if not self.hasDataType(type_):
                self._datatype.append(type_)

    def authoritiesIterator(self):
        """Return an iterator over the filter's data authorities"""
        return iter(self._dataauthorities)

    def categoriesIterator(self):
        """Return an iterator over the filter's categories"""
        return iter(self._categories)

    def countActions(self):
        """Return the number of actions in the filter"""
        return len(self._action)

    def countCategories(self):
        """Return the number of categories in the filter"""
        return len(self._categories)

    def countDataAuthorities(self):
        """Return the number of data authorities in the filter"""
        return len(self._dataauthorities)

    def countDataPaths(self):
        """Return the number of data paths in the filter"""
        return len(self._datapath)

    def countDataSchemeSpecificParts(self):
        """Return the number of data scheme specific parts in the filter"""
        return len(self._datassp)

    def countDataSchemes(self):
        """Return the number of data schemes in the filter"""
        return len(self._datascheme)

    def countDataTypes(self):
        """Return the number of data types in the filter"""
        return len(self._datatype)

    def create(self, action, dataType):
        """Create a new IntentFilter instance with a specified action and MIME
        type, where you know the MIME type is correctly formatted"""
        dataType = Intent.normalizeMimeType(dataType)
        return IntentFilter(action, dataType)

    def describeContents(self):
        """Describe the kinds of special objects contained in this Parcelable
        instance's marshaled representation"""
        pass

    def dump(self, du, prefix):
        """Return an action in the filter"""
        pass

    def getAction(self, index):
        """Return a category in the filter"""
        return self._action[index]

    def getCategory(self, index):
        """Return a category in the filter"""
        return self._categories[index]

    def getDataAuthority(self, index):
        """Return a data authority in the filter"""
        return self._dataauthorities[index]

    def getDataPath(self, index):
        """Return a data path in the filter"""
        return self._datapath[index]

    def getDataScheme(self, index):
        """Return a data scheme in the filter"""
        return self._datascheme[index]

    def getDataSchemeSpecificPart(self, index):
        """Return a data scheme specific part in the filter"""
        return self._datassp[index]

    def getDataType(self, index):
        """Return a data type in the filter"""
        return self._datatype[index]

    def getPriority(self):
        """Return the priority of this filter"""
        pass

    def hasAction(self, action):
        """Is the given action included in the filter?  Note that if the filter
        does not include any actions, false will always be returned"""
        if action.startswith('android.app.action'): action = action.replace('.app.', '.intent.')
        return action in self._action

    def hasCategory(self, category):
        """Is the given category included in the filter?"""
        if category.startswith('android.app.category'): category = category.replace('.app.', '.intent.')
        return category in self._categories

    def hasDataAuthority(self, data):
        """Is the given data authority included in the filter?  Note that if the
        filter does not include any authorities, false will always be returned"""
        return data in self._dataauthorities

    def hasDataPath(self, data):
        """Is the given data path included in the filter?  Note that if the
        filter does not include any paths, false will always be returned"""
        return data in self._datapath

    def hasDataScheme(self, scheme):
        """Is the given data scheme included in the filter?  Note that if the
        filter does not include any scheme, false will always be returned"""
        return scheme in self._datascheme

    def hasDataSchemeSpecificPart(self, data):
        """Is the given data scheme specific part included in the filter?  Note that if the
        filter does not include any scheme specific parts, false will always be
        returned"""
        return data in self._datassp

    def hasDataType(self, datatype):
        """Is the given data type included in the filter?  Note that if the filter
        does not include any type, false will always be returned"""
        return datatype in self._datatype

    def match(self, action, mimetype, scheme, data, categories, logTag):
        """Test whether this filter matches the given intent data"""
        bFlag = self.matchAction(action)
        if not bFlag: return NO_MATCH_ACTION
        retDataVal = self.matchData(mimetype, scheme, data)
        if retDataVal in (NO_MATCH_DATA, NO_MATCH_TYPE): return retDataVal
        retCatVal = self.matchCategories(categories or set())
        if not retCatVal: return retDataVal
        return NO_MATCH_CATEGORY

    def matchIntent(self, resolver, intent, resolve, logTag):
        """Test whether this filter matches the given intent"""
        action = intent.getAction()
        mimetype = intent.resolveType(resolver) if resolve else intent.getType()
        scheme = intent.getScheme()
        data = intent.getData()
        categories = intent.getCategories()
        return self.match(action, mimetype, scheme, data, categories, logTag)

    def matchAction(self, action):
        """Match this filter against an Intent's action"""
        return bool(self.countActions()) and self.hasAction(action)

    def matchCategories(self, categories):
        """Match this filter against an Intent's categories"""
        diff = filter(lambda x: not self.hasCategory(x), categories)
        if diff:
            return diff[0]

    def matchData(self, mimetype, scheme, data):
        """Match this filter against an Intent's data (type, scheme and path)"""
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
            mimetype = mimetype.split('/')
            for dataType in self.typesIterator():
                dataType = dataType.split('/')
                bFlag1 = dataType[0] == mimetype[0]
                bFlag2 = dataType[1] == mimetype[1]
                bFlag2 = bFlag2 or dataType[1] == '*' or mimetype[1] == '*'
                bFlag = bFlag1 and bFlag2
                if bFlag: break
            else:
                return NO_MATCH_TYPE
            retValue |= MATCH_CATEGORY_TYPE
            retValue += 1

        bFlag1 = not self.countDataSchemes()
        bFlag2 = not scheme or scheme in ('content', 'file')
        if not(bFlag1 and bFlag2): return NO_MATCH_DATA

        if scheme and self.countDataSchemes():
            for dataScheme in self.schemesIterator():
                bFlag = scheme == dataScheme
                if bFlag:break
            else:
                return NO_MATCH_DATA
            retValue |= MATCH_CATEGORY_SCHEME
            retValue += 1
        if not data:
            retValue |= MATCH_CATEGORY_EMPTY
            return retValue + 1
        ssp = data.getSchemeSpecificPart()
        if ssp and self.countDataSchemeSpecificParts():
            for dataSSP in self.schemeSpecificPartsIterator():
                theSSP, eqtype = dataSSP
                if eqtype == PATTERN_LITERAL:
                    bFlag = ssp == theSSP
                elif eqtype == PATTERN_PREFIX:
                    bFlag = ssp.startswith(theSSP)
                elif eqtype == PATTERN_SIMPLE_GLOB:
                    pass
                if bFlag:break
            else:
                bFlag = False
            if bFlag:
                retValue |= MATCH_CATEGORY_SCHEME_SPECIFIC_PART
                return retValue + 1
        if not bFlag and data.isOpaque(): return NO_MATCH_DATA

        answ = self.matchDataAuthority(data)
        if answ == NO_MATCH_DATA: return answ
        retValue |= answ
        retValue += 1
        path = data.getPath()
        if self.countDataPaths():
            for dataPath in self.pathsIterator():
                thePath, eqtype = dataPath
                if eqtype == PATTERN_LITERAL:
                    bFlag = path == thePath
                elif eqtype == PATTERN_PREFIX:
                    bFlag = path.startswith(thePath)
                elif eqtype == PATTERN_SIMPLE_GLOB:
                    pass
                if bFlag:break
            else:
                return NO_MATCH_DATA
            retValue |= MATCH_CATEGORY_PATH
            retValue += 1
        return retValue

    def matchDataAuthority(self, data):
        """Match this intent filter against the given Intent data"""
        host, port = data.getHost(), data.getPort()
        if self.countDataAuthorities():
            for dataAuthority in self.authoritiesIterator():
                dataHost, dataPort = dataAuthority
                if host == dataHost:
                    retval = MATCH_CATEGORY_HOST
                    if not dataPort:
                        return retval
                elif port == dataPort:
                    return retval | MATCH_CATEGORY_PORT
            else:
                return NO_MATCH_DATA
        return 0x0000000

    def pathsIterator(self):
        """Return an iterator over the filter's data paths"""
        return iter(self._datapath)

    def readFromXml(self, parser):
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
                        self.addDataSchemeSpecificPart(value, PATTERN_LITERAL)
                    elif key == 'android:sspPrefix':
                        self.addDataSchemeSpecificPart(value, PATTERN_PREFIX)
                    elif key == 'android:sspPattern':
                        self.addDataSchemeSpecificPart(value, PATTERN_SIMPLE_GLOB)
                    elif key == 'android:host':
                        host = value
                    elif key == 'android:port':
                        port = int(value)
                    elif key == 'android:path':
                        self.addDataPath(value, PATTERN_LITERAL)
                    elif key == 'android:pathPrefix':
                        self.addDataPath(value, PATTERN_PREFIX)
                    elif key == 'android:pathPattern':
                        self.addDataPath(value, PATTERN_SIMPLE_GLOB)
                    elif key == 'android:pathAdvancedPattern':
                        self.addDataPath(value, PATTERN_SIMPLE_GLOB)
                if host: self.addDataAuthority(host, port)
            else:
                key = '{%s}%s' % (androidns, 'name')
                value = fcomponent.get(key)
                if fcomponent.tag == 'action':
                    self.addAction(value)
                else:
                    self.addCategory(value)

    def schemesIterator(self):
        """Return an iterator over the filter's data schemes"""
        return iter(self._datascheme)

    def schemeSpecificPartsIterator(self):
        return iter(self._datassp)

    def setPriority(self, priority):
        """Modify priority of this filter"""
        pass

    def typesIterator(self):
        """Return an iterator over the filter's data types"""
        return iter(self._datatype)

    def writeToParcel(self, dest, flags):
        """Flatten this object in to a Parcel"""
        pass

    def writeToXml(self, serializer):
        """Write the contents of the IntentFilter as an XML stream"""
        outstr = '<intent-filter>\n'
        for action in self.actionsIterator():
            outstr += '    ' + '<action android:name="%s" />\n' % action
        for category  in self.categoriesIterator():
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

