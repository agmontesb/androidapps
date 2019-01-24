# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/ApplicationInfo"""
import os

import Android
from Android import overload
from PackageItemInfo import PackageItemInfo
from Android.interface.IParcelable import IParcelable
from Android.Os.Parcel import Parcel


"""
public static final int CATEGORY_AUDIO:
Category for apps which primarily work with audio or music, such as music
players.See also:category
"""
CATEGORY_AUDIO = 0x00000001

"""
public static final int CATEGORY_GAME:
Category for apps which are primarily games.See also:category
"""
CATEGORY_GAME = 0x00000000

"""
public static final int CATEGORY_IMAGE:
Category for apps which primarily work with images or photos, such as
camera or gallery apps.See also:category
"""
CATEGORY_IMAGE = 0x00000003

"""
public static final int CATEGORY_MAPS:
Category for apps which are primarily maps apps, such as navigation apps.See 
also:category
"""
CATEGORY_MAPS = 0x00000006

"""
public static final int CATEGORY_NEWS:
Category for apps which are primarily news apps, such as newspapers,
magazines, or sports apps.See also:category
"""
CATEGORY_NEWS = 0x00000005

"""
public static final int CATEGORY_PRODUCTIVITY:
Category for apps which are primarily productivity apps, such as cloud
storage or workplace apps.See also:category
"""
CATEGORY_PRODUCTIVITY = 0x00000007

"""
public static final int CATEGORY_SOCIAL:
Category for apps which are primarily social apps, such as messaging,
communication, email, or social network apps.See also:category
"""
CATEGORY_SOCIAL = 0x00000004

"""
public static final int CATEGORY_UNDEFINED:
Value when category is undefined.See also:category
"""
CATEGORY_UNDEFINED = -1

"""
public static final int CATEGORY_VIDEO:
Category for apps which primarily work with video or movies, such as
streaming video apps.See also:category
"""
CATEGORY_VIDEO = 0x00000002

"""
public static final int FLAG_ALLOW_BACKUP:
Value for flags: set to false if the application does not wish
to permit any OS-driven backups of its data; true otherwise.

Comes from the
android:allowBackup
attribute of the <application> tag.
"""
FLAG_ALLOW_BACKUP = 0x00008000

"""
public static final int FLAG_ALLOW_CLEAR_USER_DATA:
Value for flags: default value for the corresponding ActivityInfo flag.
Comes from android:allowClearUserData of the <application> tag.
"""
FLAG_ALLOW_CLEAR_USER_DATA = 0x00000040

"""
public static final int FLAG_ALLOW_TASK_REPARENTING:
Value for flags: default value for the corresponding ActivityInfo flag.
Comes from android:allowTaskReparenting of the <application> tag.
"""
FLAG_ALLOW_TASK_REPARENTING = 0x00000020

"""
public static final int FLAG_DEBUGGABLE:
Value for flags: set to true if this application would like to
allow debugging of its
code, even when installed on a non-development system.  Comes
from android:debuggable of the <application> tag.
"""
FLAG_DEBUGGABLE = 0x00000002

"""
public static final int FLAG_EXTERNAL_STORAGE:
Value for flags: Set to true if the application is
currently installed on external/removable/unprotected storage.  Such
applications may not be available if their storage is not currently
mounted.  When the storage it is on is not available, it will look like
the application has been uninstalled (its .apk is no longer available)
but its persistent data is not removed.
"""
FLAG_EXTERNAL_STORAGE = 0x00040000

"""
public static final int FLAG_EXTRACT_NATIVE_LIBS:
When set installer extracts native libs from .apk files.
"""
FLAG_EXTRACT_NATIVE_LIBS = 0x10000000

"""
public static final int FLAG_FACTORY_TEST:
Value for flags: set to true if this application holds the
Manifest.permission.FACTORY_TEST permission and the
device is running in factory test mode.
"""
FLAG_FACTORY_TEST = 0x00000010

"""
public static final int FLAG_FULL_BACKUP_ONLY:
Value for flags: true if the application asks that only
full-data streaming backups of its data be performed even though it defines
a BackupAgent, which normally
indicates that the app will manage its backed-up data via incremental
key/value updates.
"""
FLAG_FULL_BACKUP_ONLY = 0x04000000

"""
public static final int FLAG_HARDWARE_ACCELERATED:
Value for flags: true when the application's rendering
should be hardware accelerated.
"""
FLAG_HARDWARE_ACCELERATED = 0x20000000

