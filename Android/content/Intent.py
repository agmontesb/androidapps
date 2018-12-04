# -*- coding: utf-8 -*-
from Android.Uri import Uri
import urllib
import urlparse

# Standar Activity Actions
ACTION_MAIN = 'android.intent.action.MAIN'
ACTION_VIEW = 'android.intent.action.VIEW'
ACTION_ATTACH_DATA = 'android.intent.action.DATA'
ACTION_EDIT = 'android.intent.action.EDIT'
ACTION_PICK = 'android.intent.action.PICK'
ACTION_CHOOSER = 'android.intent.action.CHOOSER'
ACTION_GET_CONTENT = 'android.intent.action.CONTENT'
ACTION_DIAL = 'android.intent.action.DIAL'
ACTION_CALL = 'android.intent.action.CALL'
ACTION_SEND = 'android.intent.action.SEND'
ACTION_SENDTO = 'android.intent.action.SENDTO'
ACTION_ANSWER = 'android.intent.action.ANSWER'
ACTION_INSERT = 'android.intent.action.INSERT'
ACTION_DELETE = 'android.intent.action.DELETE'
ACTION_RUN = 'android.intent.action.RUN'
ACTION_SYNC = 'android.intent.action.SYNC'
ACTION_PICK_ACTIVITY = 'android.intent.action.ACTIVITY'
ACTION_SEARCH = 'android.intent.action.SEARCH'
ACTION_WEB_SEARCH = 'android.intent.action.SEARCH'
ACTION_FACTORY_TEST = 'android.intent.action.TEST'

# Standard Categories
CATEGORY_DEFAULT = 'android.intent.category.DEFAULT'
CATEGORY_BROWSABLE = 'android.intent.category.BROWSABLE'
CATEGORY_TAB = 'android.intent.category.TAB'
CATEGORY_ALTERNATIVE = 'android.intent.category.ALTERNATIVE'
CATEGORY_SELECTED_ALTERNATIVE = 'android.intent.category.SELECTED_ALTERNATIVE'
CATEGORY_LAUNCHER = 'android.intent.category.LAUNCHER'
CATEGORY_INFO = 'android.intent.category.INFO'
CATEGORY_HOME = 'android.intent.category.HOME'
CATEGORY_PREFERENCE = 'android.intent.category.PREFERENCE'
CATEGORY_TEST = 'android.intent.category.TEST'
CATEGORY_CAR_DOCK = 'android.intent.category.CAR_DOCK'
CATEGORY_DESK_DOCK = 'android.intent.category.DESK_DOCK'
CATEGORY_LE_DESK_DOCK = 'android.intent.category.LE_DESK_DOCK'
CATEGORY_HE_DESK_DOCK = 'android.intent.category.HE_DESK_DOCK'
CATEGORY_CAR_MODE = 'android.intent.category.CAR_MODE'
CATEGORY_APP_MARKET = 'android.intent.category.APP_MARKET'
CATEGORY_VR_HOME = 'android.intent.category.VR_HOME'

