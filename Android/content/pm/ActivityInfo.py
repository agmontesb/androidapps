# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/ActivityInfo"""
from Android import overload, Object
from Android.content.pm.ComponentInfo import ComponentInfo
from Android.interface.IParcelable import IParcelable, ICreator
from Android.Os.Parcel import Parcel

"""
public static final int COLOR_MODE_DEFAULT:
Value for colorMode indicating that the activity should use the
default color mode (sRGB, low dynamic range).See also:R.attr.colorMode
"""
COLOR_MODE_DEFAULT = 0x00000000

"""
public static final int COLOR_MODE_HDR:
Value of colorMode indicating that the activity should use a
high dynamic range if the presentation display supports it.See 
also:R.attr.colorMode
"""
COLOR_MODE_HDR = 0x00000002

"""
public static final int COLOR_MODE_WIDE_COLOR_GAMUT:
Value of colorMode indicating that the activity should use a
wide color gamut if the presentation display supports it.See 
also:R.attr.colorMode
"""
COLOR_MODE_WIDE_COLOR_GAMUT = 0x00000001

"""
public static final int CONFIG_COLOR_MODE:
Bit in configChanges that indicates that the activity
can itself handle the change to the display color gamut or dynamic
range. Set from the R.attr.configChanges attribute.
"""
CONFIG_COLOR_MODE = 0x00004000

"""
public static final int CONFIG_DENSITY:
Bit in configChanges that indicates that the activity
can itself handle density changes. Set from the
R.attr.configChanges attribute.
"""
CONFIG_DENSITY = 0x00001000

"""
public static final int CONFIG_FONT_SCALE:
Bit in configChanges that indicates that the activity
can itself handle changes to the font scaling factor.  Set from the
R.attr.configChanges attribute.  This is
not a core resource configuration, but a higher-level value, so its
constant starts at the high bits.
"""
CONFIG_FONT_SCALE = 0x40000000

"""
public static final int CONFIG_KEYBOARD:
Bit in configChanges that indicates that the activity
can itself handle changes to the keyboard type.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_KEYBOARD = 0x00000010

"""
public static final int CONFIG_KEYBOARD_HIDDEN:
Bit in configChanges that indicates that the activity
can itself handle changes to the keyboard or navigation being hidden/exposed.
Note that inspite of the name, this applies to the changes to any
hidden states: keyboard or navigation.
Set from the R.attr.configChanges attribute.
"""
CONFIG_KEYBOARD_HIDDEN = 0x00000020

"""
public static final int CONFIG_LAYOUT_DIRECTION:
Bit in configChanges that indicates that the activity
can itself handle the change to layout direction. Set from the
R.attr.configChanges attribute.
"""
CONFIG_LAYOUT_DIRECTION = 0x00002000

"""
public static final int CONFIG_LOCALE:
Bit in configChanges that indicates that the activity
can itself handle changes to the locale.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_LOCALE = 0x00000004

"""
public static final int CONFIG_MCC:
Bit in configChanges that indicates that the activity
can itself handle changes to the IMSI MCC.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_MCC = 0x00000001

"""
public static final int CONFIG_MNC:
Bit in configChanges that indicates that the activity
can itself handle changes to the IMSI MNC.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_MNC = 0x00000002

"""
public static final int CONFIG_NAVIGATION:
Bit in configChanges that indicates that the activity
can itself handle changes to the navigation type.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_NAVIGATION = 0x00000040

"""
public static final int CONFIG_ORIENTATION:
Bit in configChanges that indicates that the activity
can itself handle changes to the screen orientation.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_ORIENTATION = 0x00000080