"""
public static final int FLAG_HAS_CODE:
Value for flags: set to true if this application has code
associated with it.  Comes
from android:hasCode of the <application> tag.
"""
FLAG_HAS_CODE = 0x00000004

"""
public static final int FLAG_INSTALLED:
Value for flags: true if the application is currently
installed for the calling user.
"""
FLAG_INSTALLED = 0x00800000

"""
public static final int FLAG_IS_DATA_ONLY:
Value for flags: true if the application only has its
data installed; the application package itself does not currently
exist on the device.
"""
FLAG_IS_DATA_ONLY = 0x01000000

"""
public static final int FLAG_IS_GAME:

This constant was deprecated
in API level 26.
use CATEGORY_GAME instead.

Value for flags: true if the application was declared to be a
game, or false if it is a non-game application.
"""
FLAG_IS_GAME = 0x02000000

"""
public static final int FLAG_KILL_AFTER_RESTORE:
Value for flags: set to false if the application must be kept
in memory following a full-system restore operation; true otherwise.
Ordinarily, during a full system restore operation each application is shut 
down
following execution of its agent's onRestore() method.  Setting this attribute 
to
false prevents this.  Most applications will not need to set this attribute.

If
android:allowBackup
is set to false or no
android:backupAgent
is specified, this flag will be ignored.

Comes from the
android:killAfterRestore
attribute of the <application> tag.
"""
FLAG_KILL_AFTER_RESTORE = 0x00010000

"""
public static final int FLAG_LARGE_HEAP:
Value for flags: true when the application has requested a
large heap for its processes.  Corresponds to
android:largeHeap.
"""
FLAG_LARGE_HEAP = 0x00100000

"""
public static final int FLAG_MULTIARCH:
Value for flags: true if code from this application will need to be
loaded into other applications' processes. On devices that support multiple
instruction sets, this implies the code might be loaded into a process that's
using any of the devices supported instruction sets.

The system might treat such applications specially, for eg., by
extracting the application's native libraries for all supported instruction
sets or by compiling the application's dex code for all supported instruction
sets.
"""
FLAG_MULTIARCH = 0x80000000

"""
public static final int FLAG_PERSISTENT:
Value for flags: set to true if this application is persistent.
Comes from android:persistent of the <application> tag.
"""
FLAG_PERSISTENT = 0x00000008

"""
public static final int FLAG_RESIZEABLE_FOR_SCREENS:
Value for flags: true when the application knows how to adjust
its UI for different screen sizes.  Corresponds to
android:resizeable.
"""
FLAG_RESIZEABLE_FOR_SCREENS = 0x00001000

"""
public static final int FLAG_RESTORE_ANY_VERSION:
Value for flags: Set to true if the application's backup
agent claims to be able to handle restore data even "from the future,"
i.e. from versions of the application with a versionCode greater than
the one currently installed on the device.  Use with caution!  By default
this attribute is false and the Backup Manager will ensure that data
from "future" versions of the application are never supplied during a restore 
operation.

If
android:allowBackup
is set to false or no
android:backupAgent
is specified, this flag will be ignored.

Comes from the
android:restoreAnyVersion
attribute of the <application> tag.
"""
FLAG_RESTORE_ANY_VERSION = 0x00020000

"""
public static final int FLAG_STOPPED:
Value for flags: true if this application's package is in
the stopped state.
"""
FLAG_STOPPED = 0x00200000

"""
public static final int FLAG_SUPPORTS_LARGE_SCREENS:
Value for flags: true when the application's window can be
increased in size for larger screens.  Corresponds to
android:largeScreens.
"""
FLAG_SUPPORTS_LARGE_SCREENS = 0x00000800

"""
public static final int FLAG_SUPPORTS_NORMAL_SCREENS:
Value for flags: true when the application's window can be
displayed on normal screens.  Corresponds to
android:normalScreens.
"""
FLAG_SUPPORTS_NORMAL_SCREENS = 0x00000400

"""
public static final int FLAG_SUPPORTS_RTL:
Value for flags: true  when the application is willing to support
RTL (right to left). All activities will inherit this value.

Set from the R.attr.supportsRtl attribute in the
activity's manifest.

Default value is false (no support for RTL).
"""
FLAG_SUPPORTS_RTL = 0x00400000