# Standard Extra Data
EXTRA_ALARM_COUNT = 'android.intent.extra.ALARM_COUNT'
EXTRA_BCC = 'android.intent.extra.BCC'
EXTRA_CC = 'android.intent.extra.CC'
EXTRA_CHANGED_COMPONENT_NAME = 'android.intent.extra.CHANGED_COMPONENT_NAME'
EXTRA_DATA_REMOVED = 'android.intent.extra.DATA_REMOVED'
EXTRA_DOCK_STATE = 'android.intent.extra.DOCK_STATE'
EXTRA_DOCK_STATE_HE_DESK = 'android.intent.extra.DOCK_STATE_HE_DESK'
EXTRA_DOCK_STATE_LE_DESK = 'android.intent.extra.DOCK_STATE_LE_DESK'
EXTRA_DOCK_STATE_CAR = 'android.intent.extra.DOCK_STATE_CAR'
EXTRA_DOCK_STATE_DESK = 'android.intent.extra.DOCK_STATE_DESK'
EXTRA_DOCK_STATE_UNDOCKED = 'android.intent.extra.DOCK_STATE_UNDOCKED'
EXTRA_DONT_KILL_APP = 'android.intent.extra.DONT_KILL_APP'
EXTRA_EMAIL = 'android.intent.extra.EMAIL'
EXTRA_INITIAL_INTENTS = 'android.intent.extra.INITIAL_INTENTS'
EXTRA_INTENT = 'android.intent.extra.INTENT'
EXTRA_KEY_EVENT = 'android.intent.extra.KEY_EVENT'
EXTRA_ORIGINATING_URI = 'android.intent.extra.ORIGINATING_URI'
EXTRA_PHONE_NUMBER = 'android.intent.extra.PHONE_NUMBER'
EXTRA_REFERRER = 'android.intent.extra.REFERRER'
EXTRA_REMOTE_INTENT_TOKEN = 'android.intent.extra.REMOTE_INTENT_TOKEN'
EXTRA_REPLACING = 'android.intent.extra.REPLACING'
EXTRA_SHORTCUT_ICON = 'android.intent.extra.SHORTCUT_ICON'
EXTRA_SHORTCUT_ICON_RESOURCE = 'android.intent.extra.SHORTCUT_ICON_RESOURCE'
EXTRA_SHORTCUT_INTENT = 'android.intent.extra.SHORTCUT_INTENT'
EXTRA_STREAM = 'android.intent.extra.STREAM'
EXTRA_SHORTCUT_NAME = 'android.intent.extra.SHORTCUT_NAME'
EXTRA_SUBJECT = 'android.intent.extra.SUBJECT'
EXTRA_TEMPLATE = 'android.intent.extra.TEMPLATE'
EXTRA_TEXT = 'android.intent.extra.TEXT'
EXTRA_TITLE = 'android.intent.extra.TITLE'
EXTRA_UID = 'android.intent.extra.UID'

# Flags
FLAG_GRANT_READ_URI_PERMISSION = 0x00000001
FLAG_GRANT_WRITE_URI_PERMISSION = 0x00000002
FLAG_FROM_BACKGROUND = 0x00000004
FLAG_DEBUG_LOG_RESOLUTION = 0x00000008
FLAG_EXCLUDE_STOPPED_PACKAGES = 0x00000010
FLAG_INCLUDE_STOPPED_PACKAGES = 0x00000020
FLAG_GRANT_PERSISTABLE_URI_PERMISSION = 0x00000040
FLAG_GRANT_PREFIX_URI_PERMISSION = 0x00000080
FLAG_ACTIVITY_MATCH_EXTERNAL = 0x00000800
FLAG_RECEIVER_REGISTERED_ONLY = 0x40000000
FLAG_RECEIVER_REPLACE_PENDING = 0x20000000
FLAG_RECEIVER_FOREGROUND = 0x10000000
FLAG_RECEIVER_NO_ABORT = 0x08000000
FLAG_ACTIVITY_CLEAR_TOP = 0x04000000
FLAG_ACTIVITY_FORWARD_RESULT = 0x02000000
FLAG_ACTIVITY_PREVIOUS_IS_TOP = 0x01000000
FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS = 0x00800000
FLAG_ACTIVITY_BROUGHT_TO_FRONT = 0x00400000
FLAG_RECEIVER_VISIBLE_TO_INSTANT_APPS = 0x00200000
FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY = 0x00100000
FLAG_ACTIVITY_NEW_DOCUMENT = 0x00080000
FLAG_ACTIVITY_NO_USER_ACTION = 0x00040000
FLAG_ACTIVITY_REORDER_TO_FRONT = 0x00020000
FLAG_ACTIVITY_NO_ANIMATION = 0x00010000
FLAG_ACTIVITY_CLEAR_TASK = 0x00008000
FLAG_ACTIVITY_TASK_ON_HOME = 0x00004000
FLAG_ACTIVITY_RETAIN_IN_RECENTS = 0x00002000
FLAG_ACTIVITY_LAUNCH_ADJACENT = 0x00001000

