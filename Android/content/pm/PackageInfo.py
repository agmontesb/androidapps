# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/PackageInfo"""
from Android import overload, Object
from Android.content.pm.ComponentInfo import ComponentInfo
from Android.interface.IParcelable import IParcelable, ICreator

"""
public static final int INSTALL_LOCATION_AUTO:
Constant corresponding to auto in the
R.attr.installLocation attribute.
"""
INSTALL_LOCATION_AUTO = 0x00000000

"""
public static final int INSTALL_LOCATION_INTERNAL_ONLY:
Constant corresponding to internalOnly in the
R.attr.installLocation attribute.
"""
INSTALL_LOCATION_INTERNAL_ONLY = 0x00000001

"""
public static final int INSTALL_LOCATION_PREFER_EXTERNAL:
Constant corresponding to preferExternal in the
R.attr.installLocation attribute.
"""
INSTALL_LOCATION_PREFER_EXTERNAL = 0x00000002

"""
public static final int REQUESTED_PERMISSION_GRANTED:
Flag for requestedPermissionsFlags: the requested permission
is currently granted to the application.
"""
REQUESTED_PERMISSION_GRANTED = 0x00000002


class PackageInfo(Object, IParcelable):
    """
    Overall information about the contents of a package. This corresponds to 
    all of the information collected from AndroidManifest.xml.
    """

    """
    public static final Creator<PackageInfo> CREATOR:
    
    """
    CREATOR = type(
        'PackageInfoCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: PackageInfo()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * PackageInfo)()
        })()

    @overload
    def __init__(self):
        super(PackageInfo, self).__init__()
        """
        public ActivityInfo[] activities:
        Array of all <activity> tags included under <application>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_ACTIVITIES was set.
        """
        self.activities = []

        """
        public ApplicationInfo applicationInfo:
        Information collected from the <application> tag, or null if
        there was none.
        """
        self.applicationInfo = 0

        """
        public int baseRevisionCode:
        The revision number of the base APK for this package, as specified by the
        <manifest> tag's revisionCode attribute.
        """
        self.baseRevisionCode = 0

        """
        public ConfigurationInfo[] configPreferences:
        Application specified preferred configuration
        <uses-configuration> tags included under <manifest>,
        or null if there were none. This is only filled in if the flag
        PackageManager.GET_CONFIGURATIONS was set.
        """
        self.configPreferences = []

        """
        public FeatureGroupInfo[] featureGroups:
        Groups of features that this application has requested.
        Each group contains a set of features that are required.
        A device must match the features listed in reqFeatures and one
        or more FeatureGroups in order to have satisfied the feature 
        requirement.See also:FeatureInfo.FLAG_REQUIRED
        """
        self.featureGroups = []

        """
        public long firstInstallTime:
        The time at which the app was first installed.  Units are as
        per System.currentTimeMillis().
        """
        self.firstInstallTime = 0L

        """
        public int[] gids:
        All kernel group-IDs that have been assigned to this package.
        This is only filled in if the flag PackageManager.GET_GIDS was set.
        """
        self.gids = []

        """
        public int installLocation:
        The install location requested by the package. From the
        R.attr.installLocation attribute, one of
        INSTALL_LOCATION_AUTO, INSTALL_LOCATION_INTERNAL_ONLY,
        INSTALL_LOCATION_PREFER_EXTERNAL
        """
        self.installLocation = INSTALL_LOCATION_AUTO

        """
        public InstrumentationInfo[] instrumentation:
        Array of all <instrumentation> tags included under <manifest>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_INSTRUMENTATION was set.
        """
        self.instrumentation = []

        """
        public long lastUpdateTime:
        The time at which the app was last updated.  Units are as
        per System.currentTimeMillis().
        """
        self.lastUpdateTime = 0L

        """
        public String packageName:
        The name of this package.  From the <manifest> tag's "name"
        attribute.
        """
        self.packageName = ''

        """
        public PermissionInfo[] permissions:
        Array of all <permission> tags included under <manifest>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_PERMISSIONS was set.
        """
        self.permissions = []

        """
        public ProviderInfo[] providers:
        Array of all <provider> tags included under <application>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_PROVIDERS was set.
        """
        self.providers = []

        """
        public ActivityInfo[] receivers:
        Array of all <receiver> tags included under <application>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_RECEIVERS was set.
        """
        self.receivers = []

        """
        public FeatureInfo[] reqFeatures:
        Features that this application has requested.See 
        also:FeatureInfo.FLAG_REQUIRED
        """
        self.reqFeatures = []

        """
        public String[] requestedPermissions:
        Array of all <uses-permission> tags included under <manifest>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_PERMISSIONS was set.  This list includes
        all permissions requested, even those that were not granted or known
        by the system at install time.
        """
        self.requestedPermissions = []

        """
        public int[] requestedPermissionsFlags:
        Array of flags of all <uses-permission> tags included under <manifest>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_PERMISSIONS was set.  Each value matches
        the corresponding entry in requestedPermissions, and will have
        the flag REQUESTED_PERMISSION_GRANTED set as appropriate.
        """
        self.requestedPermissionsFlags = []

        """
        public ServiceInfo[] services:
        Array of all <service> tags included under <application>,
        or null if there were none.  This is only filled in if the flag
        PackageManager.GET_SERVICES was set.
        """
        self.services = []

        """
        public String sharedUserId:
        The shared user ID name of this package, as specified by the <manifest>
        tag's sharedUserId
        attribute.
        """
        self.sharedUserId = ''

        """
        public int sharedUserLabel:
        The shared user ID label of this package, as specified by the <manifest>
        tag's sharedUserLabel
        attribute.
        """
        self.sharedUserLabel = 0

        """
        public Signature[] signatures:

        This field was deprecated
        in API level 28.
        use signingInfo instead

        Array of all signatures read from the package file. This is only filled
        in if the flag PackageManager.GET_SIGNATURES was set. A package
        must be signed with at least one certificate which is at position zero.
        The package can be signed with additional certificates which appear as
        subsequent entries.

        Note: Signature ordering is not guaranteed to be
        stable which means that a package signed with certificates A and B is
        equivalent to being signed with certificates B and A. This means that
        in case multiple signatures are reported you cannot assume the one at
        the first position to be the same across updates.

        Deprecated This has been replaced by the
        signingInfo field, which takes into
        account signing certificate rotation.  For backwards compatibility in
        the event of signing certificate rotation, this will return the oldest
        reported signing certificate, so that an application will appear to
        callers as though no rotation occurred.
        """
        self.signatures = []

        """
        public SigningInfo signingInfo:
        Signing information read from the package file, potentially
        including past signing certificates no longer used after signing
        certificate rotation.  This is only filled in if
        the flag PackageManager.GET_SIGNING_CERTIFICATES was set.

        Use this field instead of the deprecated signatures field.
        See SigningInfo for more information on its contents.
        """
        self.signingInfo = 0

        """
        public String[] splitNames:
        The names of any installed split APKs for this package.
        """
        self.splitNames = []

        """
        public int[] splitRevisionCodes:
        The revision number of any split APKs for this package, as specified by
        the <manifest> tag's
        revisionCode
        attribute. Indexes are a 1:1 mapping against splitNames.
        """
        self.splitRevisionCodes = []

        """
        public int versionCode:

        This field was deprecated
        in API level 28.
        Use getLongVersionCode() instead, which includes both
        this and the additional
        versionCodeMajor attribute.
        The version number of this package, as specified by the <manifest>
        tag's versionCode
        attribute.
        See also:getLongVersionCode()
        """
        self.versionCode = 0

        """
        public String versionName:
        The version name of this package, as specified by the <manifest>
        tag's versionName attribute.
        """
        self.versionName = ''

        """
        private PersistableBundle _unclasifiedFields:
        The fields declare in <manifest> that are not asociated to a flag or
        an attribute
        """
        self._unclassifiedFields = None
        pass

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

    def getLongVersionCode(self):
        """
        Return versionCode and versionCodeMajor combined together as a single 
        long value.  The versionCodeMajor is placed in the upper 32 bits.
        :return: long.
        """
        pass

    def setLongVersionCode(self, longVersionCode):
        """
        Set the full version code in this PackageInfo, updating versionCode 
        with the lower bits.
        :param longVersionCode: long
        See also: getLongVersionCode()
        """
        pass

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
        return self.__str__()

    def writeToParcel(self, dest, parcelableFlags):
        """
        Flatten this object in to a Parcel.
        :param dest: Parcel: The Parcel in which the object should be written.
        :param parcelableFlags: int: Additional flags about how the object 
        should be written. May be 0 or 
        Parcelable.PARCELABLE_WRITE_RETURN_VALUE.
        """
        dest.writeParcelableArray(self.activities, 0)
        dest.writeParcelableArray(self.applicationInfo, 0)
        dest.writeInt(self.baseRevisionCode)
        dest.writeParcelableArray(self.configPreferences, 0)
        dest.writeParcelableArray(self.featureGroups, 0)
        dest.writeLong(self.firstInstallTime)
        dest.writeIntArray(self.gids)
        dest.writeInt(self.installLocation)
        dest.writeParcelableArray(self.instrumentation, 0)
        dest.writeLong(self.lastUpdateTime)
        dest.writeString(self.packageName)
        dest.writeParcelableArray(self.permissions, 0)
        dest.writeParcelableArray(self.providers, 0)
        dest.writeParcelableArray(self.receivers, 0)
        dest.writeParcelableArray(self.reqFeatures, 0)
        dest.writeParcelableArray(self.requestedPermissions, 0)
        dest.writeIntArray(self.requestedPermissionsFlags)
        dest.writeParcelableArray(self.services, 0)
        dest.writeString(self.sharedUserId)
        dest.writeInt(self.sharedUserLabel)
        dest.writeParcelableArray(self.signatures, 0)
        dest.writeInt(self.signingInfo)
        dest.writeStringArray(self.splitNames)
        dest.writeIntArray(self.splitRevisionCodes)
        dest.writeInt(self.versionCode)
        dest.writeString(self.versionName)
        pass

    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return PackageInfo:
        '''
        self.activities = src.readParcelableArray(None)
        self.applicationInfo = src.readParcelableArray(None)
        self.baseRevisionCode = src.readInt()
        self.configPreferences = src.readParcelableArray(None)
        self.featureGroups = src.readParcelableArray(None)
        self.firstInstallTime = src.readLong()
        self.gids = src.createIntArray()
        self.installLocation = src.readInt()
        self.instrumentation = src.readParcelableArray(None)
        self.lastUpdateTime = src.readLong()
        self.packageName = src.readString()
        self.permissions = src.readParcelableArray(None)
        self.providers = src.readParcelableArray(None)
        self.receivers = src.readParcelableArray(None)
        self.reqFeatures = src.readParcelableArray(None)
        self.requestedPermissions = src.readParcelableArray(None)
        self.requestedPermissionsFlags = src.createIntArray()
        self.services = src.readParcelableArray(None)
        self.sharedUserId = src.readString()
        self.sharedUserLabel = src.readInt()
        self.signatures = src.readParcelableArray(None)
        self.signingInfo = src.readInt()
        self.splitNames = src.createStringArray()
        self.splitRevisionCodes = src.createIntArray()
        self.versionCode = src.readInt()
        self.versionName = src.readString()
        return self