"""
public static final int FLAG_SUPPORTS_SCREEN_DENSITIES:
Value for flags: true when the application knows how to
accommodate different screen densities.  Corresponds to
android:anyDensity.
"""
FLAG_SUPPORTS_SCREEN_DENSITIES = 0x00002000

"""
public static final int FLAG_SUPPORTS_SMALL_SCREENS:
Value for flags: true when the application's window can be
reduced in size for smaller screens.  Corresponds to
android:smallScreens.
"""
FLAG_SUPPORTS_SMALL_SCREENS = 0x00000200

"""
public static final int FLAG_SUPPORTS_XLARGE_SCREENS:
Value for flags: true when the application's window can be
increased in size for extra large screens.  Corresponds to
android:xlargeScreens.
"""
FLAG_SUPPORTS_XLARGE_SCREENS = 0x00080000

"""
public static final int FLAG_SUSPENDED:
Value for flags: true if this application's package is in
the suspended state.
"""
FLAG_SUSPENDED = 0x40000000

"""
public static final int FLAG_SYSTEM:
Value for flags: if set, this application is installed in the
device's system image.
"""
FLAG_SYSTEM = 0x00000001

"""
public static final int FLAG_TEST_ONLY:
Value for flags: this is set if the application has specified
android:testOnly to be true.
"""
FLAG_TEST_ONLY = 0x00000100

"""
public static final int FLAG_UPDATED_SYSTEM_APP:
Value for flags: this is set if this application has been
installed as an update to a built-in system application.
"""
FLAG_UPDATED_SYSTEM_APP = 0x00000080

"""
public static final int FLAG_USES_CLEARTEXT_TRAFFIC:
Value for flags: true if the application may use cleartext network traffic
(e.g., HTTP rather than HTTPS; WebSockets rather than WebSockets Secure; XMPP, 
IMAP, STMP
without STARTTLS or TLS). If false, the app declares that it does not intend 
to use
cleartext network traffic, in which case platform components (e.g., HTTP 
stacks,
DownloadManager, MediaPlayer) will refuse app's requests to use cleartext
traffic. Third-party libraries are encouraged to honor this flag as well.

NOTE: WebView honors this flag for applications targeting API level 26 and up.

This flag is ignored on Android N and above if an Android Network Security 
Config is
present.

This flag comes from
android:usesCleartextTraffic of the <application> tag.
"""
FLAG_USES_CLEARTEXT_TRAFFIC = 0x08000000

"""
public static final int FLAG_VM_SAFE_MODE:
Value for flags: set to true if this application would like to
request the VM to operate under the safe mode. Comes from
android:vmSafeMode of the <application> tag.
"""
FLAG_VM_SAFE_MODE = 0x00004000