URI_INTENT_SCHEME = 0x00000001
URI_ANDROID_APP_SCHEME = 0x00000002
URI_ALLOW_UNSAFE = 0x00000004

def marshallExtras(extras):
    def itemType(item):
        bTypes = (int, float, bool, str)
        typeCode = ('i', 'f', 'b', 'S')
        type_ = type(item)
        npos = bTypes.index(type_)
        return typeCode[npos]

    strobj = {}
    stack = extras.items()
    while stack:
        key, value = stack.pop()
        vprefix = value
        if isinstance(vprefix, (list, tuple)):
            vprefix = vprefix[0]
        elif isinstance(vprefix, dict):
            ikeys = vprefix.keys()
            stack.append(('keys.' + key, ikeys))
            for k, item in enumerate(ikeys):
                ivalue = vprefix[item]
                stack.append((('p%s.%s') % (k, key), ivalue))
            continue
        else:
            if isinstance(value, bool): value = int(value)
        prefix = itemType(vprefix)
        strobj['%s.%s' % (prefix, key)] = value
    output = urllib.urlencode(strobj, doseq=True).replace('&', ';')
    return output

def unmarshalExtras(marshalExras):
    def typeItem(item):
        bTypes = (int, float, bool, str)
        typeCode = ('i', 'f', 'b', 'S')
        npos = typeCode.index(item)
        return bTypes[npos]

    output = marshalExras
    salida = {}
    output = output.replace(';', '&')
    output = urlparse.parse_qs(output)
    for key, value in output.items():
        prefix, key = key.split('.', 1)
        members = salida.setdefault(key, [])
        for item in value:
            tipo = typeItem(prefix)
            item = tipo(item)
            members.append(item)
        if len(members) == 1: salida[key] = members[0]
    edict = sorted(filter(lambda x:x.startswith('keys'), salida))
    for itemkey in edict:
        keys = salida.pop(itemkey)
        key = itemkey.split('.', 1)[-1]
        values = len(keys)*[None]
        evals = filter(lambda x:x.endswith(key), salida)
        for itemval in evals:
            value = salida.pop(itemval)
            pos =  int(itemval.split('.', 1)[0][1:])
            values[pos] = value
        salida[key] = dict(zip(keys, values))
    return salida