"""
public static final int CONFIG_SCREEN_LAYOUT:
Bit in configChanges that indicates that the activity
can itself handle changes to the screen layout.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_SCREEN_LAYOUT = 0x00000100

"""
public static final int CONFIG_SCREEN_SIZE:
Bit in configChanges that indicates that the activity
can itself handle the screen size. Set from the
R.attr.configChanges attribute.  This will be
set by default for applications that target an earlier version
than Build.VERSION_CODES.HONEYCOMB_MR2...
however, you will not see the bit set here becomes some
applications incorrectly compare configChanges against
an absolute value rather than correctly masking out the bits
they are interested in.  Please don't do that, thanks.
"""
CONFIG_SCREEN_SIZE = 0x00000400

"""
public static final int CONFIG_SMALLEST_SCREEN_SIZE:
Bit in configChanges that indicates that the activity
can itself handle the smallest screen size. Set from the
R.attr.configChanges attribute.  This will be
set by default for applications that target an earlier version
than Build.VERSION_CODES.HONEYCOMB_MR2...
however, you will not see the bit set here becomes some
applications incorrectly compare configChanges against
an absolute value rather than correctly masking out the bits
they are interested in.  Please don't do that, thanks.
"""
CONFIG_SMALLEST_SCREEN_SIZE = 0x00000800

"""
public static final int CONFIG_TOUCHSCREEN:
Bit in configChanges that indicates that the activity
can itself handle changes to the touchscreen type.  Set from the
R.attr.configChanges attribute.
"""
CONFIG_TOUCHSCREEN = 0x00000008

"""
public static final int CONFIG_UI_MODE:
Bit in configChanges that indicates that the activity
can itself handle the ui mode. Set from the
R.attr.configChanges attribute.
"""
CONFIG_UI_MODE = 0x00000200

"""
public static final int DOCUMENT_LAUNCH_ALWAYS:
Constant corresponding to always in
the R.attr.documentLaunchMode attribute.
"""
DOCUMENT_LAUNCH_ALWAYS = 0x00000002

"""
public static final int DOCUMENT_LAUNCH_INTO_EXISTING:
Constant corresponding to intoExisting in
the R.attr.documentLaunchMode attribute.
"""
DOCUMENT_LAUNCH_INTO_EXISTING = 0x00000001

"""
public static final int DOCUMENT_LAUNCH_NEVER:
Constant corresponding to never in
the R.attr.documentLaunchMode attribute.
"""
DOCUMENT_LAUNCH_NEVER = 0x00000003

"""
public static final int DOCUMENT_LAUNCH_NONE:
Constant corresponding to none in
the R.attr.documentLaunchMode attribute.
"""
DOCUMENT_LAUNCH_NONE = 0x00000000

"""
public static final int FLAG_ALLOW_TASK_REPARENTING:
Bit in flags that indicates that the activity can be moved
between tasks based on its task affinity.  Set from the
R.attr.allowTaskReparenting attribute.
"""
FLAG_ALLOW_TASK_REPARENTING = 0x00000040

"""
public static final int FLAG_ALWAYS_RETAIN_TASK_STATE:
Bit in flags indicating that, when the activity is the root
of a task, that task's stack should never be cleared when it is
relaunched from home.  Set from the
R.attr.alwaysRetainTaskState attribute.
"""
FLAG_ALWAYS_RETAIN_TASK_STATE = 0x00000008

"""
public static final int FLAG_AUTO_REMOVE_FROM_RECENTS:
Bit in flags indicating that tasks started with this activity are to be
removed from the recent list of tasks when the last activity in the task is 
finished.
Corresponds to R.attr.autoRemoveFromRecents
"""
FLAG_AUTO_REMOVE_FROM_RECENTS = 0x00002000

"""
public static final int FLAG_CLEAR_TASK_ON_LAUNCH:
Bit in flags indicating that, when the activity is the root
of a task, that task's stack should be cleared each time the user
re-launches it from home.  As a result, the user will always
return to the original activity at the top of the task.
This flag only applies to activities that
are used to start the root of a new task.  Set from the
R.attr.clearTaskOnLaunch attribute.
"""
FLAG_CLEAR_TASK_ON_LAUNCH = 0x00000004

"""
public static final int FLAG_ENABLE_VR_MODE:
Bit in flags indicating that this activity should be run with VR mode enabled.