class ApplicationInfo(PackageItemInfo, IParcelable):
    """
    Information you can retrieve about a particular application. This 
    corresponds to information collected from the AndroidManifest.xml's 
    <application> tag.
    """

    """
    public static final Creator<ApplicationInfo> CREATOR:
    
    """
    CREATOR = type(
        'ApplicationInfoCreator',
        (IParcelable.ICreator,), {
            'createFromParcel': lambda self, inparcel: ApplicationInfo()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * ApplicationInfo)()
        })()

    @overload
    def __init__(self):
        super(ApplicationInfo, self).__init__()

        """
        public String appComponentFactory:
        The factory of this package, as specified by the <manifest>
        tag's R.styleable.AndroidManifestApplication_appComponentFactory
        attribute.
        """
        self.appComponentFactory = ''

        """
        public String backupAgentName:
        Class implementing the Application's backup functionality.  From
        the "backupAgent" attribute.  This is an optional attribute and
        will be null if the application does not specify it in its manifest.

        If android:allowBackup is set to false, this attribute is ignored.
        """
        self.backupAgentName = ''

        """
        public int category:
        The category of this app. Categories are used to cluster multiple apps
        together into meaningful groups, such as when summarizing battery,
        network, or disk usage. Apps should only define this value when they fit
        well into one of the specific categories.

        Set from the R.attr.appCategory attribute in the
        manifest. If the manifest doesn't define a category, this value may have
        been provided by the installer via
        PackageManager.setApplicationCategoryHint(String, int).
        Value is CATEGORY_UNDEFINED, CATEGORY_GAME, CATEGORY_AUDIO, 
        CATEGORY_VIDEO, CATEGORY_IMAGE, CATEGORY_SOCIAL, CATEGORY_NEWS, 
        CATEGORY_MAPS or CATEGORY_PRODUCTIVITY.
        """
        self.category = CATEGORY_UNDEFINED

        """
        public String className:
        Class implementing the Application object.  From the "class"
        attribute.
        """
        self.className = ''

        """
        public int compatibleWidthLimitDp:
        The maximum smallest screen width the application is designed for.  If 0,
        nothing has been specified.  Comes from
        android:compatibleWidthLimitDp attribute of the <supports-screens> tag.
        """
        self.compatibleWidthLimitDp = 0

        """
        public String dataDir:
        Full path to the default directory assigned to the package for its
        persistent data.
        """
        self.dataDir = ''

        """
        public int descriptionRes:
        A style resource identifier (in the package's resources) of the
        description of an application.  From the "description" attribute
        or, if not set, 0.
        """
        self.descriptionRes = 0

        """
        public String deviceProtectedDataDir:
        Full path to the device-protected directory assigned to the package for
        its persistent data.See also:Context.createDeviceProtectedStorageContext()
        """
        self.deviceProtectedDataDir = ''

        """
        public boolean enabled:
        When false, indicates that all components within this application are
        considered disabled, regardless of their individually set enabled status.
        """
        self.enabled = True

        """
        public int flags:
        Flags associated with the application.  Any combination of
        FLAG_SYSTEM, FLAG_DEBUGGABLE, FLAG_HAS_CODE,
        FLAG_PERSISTENT, FLAG_FACTORY_TEST, and
        FLAG_ALLOW_TASK_REPARENTINGFLAG_ALLOW_CLEAR_USER_DATA, 
        FLAG_UPDATED_SYSTEM_APP,
        FLAG_TEST_ONLY, FLAG_SUPPORTS_SMALL_SCREENS,
        FLAG_SUPPORTS_NORMAL_SCREENS,
        FLAG_SUPPORTS_LARGE_SCREENS, FLAG_SUPPORTS_XLARGE_SCREENS,
        FLAG_RESIZEABLE_FOR_SCREENS,
        FLAG_SUPPORTS_SCREEN_DENSITIES, FLAG_VM_SAFE_MODE,
        FLAG_ALLOW_BACKUP, FLAG_KILL_AFTER_RESTORE,
        FLAG_RESTORE_ANY_VERSION, FLAG_EXTERNAL_STORAGE,
        FLAG_LARGE_HEAP, FLAG_STOPPED,
        FLAG_SUPPORTS_RTL, FLAG_INSTALLED,
        FLAG_IS_DATA_ONLY, FLAG_IS_GAME,
        FLAG_FULL_BACKUP_ONLY, FLAG_USES_CLEARTEXT_TRAFFIC,
        FLAG_MULTIARCH.
        """
        self.flags = 0

        """
        public int largestWidthLimitDp:
        The maximum smallest screen width the application will work on.  If 0,
        nothing has been specified.  Comes from
        android:largestWidthLimitDp attribute of the <supports-screens> tag.
        """
        self.largestWidthLimitDp = 0

        """
        public String manageSpaceActivityName:
        Class implementing the Application's manage space
        functionality.  From the "manageSpaceActivity"
        attribute. This is an optional attribute and will be null if
        applications don't specify it in their manifest
        """
        self.manageSpaceActivityName = ''

        """
        public int minSdkVersion:
        The minimum SDK version this application can run on. It will not run
        on earlier versions.
        """
        self.minSdkVersion = 0

        """
        public String nativeLibraryDir:
        Full path to the directory where native JNI libraries are stored.
        """
        self.nativeLibraryDir = ''

        """
        public String permission:
        Optional name of a permission required to be able to access this
        application's components.  From the "permission" attribute.
        """
        self.permission = ''

        """
        public String processName:
        The name of the process this application should run in.  From the
        "process" attribute or, if not set, the same as
        packageName.
        """
        self.processName = ''

        """
        public String publicSourceDir:
        Full path to the publicly available parts of sourceDir,
        including resources and manifest. This may be different from
        sourceDir if an application is forward locked.
        """
        self.publicSourceDir = ''

        """
        public int requiresSmallestWidthDp:
        The required smallest screen width the application can run on.  If 0,
        nothing has been specified.  Comes from
        android:requiresSmallestWidthDp attribute of the <supports-screens> tag.
        """
        self.requiresSmallestWidthDp = 0

        """
        public String[] sharedLibraryFiles:
        Paths to all shared libraries this application is linked against.  This
        field is only set if the PackageManager.GET_SHARED_LIBRARY_FILES flag was 
        used when retrieving
        the structure.
        """
        self.sharedLibraryFiles = []

        """
        public String sourceDir:
        Full path to the base APK for this application.
        """
        self.sourceDir = ''

        """
        public String[] splitNames:
        The names of all installed split APKs, ordered lexicographically.
        """
        self.splitNames = []

        """
        public String[] splitPublicSourceDirs:
        Full path to the publicly available parts of splitSourceDirs,
        including resources and manifest. This may be different from
        splitSourceDirs if an application is forward locked.See 
        also:splitSourceDirs
        """
        self.splitPublicSourceDirs = []

        """
        public String[] splitSourceDirs:
        Full paths to zero or more split APKs, indexed by the same order as 
        splitNames.
        """
        self.splitSourceDirs = []

        """
        public UUID storageUuid:
        UUID of the storage volume on which this application is being hosted. For
        apps hosted on the default internal storage at
        Environment.getDataDirectory(), the UUID value is
        StorageManager.UUID_DEFAULT.
        """
        self.storageUuid = 0

        """
        public int targetSdkVersion:
        The minimum SDK version this application targets.  It may run on earlier
        versions, but it knows how to work with any new behavior added at this
        version.  Will be Build.VERSION_CODES.CUR_DEVELOPMENT
        if this is a development build and the app is targeting that.  You should
        compare that this number is >= the SDK version number at which your
        behavior was introduced.
        """
        self.targetSdkVersion = 0

        """
        public String taskAffinity:
        Default task affinity of all activities in this application. See
        ActivityInfo.taskAffinity for more information.  This comes
        from the "taskAffinity" attribute.
        """
        self.taskAffinity = ''

        """
        public int theme:
        A style resource identifier (in the package's resources) of the
        default visual theme of the application.  From the "theme" attribute
        or, if not set, 0.
        """
        self.theme = 0

        """
        public int uiOptions:
        The default extra UI options for activities in this application.
        Set from the R.attr.uiOptions attribute in the
        activity's manifest.
        """
        self.uiOptions = 0

        """
        public int uid:
        The kernel user-ID that has been assigned to this application;
        currently this is not a unique ID (multiple applications can have
        the same uid).
        """
        self.uid = 0

        self._name = ''

        pass

    @__init__.adddef('ApplicationInfo')
    def __init__(self, orig):
        """
        :param orig: ApplicationInfo.
        """
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.__init__()
        self._readFromParcel(parcel)

    @property
    def packageName(self):
        return self._name

    @packageName.setter
    def packageName(self, value):
        self._name = value
        if not value: return
        baseDir = os.path.dirname(Android.__file__)
        baseDir = os.path.dirname(baseDir)
        if value == 'android':
            self.dataDir = baseDir
            return
        # self.deviceProtectedDataDir = self.deviceProtectedDataDir or os.path.join(baseDir, 'data', 'data', value)
        # self.credentialProtectedDataDir = self.deviceProtectedDataDir
        value = value.rsplit('.', 1)[-1]
        self.dataDir = os.path.join(baseDir, 'data', 'data', value)

    def describeContents(self):
        """
        Describe the kinds of special objects contained in this Parcelable 
        instance's marshaled representation. For example, if the object will 
        include a file descriptor in the output of readToParcel(Parcel, int), 
        the return value of this method must include the 
        CONTENTS_FILE_DESCRIPTOR bit.
        :return: int. a bitmask indicating the set of special object types 
        marshaled by this Parcelable object instance.
        """
        return 0

    def dump(self, pw, prefix):
        """
        :param pw: Printer
        :param prefix: String
        """
        pass

    @classmethod
    def getCategoryTitle(cls, context, category):
        """
        Return a concise, localized title for the given category value, or 
        null for unknown values such as CATEGORY_UNDEFINED.
        :param context: Context
        :param category: intValue is CATEGORY_UNDEFINED, CATEGORY_GAME, 
        CATEGORY_AUDIO, CATEGORY_VIDEO, CATEGORY_IMAGE, CATEGORY_SOCIAL, 
        CATEGORY_NEWS, CATEGORY_MAPS or CATEGORY_PRODUCTIVITY.
        :return: CharSequence.
        See also: category
        """
        category_name = (
            'CATEGORY_AUDIO', 'CATEGORY_GAME',
            'CATEGORY_IMAGE', 'CATEGORY_MAPS', 'CATEGORY_NEWS',
            'CATEGORY_PRODUCTIVITY', 'CATEGORY_SOCIAL', 'CATEGORY_VIDEO',
        )
        category_value = (
            CATEGORY_AUDIO, CATEGORY_GAME,
            CATEGORY_IMAGE, CATEGORY_MAPS, CATEGORY_NEWS,
            CATEGORY_PRODUCTIVITY, CATEGORY_SOCIAL, CATEGORY_VIDEO,
        )
        default = 'CATEGORY_UNDEFINED'
        try:
            pos = category_value.index(category)
            cat_name = category_name[pos]
        except:
            cat_name = default
        cat_name = '@android:string/app_' + cat_name.lower()
        resid = context.getIdentifier(cat_name)
        return context.getString(resid)

    def isVirtualPreload(self):
        """
        Returns whether or not this application was installed as a virtual 
        preload.
        :return: boolean.
        """
        pass

    def loadDescription(self, pm):
        """
        Retrieve the textual description of the application.  This will call 
        back on the given PackageManager to load the description from the 
        application.
        :param pm: PackageManager: A PackageManager from which the label can 
        be loaded; usually the PackageManager from which you originally 
        retrieved this item.
        :return: CharSequence. Returns a CharSequence containing the 
        application's description. If there is no description, null is 
        returned.
        """
        return pm.getText(self.packageName, self.descriptionRes, self)

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
        :param dest: Parcel
        :param parcelableFlags: int
        """
        super(ApplicationInfo, self).writeToParcel(dest, parcelableFlags)
        dest.writeString(self.appComponentFactory)
        dest.writeString(self.backupAgentName)
        dest.writeInt(self.category)
        dest.writeString(self.className)
        dest.writeInt(self.compatibleWidthLimitDp)
        dest.writeString(self.dataDir)
        dest.writeInt(self.descriptionRes)
        dest.writeString(self.deviceProtectedDataDir)
        dest.writeByte(self.enabled)
        dest.writeInt(self.flags)
        dest.writeInt(self.largestWidthLimitDp)
        dest.writeString(self.manageSpaceActivityName)
        dest.writeInt(self.minSdkVersion)
        dest.writeString(self.nativeLibraryDir)
        dest.writeString(self.permission)
        dest.writeString(self.processName)
        dest.writeString(self.publicSourceDir)
        dest.writeInt(self.requiresSmallestWidthDp)
        dest.writeStringArray(self.sharedLibraryFiles)
        dest.writeString(self.sourceDir)
        dest.writeStringArray(self.splitNames)
        dest.writeStringArray(self.splitPublicSourceDirs)
        dest.writeStringArray(self.splitSourceDirs)
        dest.writeInt(self.storageUuid)
        dest.writeInt(self.targetSdkVersion)
        dest.writeString(self.taskAffinity)
        dest.writeInt(self.theme)
        dest.writeInt(self.uiOptions)
        dest.writeInt(self.uid)
        pass
    
    def _readFromParcel(self, source):
        """
        :param source: Parcel.
        """
        super(ApplicationInfo, self)._readFromParcel(source)
        self.appComponentFactory = source.readString()
        self.backupAgentName = source.readString()
        self.category = source.readInt()
        self.className = source.readString()
        self.compatibleWidthLimitDp = source.readInt()
        self.dataDir = source.readString()
        self.descriptionRes = source.readInt()
        self.deviceProtectedDataDir = source.readString()
        self.enabled = bool(source.readByte())
        self.flags = source.readInt()
        self.largestWidthLimitDp = source.readInt()
        self.manageSpaceActivityName = source.readString()
        self.minSdkVersion = source.readInt()
        self.nativeLibraryDir = source.readString()
        self.permission = source.readString()
        self.processName = source.readString()
        self.publicSourceDir = source.readString()
        self.requiresSmallestWidthDp = source.readInt()
        self.sharedLibraryFiles = source.createStringArray()
        self.sourceDir = source.readString()
        self.splitNames = source.createStringArray()
        self.splitPublicSourceDirs = source.createStringArray()
        self.splitSourceDirs = source.createStringArray()
        self.storageUuid = source.readInt()
        self.targetSdkVersion = source.readInt()
        self.taskAffinity = source.readString()
        self.theme = source.readInt()
        self.uiOptions = source.readInt()
        self.uid = source.readInt()
        return self