class Intent(object):
    def __init__(self, action='', uri=None, component=None):
        self._categories = set()
        self._flags = None
        self._action = None
        self._extras = dict()
        self._component = None
        self._data = None
        self._mimetype = None
        self._selector = None
        if component: self.setComponent(component)
        if action: self.setAction(action)
        if uri: self.setData(uri)

    def addCategory(self, category):
        """Add a new category to the intent."""
        self._categories.add(category)
        return self

    def addFlags(self, flags):
        """Add additional flags to the intent (or with existing flags value)."""
        self._flags |= flags
        return self

    def clone(self):
        """Creates and returns a copy of this object."""
        pass

    def cloneFilter(self):
        """Make a clone of only the parts of the Intent that are relevant for filter matching: the action, data, type, component, and categories."""
        pass

    # def createChooser(self, target, title, sender):
    #     """Convenience function for creating a ACTION_CHOOSER Intent."""
    #     pass
    # def createChooser(self, target, title):
    #     """Convenience function for creating a ACTION_CHOOSER Intent."""
    #     pass
    # def describeContents(self):
    #     """Describe the kinds of special objects contained in this Parcelable instance's marshaled representation."""
    #     pass
    # def fillIn(self, other, flags):
    #     """Copy the contents of other in to this object, but only where fields are not defined by this object."""
    #     pass

    def filterEquals(self, other):
        """Determine if two intents are the same for the purposes of intent resolution (filtering)."""
        bflag = self.getAction() == other.getAction()
        bflag = bflag and self.getData() == other.getData()
        bflag = bflag and self.getCategories() == other.getCategories()
        return bflag

    def filterHashCode(self):
        """Generate hash code that matches semantics of filterEquals()."""
        pass

    def getAction(self):
        """Retrieve the general action to be performed, such as ACTION_VIEW."""
        return self._action

    # def getBooleanArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getBooleanExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getBundleExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getByteArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getByteExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass

    def getCategories(self):
        """Return the set of all categories in the intent."""
        return self._categories or None

    # def getCharArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    #
    # def getCharExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getCharSequenceArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getCharSequenceArrayListExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getCharSequenceExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getClipData(self):
    #     """Return the ClipData associated with this Intent."""
    #     pass

    def getComponent(self):
        """Retrieve the concrete component associated with the intent."""
        component = self._component
        bFlag = component[0] and component[1]
        return self._component if bFlag else None

    def getData(self):
        """Retrieve data this intent is operating on."""
        return self._data

    def getDataString(self):
        """The same as getData(), but returns the URI as an encoded String."""
        data = self.getData().toString()
        return urllib.quote(data, safe='/~')

    # def getDoubleArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getDoubleExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass

    def getExtras(self):
        """Retrieves a map of extended data from the intent."""
        return self._extras

    def getFlags(self):
        """Retrieve any special flags associated with this intent."""
        return self._flags or 0

    # def getFloatArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getFloatExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getIntArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getIntExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getIntegerArrayListExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass

    # def getIntent(self, uri):
    #     """      This method was deprecated      in API level 4.    Use parseUri(String, int) instead.                                                            static                        Intent                      getIntentOld(String uri)                                                                              long[]                      getLongArrayExtra(String name)                    Retrieve extended data from the intent."""
    #     pass

    # def getLongExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass

    def getPackage(self):
        """Retrieve the application package name this Intent is limited to."""
        component = self.getComponent() or (None,)
        return component[0]

    # def getParcelableArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getParcelableArrayListExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getParcelableExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass

    def getScheme(self):
        """Return the scheme portion of the intent's data."""
        uri = self.getData() or ''
        return uri and uri.getScheme()

    def getSelector(self):
        """Return the specific selector associated with this Intent."""
        return self._selector or self

    # def getSerializableExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getShortArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getShortExtra(self, name, defaultValue):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getSourceBounds(self):
    #     """Get the bounds of the sender of this intent, in screen coordinates."""
    #     pass
    # def getStringArrayExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getStringArrayListExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass
    # def getStringExtra(self, name):
    #     """Retrieve extended data from the intent."""
    #     pass

    def getType(self):
        """Retrieve any explicit MIME type included in the intent."""
        return self._mimetype

    def hasCategory(self, category):
        """Check if a category exists in the intent."""
        return category in self._categories

    def hasExtra(self, name):
        """Returns true if an extra value is associated with the given name."""
        return name in self._extras

    # def hasFileDescriptors(self):
    #     """Returns true if the Intent's extras contain a parcelled file descriptor."""
    #     pass
    @classmethod
    def makeMainActivity(cls, mainActivity):
        """Create an intent to launch the main (root) activity of a task."""
        return Intent(component=mainActivity)

    @classmethod
    def makeMainSelectorActivity(cls, selectorAction, selectorCategory):
        """Make an Intent for the main activity of an application, without specifying a specific activity to run but giving a selector to find the activity."""
        intent = Intent(action=selectorAction)
        return intent.addCategory(selectorCategory)

    @classmethod
    def makeRestartActivityTask(cls, mainActivity):
        """Make an Intent that can be used to re-launch an application's task in its base state."""
        pass

    @classmethod
    def normalizeMimeType(cls, type_):
        """Normalize a MIME data type."""
        if type_:
            type_ = type_.split(';', 1)[0]
            type_ = type_.lower()
        return type_

    @classmethod
    def parseIntent(cls, resources, parser, attrs):
        """Parses the "intent" element (and its children) from XML and instantiates an Intent object."""
        pass

    @classmethod
    def parseUri(cls, uri, flags):
        """Create an intent from a URI."""
        if flags & URI_ANDROID_APP_SCHEME:
            assert uri.getScheme() == 'android-app'
            packageName = uri.getAuthority()
            pathSegments = uri.getPathSegments()
            query = uri.getQuery()
            fragment = uri.getFragment()
            data = None
            if pathSegments:
                dataScheme, dataHost, dataPath = pathSegments + (3 - len(pathSegments)) * ['', ]
                data = urlparse.urlunparse((dataScheme, dataHost, dataPath, None, query, None))
            defaultAction = 'android.intent.action.VIEW' if data else 'android.intent.action.MAIN'
            parse_fragment = dict(flags=[0], action=[defaultAction],
                                  classname=[None], type=[None])
            if fragment:
                fragment = '&'.join(fragment.split(';')[1:-1])
                parse_fragment.update(urlparse.parse_qs(fragment))
            action = parse_fragment.pop('action')[0]
            flags = parse_fragment.pop('flags')[0]
            mimeType = parse_fragment.pop('type')[0]
            className = parse_fragment.pop('classname')[0]
            extras = parse_fragment
            intent = Intent(action=action)
            intent = intent.setPackage(packageName)
            if className:
                intent = intent.setClassName(packageName, className)
            if data:
                intent = intent.setData(data)
            if flags:
                intent = intent.setFlags(flags)
            if mimeType:
                intent = intent.setType(mimeType)
            if extras:
                extras = urllib.urlencode(extras, doseq=True).replace('&', ';')
                extras = unmarshalExtras(extras)
                intent = intent.replaceExtras(extras)
        return intent

    # def putCharSequenceArrayListExtra(self, name, value):
    #     """Add extended data to the intent."""
    #     pass

    # def putExtra(self, name, value):
    #     """Add extended data to the intent."""
    #     pass
    #
    # def putExtras(self, src):
    #     """Copy all extras in 'src' in to this intent."""
    #     pass

    def putExtras(self, extras):
        """Add a set of extended data to the intent."""
        self._extras.update(extras)

    # def putIntegerArrayListExtra(self, name, value):
    #     """Add extended data to the intent."""
    #     pass
    # def putParcelableArrayListExtra(self, name, value):
    #     """Add extended data to the intent."""
    #     pass
    # def putStringArrayListExtra(self, name, value):
    #     """Add extended data to the intent."""
    #     pass
    # def readFromParcel(self, in):
    #     """Remove a category from an intent."""
    #     pass

    def removeExtra(self, name):
        """Remove extended data from the intent."""
        self._extras.pop(name)

    def removeFlags(self, flags):
        """Remove these flags from the intent."""
        self._flags = self._flags ^ flags

    # def replaceExtras(self, src):
    #     """Completely replace the extras in the Intent with the extras in the given Intent."""
    #     pass

    def replaceExtras(self, extras):
        """Completely replace the extras in the Intent with the given Bundle of extras."""
        self._extras = extras
        return self

    def resolveActivity(self, pm):
        """Return the Activity component that should be used to handle this intent."""
        if self.getComponent():
            return self.getComponent()

        pass

    def resolveActivityInfo(self, pm, flags):
        """Resolve the Intent into an ActivityInfo describing the activity that should execute the intent."""
        pass

    def resolveType(self, resolver):
        """Return the MIME data type of this intent."""
        uri = self.getData()
        if not uri: return ''
        scheme = uri.getScheme()
        contentProvider = uri.getAuthority()
        # TODO: Como no he implementado el resolver, acá se infiere el tipo
        if scheme == 'content':
            tailpath = uri.getLastPathSegment()
            try:
                int(tailpath)
            except:
                return "vnd.android.cursor.dir/*"
            return "vnd.android.cursor.item/*"

    # def resolveType(self, resolver):
    #     """Return the MIME data type of this intent."""
    #     pass

    def resolveTypeIfNeeded(self, resolver):
        """Return the MIME data type of this intent, only if it will be needed for intent resolution."""
        pass

    def setAction(self, action):
        """Set the general action to be performed."""
        self._action = action or None

    # def setClass(self, packageContext, cls):
    #     """Convenience for calling setComponent(ComponentName) with the name returned by a Class object."""
    #     pass

    def setClassName(self, packageName, className):
        """Convenience for calling setComponent(ComponentName) with an explicit application package name and class name."""
        self._component = (packageName, className)

    # def setClassName(self, packageContext, className):
    #     """Convenience for calling setComponent(ComponentName) with an explicit class name."""
    #     pass
    # def setClipData(self, clip):
    #     """Set a ClipData associated with this Intent."""
    #     pass

    def setComponent(self, component):
        """(Usually optional) Explicitly set the component to handle the intent."""
        if component is not None:
            assert isinstance(component, tuple) and len(component) == 2, 'The component is a tuple (packageName, className)'
        self._component = component
        return self

    def setData(self, data):
        """Set the data this intent is operating on."""
        assert isinstance(data, Uri), 'Not a Uri'
        self._data = data
        return  self

    def setDataAndNormalize(self, data):
        """Normalize and set the data this intent is operating on."""
        data = urllib.quote(data, safe='/~')
        return self.setData(data)

    def setDataAndType(self, data, type_):
        """(Usually optional) Set the data for the intent along with an explicit MIME data type."""
        self.setData(data)
        return self.setType(type_)


    def setDataAndTypeAndNormalize(self, data, type_):
        """(Usually optional) Normalize and set both the data Uri and an explicit MIME data type."""
        self.setDataAndNormalize(data)
        return self.setType(type_)

    # def setExtrasClassLoader(self, loader):
    #     """Sets the ClassLoader that will be used when unmarshalling any Parcelable values from the extras of this Intent."""
    #     pass

    def setFlags(self, flags):
        """Set special flags controlling how this intent is handled."""
        self._flags = flags
        return self

    def setPackage(self, packageName):
        """(Usually optional) Set an explicit application package name that limits the components this Intent will resolve to."""
        pckName, className = self._component or ('', '')
        self._component = (packageName, className)
        return self

    def setSelector(self, selector):
        """Set a selector for this Intent."""
        assert isinstance(selector, Intent)
        self._selector = selector

    # def setSourceBounds(self, r):
    #     """Set the bounds of the sender of this intent, in screen coordinates."""
    #     pass

    def setType(self, type_):
        """Set an explicit MIME data type."""
        self._mimetype = type_
        return self

    def setTypeAndNormalize(self, type_):
        """Normalize and set an explicit MIME data type."""
        type_ = Intent.normalizeMimeType(type_)
        return self.setType(type_)

    def toString(self):
        """Returns a string representation of the object."""
        self.__str__()

    def toURI(self, flags):
        """This method was deprecated in API level 4. Use toUri(int) instead. String toUri(int flags) Convert this Intent into a String holding a URI representation of it."""
        if flags & URI_ANDROID_APP_SCHEME:
            scheme = 'android-app'
            netloc = self.getPackage()
            if self.getData():
                urlScheme, urlHost, urlPath, params, query = self._data[:-1]
                if urlPath: urlPath = urlPath[1:]
                path = filter(lambda x: x != '', (urlScheme, urlHost, urlPath))
                path = '/'.join(path)
            else:
                params = query = path = ''
                path = '/' + path
            defaultAction = ('android.intent.action.VIEW', 'android.intent.action.MAIN')
            action = self.getAction() if self.getAction() not in defaultAction else None
            parse_fragment = [('action', action),
                              ('flags', self.getFlags() or None),
                              ('type', self.getType()),
                              ('classname', self.getComponent()[1] or None)]
            parse_fragment = filter(lambda x: x[1] is not None, parse_fragment)
            fragment = urllib.urlencode(parse_fragment, doseq=True).replace('&', ';')
            extras = marshallExtras(self.getExtras())
            if fragment or extras:
                fragmentbase = ['Intent', 'end']
                if fragment:
                    fragmentbase.insert(-1, fragment)
                if extras:
                    fragmentbase.insert(-1, extras)
                fragment = ';'.join(fragmentbase)
            return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))
        pass

    def writeToParcel(self, out, flags):
        """Flatten this object in to a Parcel."""
        pass