.
See also:ERROR(/android.app.Activity#setVrMode(boolean))
"""
FLAG_ENABLE_VR_MODE = 0x00008000

"""
public static final int FLAG_EXCLUDE_FROM_RECENTS:
Bit in flags that indicates that the activity should not
appear in the list of recently launched activities.  Set from the
R.attr.excludeFromRecents attribute.
"""
FLAG_EXCLUDE_FROM_RECENTS = 0x00000020

"""
public static final int FLAG_FINISH_ON_CLOSE_SYSTEM_DIALOGS:
Bit in flags indicating that, when a request to close system
windows happens, this activity is finished.
Set from the
R.attr.finishOnCloseSystemDialogs attribute.
"""
FLAG_FINISH_ON_CLOSE_SYSTEM_DIALOGS = 0x00000100

"""
public static final int FLAG_FINISH_ON_TASK_LAUNCH:
Bit in flags indicating that, when the activity's task is
relaunched from home, this activity should be finished.
Set from the
R.attr.finishOnTaskLaunch attribute.
"""
FLAG_FINISH_ON_TASK_LAUNCH = 0x00000002

"""
public static final int FLAG_HARDWARE_ACCELERATED:
Value for flags: true when the application's rendering should
be hardware accelerated.
"""
FLAG_HARDWARE_ACCELERATED = 0x00000200

"""
public static final int FLAG_IMMERSIVE:
Bit in flags corresponding to an immersive activity
that wishes not to be interrupted by notifications.
Applications that hide the system notification bar with
WindowManager.LayoutParams.FLAG_FULLSCREEN
may still be interrupted by high-priority notifications; for example, an
incoming phone call may use
fullScreenIntent
to present a full-screen in-call activity to the user, pausing the
current activity as a side-effect. An activity with
FLAG_IMMERSIVE:
 set, however, will not be interrupted; the
notification may be shown in some other way (such as a small floating
"toast" window).

Note that this flag will always reflect the Activity's
android:immersive manifest definition, even if the Activity's
immersive state is changed at runtime via
Activity.setImmersive(boolean).See 
also:Notification.FLAG_HIGH_PRIORITYActivity.setImmersive(boolean)
"""
FLAG_IMMERSIVE = 0x00000800

"""
public static final int FLAG_MULTIPROCESS:
Bit in flags indicating whether this activity is able to
run in multiple processes.  If
true, the system may instantiate it in the some process as the
process starting it in order to conserve resources.  If false, the
default, it always runs in ComponentInfo.processName.  Set from the
R.attr.multiprocess attribute.
"""
FLAG_MULTIPROCESS = 0x00000001

"""
public static final int FLAG_NO_HISTORY:
Bit in flags indicating that, when the user navigates away
from an activity, it should be finished.
Set from the
R.attr.noHistory attribute.
"""
FLAG_NO_HISTORY = 0x00000080

"""
public static final int FLAG_RELINQUISH_TASK_IDENTITY:
Bit in flags: If set, a task rooted at this activity will have its
baseIntent replaced by the activity immediately above this. Each activity may 
further
relinquish its identity to the activity above it using this flag. Set from the
R.attr.relinquishTaskIdentity attribute.
"""
FLAG_RELINQUISH_TASK_IDENTITY = 0x00001000

"""
public static final int FLAG_RESUME_WHILE_PAUSING:
Bit in flags indicating that this activity can start is creation/resume
while the previous activity is still pausing.  Corresponds to
R.attr.resumeWhilePausing
"""
FLAG_RESUME_WHILE_PAUSING = 0x00004000

"""
public static final int FLAG_SINGLE_USER:
Bit in flags: If set, a single instance of the receiver will
run for all users on the device.  Set from the
R.attr.singleUser attribute.  Note that this flag is
only relevant for ActivityInfo structures that are describing receiver
components; it is not applied to activities.
"""
FLAG_SINGLE_USER = 0x40000000

"""
public static final int FLAG_STATE_NOT_NEEDED:
Bit in flags indicating that the activity's state
is not required to be saved, so that if there is a failure the
activity will not be removed from the activity stack.  Set from the
R.attr.stateNotNeeded attribute.
"""
FLAG_STATE_NOT_NEEDED = 0x00000010

"""
public static final int LAUNCH_MULTIPLE:
Constant corresponding to standard in
the R.attr.launchMode attribute.
"""
LAUNCH_MULTIPLE = 0x00000000

"""
public static final int LAUNCH_SINGLE_INSTANCE:
Constant corresponding to singleInstance in
the R.attr.launchMode attribute.
"""
LAUNCH_SINGLE_INSTANCE = 0x00000003

"""
public static final int LAUNCH_SINGLE_TASK:
Constant corresponding to singleTask in
the R.attr.launchMode attribute.
"""
LAUNCH_SINGLE_TASK = 0x00000002

"""
public static final int LAUNCH_SINGLE_TOP:
Constant corresponding to singleTop in
the R.attr.launchMode attribute.
"""
LAUNCH_SINGLE_TOP = 0x00000001

"""
public static final int PERSIST_ACROSS_REBOOTS:
Constant corresponding to persistAcrossReboots in
the R.attr.persistableMode attribute.
"""
PERSIST_ACROSS_REBOOTS = 0x00000002

"""
public static final int PERSIST_NEVER:
Constant corresponding to doNotPersist in
the R.attr.persistableMode attribute.
"""
PERSIST_NEVER = 0x00000001

"""
public static final int PERSIST_ROOT_ONLY:
Constant corresponding to persistRootOnly in
the R.attr.persistableMode attribute.
"""
PERSIST_ROOT_ONLY = 0x00000000

"""
public static final int SCREEN_ORIENTATION_BEHIND:
Constant corresponding to behind in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_BEHIND = 0x00000003

"""
public static final int SCREEN_ORIENTATION_FULL_SENSOR:
Constant corresponding to fullSensor in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_FULL_SENSOR = 0x0000000a

"""
public static final int SCREEN_ORIENTATION_FULL_USER:
Constant corresponding to fullUser in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_FULL_USER = 0x0000000d

"""
public static final int SCREEN_ORIENTATION_LANDSCAPE:
Constant corresponding to landscape in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_LANDSCAPE = 0x00000000

"""
public static final int SCREEN_ORIENTATION_LOCKED:
Constant corresponding to locked in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_LOCKED = 0x0000000e

"""
public static final int SCREEN_ORIENTATION_NOSENSOR:
Constant corresponding to nosensor in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_NOSENSOR = 0x00000005

"""
public static final int SCREEN_ORIENTATION_PORTRAIT:
Constant corresponding to portrait in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_PORTRAIT = 0x00000001

"""
public static final int SCREEN_ORIENTATION_REVERSE_LANDSCAPE:
Constant corresponding to reverseLandscape in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_REVERSE_LANDSCAPE = 0x00000008

"""
public static final int SCREEN_ORIENTATION_REVERSE_PORTRAIT:
Constant corresponding to reversePortrait in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_REVERSE_PORTRAIT = 0x00000009

"""
public static final int SCREEN_ORIENTATION_SENSOR:
Constant corresponding to sensor in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_SENSOR = 0x00000004

"""
public static final int SCREEN_ORIENTATION_SENSOR_LANDSCAPE:
Constant corresponding to sensorLandscape in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_SENSOR_LANDSCAPE = 0x00000006

"""
public static final int SCREEN_ORIENTATION_SENSOR_PORTRAIT:
Constant corresponding to sensorPortrait in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_SENSOR_PORTRAIT = 0x00000007

"""
public static final int SCREEN_ORIENTATION_UNSPECIFIED:
Constant corresponding to unspecified in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_UNSPECIFIED = -1

"""
public static final int SCREEN_ORIENTATION_USER:
Constant corresponding to user in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_USER = 0x00000002

"""
public static final int SCREEN_ORIENTATION_USER_LANDSCAPE:
Constant corresponding to userLandscape in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_USER_LANDSCAPE = 0x0000000b

"""
public static final int SCREEN_ORIENTATION_USER_PORTRAIT:
Constant corresponding to userPortrait in
the R.attr.screenOrientation attribute.
"""
SCREEN_ORIENTATION_USER_PORTRAIT = 0x0000000c

"""
public static final int UIOPTION_SPLIT_ACTION_BAR_WHEN_NARROW:
Flag for use with uiOptions.
Indicates that the action bar should put all action items in a separate bar 
when
the screen is narrow.
This value corresponds to "splitActionBarWhenNarrow" for the uiOptions XML
attribute.
"""
UIOPTION_SPLIT_ACTION_BAR_WHEN_NARROW = 0x00000001


class ActivityInfo(ComponentInfo, IParcelable):
    """
    Information you can retrieve about a particular application activity or 
    receiver. This corresponds to information collected from the 
    AndroidManifest.xml's <activity> and <receiver> tags.
    """

    """
    public static final Creator<ActivityInfo> CREATOR:
    
    """
    CREATOR = type(
        'ActivityInfoCreator',
        (ICreator,), {
            'createFromParcel': lambda self, inparcel: ActivityInfo()._readFromParcel(inparcel),
            'newArray': lambda self, size: (size * ActivityInfo)()
        })()

    @overload
    def __init__(self):
        """"""
        super(ActivityInfo, self).__init__()
        """
        public int colorMode:
        The color mode requested by this activity. The target display may not be
        able to honor the request.
        Value is COLOR_MODE_DEFAULT, COLOR_MODE_WIDE_COLOR_GAMUT or COLOR_MODE_HDR.
        """
        self.colorMode = COLOR_MODE_DEFAULT

        """
        public int configChanges:
        Bit mask of kinds of configuration changes that this activity
        can handle itself (without being restarted by the system).
        Contains any combination of CONFIG_FONT_SCALE,
        CONFIG_MCC, CONFIG_MNC,
        CONFIG_LOCALE, CONFIG_TOUCHSCREEN,
        CONFIG_KEYBOARD, CONFIG_NAVIGATION,
        CONFIG_ORIENTATION, CONFIG_SCREEN_LAYOUT,
        CONFIG_DENSITY, CONFIG_LAYOUT_DIRECTION and
        CONFIG_COLOR_MODE.
        Set from the R.attr.configChanges attribute.
        """
        self.configChanges = 0

        """
        public int documentLaunchMode:
        The document launch mode style requested by the activity. From the
        R.attr.documentLaunchMode attribute, one of
        DOCUMENT_LAUNCH_NONE, DOCUMENT_LAUNCH_INTO_EXISTING,
        DOCUMENT_LAUNCH_ALWAYS.

        Modes DOCUMENT_LAUNCH_ALWAYS
        and DOCUMENT_LAUNCH_INTO_EXISTING are equivalent to 
        Intent.FLAG_ACTIVITY_NEW_DOCUMENT with and without 
        Intent.FLAG_ACTIVITY_MULTIPLE_TASK respectively.
        """
        self.documentLaunchMode = 0

        """
        public int flags:
        Options that have been set in the activity declaration in the
        manifest.
        These include:
        FLAG_MULTIPROCESS,
        FLAG_FINISH_ON_TASK_LAUNCH, FLAG_CLEAR_TASK_ON_LAUNCH,
        FLAG_ALWAYS_RETAIN_TASK_STATE,
        FLAG_STATE_NOT_NEEDED, FLAG_EXCLUDE_FROM_RECENTS,
        FLAG_ALLOW_TASK_REPARENTING, FLAG_NO_HISTORY,
        FLAG_FINISH_ON_CLOSE_SYSTEM_DIALOGS,
        FLAG_HARDWARE_ACCELERATED, FLAG_SINGLE_USER.
        """
        self.flags = 0

        """
        public int launchMode:
        The launch mode style requested by the activity.  From the
        R.attr.launchMode attribute, one of
        LAUNCH_MULTIPLE,
        LAUNCH_SINGLE_TOP, LAUNCH_SINGLE_TASK, or
        LAUNCH_SINGLE_INSTANCE.
        """
        self.launchMode = 0

        """
        public int maxRecents:
        The maximum number of tasks rooted at this activity that can be in the 
        recent task list.
        Refer to R.attr.maxRecents.
        """
        self.maxRecents = 0

        """
        public String parentActivityName:
        If defined, the activity named here is the logical parent of this activity.
        """
        self.parentActivityName = ''

        """
        public String permission:
        Optional name of a permission required to be able to access this
        Activity.  From the "permission" attribute.
        """
        self.permission = ''

        """
        public int persistableMode:
        Value indicating how this activity is to be persisted across
        reboots for restoring in the Recents list.
        R.attr.persistableMode
        """
        self.persistableMode = 0

        """
        public int screenOrientation:
        The preferred screen orientation this activity would like to run in.
        From the R.attr.screenOrientation attribute, one of
        SCREEN_ORIENTATION_UNSPECIFIED,
        SCREEN_ORIENTATION_LANDSCAPE,
        SCREEN_ORIENTATION_PORTRAIT,
        SCREEN_ORIENTATION_USER,
        SCREEN_ORIENTATION_BEHIND,
        SCREEN_ORIENTATION_SENSOR,
        SCREEN_ORIENTATION_NOSENSOR,
        SCREEN_ORIENTATION_SENSOR_LANDSCAPE,
        SCREEN_ORIENTATION_SENSOR_PORTRAIT,
        SCREEN_ORIENTATION_REVERSE_LANDSCAPE,
        SCREEN_ORIENTATION_REVERSE_PORTRAIT,
        SCREEN_ORIENTATION_FULL_SENSOR,
        SCREEN_ORIENTATION_USER_LANDSCAPE,
        SCREEN_ORIENTATION_USER_PORTRAIT,
        SCREEN_ORIENTATION_FULL_USER,
        SCREEN_ORIENTATION_LOCKED,
        Value is SCREEN_ORIENTATION_UNSPECIFIED, SCREEN_ORIENTATION_LANDSCAPE, 
        SCREEN_ORIENTATION_PORTRAIT, SCREEN_ORIENTATION_USER, 
        SCREEN_ORIENTATION_BEHIND, SCREEN_ORIENTATION_SENSOR, 
        SCREEN_ORIENTATION_NOSENSOR, SCREEN_ORIENTATION_SENSOR_LANDSCAPE, 
        SCREEN_ORIENTATION_SENSOR_PORTRAIT, SCREEN_ORIENTATION_REVERSE_LANDSCAPE, 
        SCREEN_ORIENTATION_REVERSE_PORTRAIT, SCREEN_ORIENTATION_FULL_SENSOR, 
        SCREEN_ORIENTATION_USER_LANDSCAPE, SCREEN_ORIENTATION_USER_PORTRAIT, 
        SCREEN_ORIENTATION_FULL_USER or SCREEN_ORIENTATION_LOCKED.
        """
        self.screenOrientation = SCREEN_ORIENTATION_UNSPECIFIED

        """
        public int softInputMode:
        The desired soft input mode for this activity's main window.
        Set from the R.attr.windowSoftInputMode attribute
        in the activity's manifest.  May be any of the same values allowed
        for WindowManager.LayoutParams.softInputMode.  If 0 (unspecified),
        the mode from the theme will be used.
        Value is either 0 or combination of SOFT_INPUT_STATE_UNSPECIFIED, 
        SOFT_INPUT_STATE_UNCHANGED, SOFT_INPUT_STATE_HIDDEN, 
        SOFT_INPUT_STATE_ALWAYS_HIDDEN, SOFT_INPUT_STATE_VISIBLE, 
        SOFT_INPUT_STATE_ALWAYS_VISIBLE, SOFT_INPUT_ADJUST_RESIZE, 
        SOFT_INPUT_ADJUST_PAN, SOFT_INPUT_ADJUST_NOTHING or 
        SOFT_INPUT_IS_FORWARD_NAVIGATION.
        """
        self.softInputMode = 0

        """
        public String targetActivity:
        If this is an activity alias, this is the real activity class to run
        for it.  Otherwise, this is null.
        """
        self.targetActivity = ''

        """
        public String taskAffinity:
        The affinity this activity has for another task in the system.  The
        string here is the name of the task, often the package name of the
        overall package.  If null, the activity has no affinity.  Set from the
        R.attr.taskAffinity attribute.
        """
        self.taskAffinity = ''

        """
        public int theme:
        A style resource identifier (in the package's resources) of this
        activity's theme.  From the "theme" attribute or, if not set, 0.
        """
        self.theme = 0

        """
        public int uiOptions:
        The desired extra UI options for this activity and its main window.
        Set from the R.attr.uiOptions attribute in the
        activity's manifest.
        """
        self.uiOptions = 0

        """
        public ActivityInfo.WindowLayout windowLayout:
        Information about desired position and size of activity on the display when
        it is first started.
        """
        self.windowLayout = None
        pass

    @__init__.adddef('ActivityInfo')
    def ActivityInfo(self, orig):
        """
        :param orig: ActivityInfo.
        """
        parcel = Parcel()
        orig.writeToParcel(parcel, 0)
        parcel.setDataPosition(0)
        self.__init__()
        self._readFromParcel(parcel)
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

    def dump(self, pw, prefix):
        """
        :param pw: Printer
        :param prefix: String
        """
        pass

    def getThemeResource(self):
        """
        Return the theme resource identifier to use for this activity.  If the 
        activity defines a theme, that is used; else, the application theme is 
        used.
        :return: int. The theme associated with this activity.
        """
        return self.theme

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
        super(ActivityInfo, self).writeToParcel(dest, parcelableFlags)
        dest.writeInt(self.colorMode)
        dest.writeInt(self.configChanges)
        dest.writeInt(self.documentLaunchMode)
        dest.writeInt(self.flags)
        dest.writeInt(self.launchMode)
        dest.writeInt(self.maxRecents)
        dest.writeString(self.parentActivityName)
        dest.writeString(self.permission)
        dest.writeInt(self.persistableMode)
        dest.writeInt(self.screenOrientation)
        dest.writeInt(self.softInputMode)
        dest.writeString(self.targetActivity)
        dest.writeString(self.taskAffinity)
        dest.writeInt(self.theme)
        dest.writeInt(self.uiOptions)
        # dest.writeParcelable(self.windowLayout)

    def _readFromParcel(self, src):
        '''
        :param src: Parcel: The Parcel in which the object is written.
        :return ActivityInfo:
        '''
        super(ActivityInfo, self)._readFromParcel(src)
        self.colorMode = src.readInt()
        self.configChanges = src.readInt()
        self.documentLaunchMode = src.readInt()
        self.flags = src.readInt()
        self.launchMode = src.readInt()
        self.maxRecents = src.readInt()
        self.parentActivityName = src.readString()
        self.permission = src.readString()
        self.persistableMode = src.readInt()
        self.screenOrientation = src.readInt()
        self.softInputMode = src.readInt()
        self.targetActivity = src.readString()
        self.taskAffinity = src.readString()
        self.theme = src.readInt()
        self.uiOptions = src.readInt()
        return self


class WindowLayout(Object):
    """
    Contains information about position and size of the activity on the
    display. Used in freeform mode to set desired position when activity is
    first launched. It describes how big the activity wants to be in both
    width and height, the minimal allowed size, and the gravity to be applied.
    """

    def __init__(self, width=0, widthFraction=0.0, height=0, heightFraction=0.0, gravity=0, minWidth=0, minHeight=0):
        """
        :param width: int.
        :param widthFraction: float.
        :param height: int.
        :param heightFraction: float.
        :param gravity: int.
        :param minWidth: int.
        :param minHeight: int.
        """
        super(WindowLayout, self).__init__()
        """
        public final int gravity:
        Gravity of activity.
        Currently Gravity.TOP, Gravity.BOTTOM, Gravity.LEFT and Gravity.RIGHT 
        are supported.
        """
        self.gravity = gravity

        """
        public final int height:
        Height of activity in pixels.
        """
        self.height = height

        """
        public final float heightFraction:
        Height of activity as a fraction of available display height.
        If both height and this value are set this one will be preferred.
        """
        self.heightFraction = heightFraction

        """
        public final int minHeight:
        Minimal height of activity in pixels to be able to display its content.
    
        NOTE: A task's root activity value is applied to all additional
        activities launched in the task. That is if the root activity of a task 
        set minimal
        height, then the system will set the same minimal height on all other 
        activities in the
        task. It will also ignore any other minimal height attributes of non-root 
        activities.
        """
        self.minHeight = minHeight

        """
        public final int minWidth:
        Minimal width of activity in pixels to be able to display its content.
    
        NOTE: A task's root activity value is applied to all additional
        activities launched in the task. That is if the root activity of a task 
        set minimal
        width, then the system will set the same minimal width on all other 
        activities in the
        task. It will also ignore any other minimal width attributes of non-root 
        activities.
        """
        self.minWidth = minWidth

        """
        public final int width:
        Width of activity in pixels.
        """
        self.width = width

        """
        public final float widthFraction:
        Width of activity as a fraction of available display width.
        If both width and this value are set this one will be preferred.
        """
        self.widthFraction = widthFraction
        pass
