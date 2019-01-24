# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/Context"""
import abc

from Android import overload

class IContext(object):
    __metaclass__ = abc.ABCMeta

    """
    public static final String ACCESSIBILITY_SERVICE:
    Use with getSystemService(String) to retrieve a AccessibilityManager for 
    giving the user
    """
    ACCESSIBILITY_SERVICE = 'accessibility'
    """
    public static final String ACCOUNT_SERVICE:
    Use with getSystemService(String) to retrieve a
    AccountManager for receiving intents at a
    """
    ACCOUNT_SERVICE = 'account'
    """
    public static final String ACTIVITY_SERVICE:
    Use with getSystemService(String) to retrieve a
    ActivityManager for interacting with the global
    """
    ACTIVITY_SERVICE = 'activity'
    """
    public static final String ALARM_SERVICE:
    Use with getSystemService(String) to retrieve a
    AlarmManager for receiving intents at a
    """
    ALARM_SERVICE = 'alarm'
    """
    public static final String APPWIDGET_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    APPWIDGET_SERVICE = 'appwidget'
    """
    public static final String APP_OPS_SERVICE:
    Use with getSystemService(String) to retrieve a
    AppOpsManager for tracking application operations
    """
    APP_OPS_SERVICE = 'appops'
    """
    public static final String AUDIO_SERVICE:
    Use with getSystemService(String) to retrieve a
    AudioManager for handling management of volume,
    """
    AUDIO_SERVICE = 'audio'
    """
    public static final String BATTERY_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    BATTERY_SERVICE = 'batterymanager'
    """
    public static final int BIND_ABOVE_CLIENT:
    Flag for bindService(Intent, ServiceConnection, int): indicates that the 
    client application
    binding to this service considers the service to be more important than
    the app itself.  When set, the platform will try to have the out of
    memory killer kill the app before it kills the service it is bound to, 
    though
    this is not guaranteed to be the case.
    """
    BIND_ABOVE_CLIENT = 0x00000008
    """
    public static final int BIND_ADJUST_WITH_ACTIVITY:
    Flag for bindService(Intent, ServiceConnection, int): If binding from an 
    activity, allow the
    target service's process importance to be raised based on whether the
    activity is visible to the user, regardless whether another flag is
    used to reduce the amount that the client process's overall importance
    is used to impact it.
    """
    BIND_ADJUST_WITH_ACTIVITY = 0x00000080
    """
    public static final int BIND_ALLOW_OOM_MANAGEMENT:
    Flag for bindService(Intent, ServiceConnection, int): allow the process 
    hosting the bound
    service to go through its normal memory management.  It will be
    treated more like a running service, allowing the system to
    (temporarily) expunge the process if low on memory or for some other
    whim it may have, and being more aggressive about making it a candidate
    to be killed (and restarted) if running for a long time.
    """
    BIND_ALLOW_OOM_MANAGEMENT = 0x00000010
    """
    public static final int BIND_AUTO_CREATE:
    Flag for bindService(Intent, ServiceConnection, int): automatically create 
    the service as long
    as the binding exists.  Note that while this will create the service,
    its Service.onStartCommand(Intent, int, int)
    method will still only be called due to an
    explicit call to startService(Intent).  Even without that, though,
    this still provides you with access to the service object while the
    service is created.
    
    Note that prior to Build.VERSION_CODES.ICE_CREAM_SANDWICH,
    not supplying this flag would also impact how important the system
    consider's the target service's process to be.  When set, the only way
    for it to be raised was by binding from a service in which case it will
    only be important when that activity is in the foreground.  Now to
    achieve this behavior you must explicitly supply the new flag
    BIND_ADJUST_WITH_ACTIVITY.  For compatibility, old applications
    that don't specify BIND_AUTO_CREATE:
     will automatically have
    the flags BIND_WAIVE_PRIORITY and
    BIND_ADJUST_WITH_ACTIVITY set for them in order to achieve
    the same result.
    """
    BIND_AUTO_CREATE = 0x00000001
    """
    public static final int BIND_DEBUG_UNBIND:
    Flag for bindService(Intent, ServiceConnection, int): include debugging 
    help for mismatched
    calls to unbind.  When this flag is set, the callstack of the following
    unbindService(ServiceConnection) call is retained, to be printed if a later
    incorrect unbind call is made.  Note that doing this requires retaining
    information about the binding that was made for the lifetime of the app,
    resulting in a leak -- this should only be used for debugging.
    """
    BIND_DEBUG_UNBIND = 0x00000002
    """
    public static final int BIND_EXTERNAL_SERVICE:
    Flag for bindService(Intent, ServiceConnection, int): The service being 
    bound is an
    isolated,
    external service.  This binds the service into the
    calling application's package, rather than the package in which the 
    service is declared.
    
    When using this flag, the code for the service being bound will execute 
    under the calling
    application's package name and user ID.  Because the service must be an 
    isolated process,
    it will not have direct access to the application's data, though.
    
    The purpose of this flag is to allow applications to provide services that 
    are attributed
    to the app using the service, rather than the application providing the 
    service.
    """
    BIND_EXTERNAL_SERVICE = 0x80000000
    """
    public static final int BIND_IMPORTANT:
    Flag for bindService(Intent, ServiceConnection, int): this service is very 
    important to
    the client, so should be brought to the foreground process level
    when the client is.  Normally a process can only be raised to the
    visibility level by a client, even if that client is in the foreground.
    """
    BIND_IMPORTANT = 0x00000040
    """
    public static final int BIND_NOT_FOREGROUND:
    Flag for bindService(Intent, ServiceConnection, int): don't allow this 
    binding to raise
    the target service's process to the foreground scheduling priority.
    It will still be raised to at least the same memory priority
    as the client (so that its process will not be killable in any
    situation where the client is not killable), but for CPU scheduling
    purposes it may be left in the background.  This only has an impact
    in the situation where the binding client is a foreground process
    and the target service is in a background process.
    """
    BIND_NOT_FOREGROUND = 0x00000004
    """
    public static final int BIND_WAIVE_PRIORITY:
    Flag for bindService(Intent, ServiceConnection, int): don't impact the 
    scheduling or
    memory management priority of the target service's hosting process.
    Allows the service's process to be managed on the background LRU list
    just like a regular application process in the background.
    """
    BIND_WAIVE_PRIORITY = 0x00000020
    """
    public static final String BLUETOOTH_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    BLUETOOTH_SERVICE = 'bluetooth'
    """
    public static final String CAMERA_SERVICE:
    Use with getSystemService(String) to retrieve a
    CameraManager for interacting with
    """
    CAMERA_SERVICE = 'camera'
    """
    public static final String CAPTIONING_SERVICE:
    Use with getSystemService(String) to retrieve a
    CaptioningManager for obtaining
    captioning properties and listening for changes in captioning
    """
    CAPTIONING_SERVICE = 'captioning'
    """
    public static final String CARRIER_CONFIG_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    CARRIER_CONFIG_SERVICE = 'carrier_config'
    """
    public static final String CLIPBOARD_SERVICE:
    Use with getSystemService(String) to retrieve a
    ClipboardManager for accessing and modifying
    """
    CLIPBOARD_SERVICE = 'clipboard'
    """
    public static final String COMPANION_DEVICE_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    COMPANION_DEVICE_SERVICE = 'companiondevice'
    """
    public static final String CONNECTIVITY_SERVICE:
    Use with getSystemService(String) to retrieve a ConnectivityManager for 
    handling management of
    """
    CONNECTIVITY_SERVICE = 'connectivity'
    """
    public static final String CONSUMER_IR_SERVICE:
    Use with getSystemService(String) to retrieve a
    ConsumerIrManager for transmitting infrared
    """
    CONSUMER_IR_SERVICE = 'consumer_ir'
    """
    public static final int CONTEXT_IGNORE_SECURITY:
    Flag for use with createPackageContext(String, int): ignore any security
    restrictions on the Context being requested, allowing it to always
    be loaded.  For use with CONTEXT_INCLUDE_CODE to allow code
    to be loaded into a process even when it isn't safe to do so.  Use
    with extreme care!
    """
    CONTEXT_IGNORE_SECURITY = 0x00000002
    """
    public static final int CONTEXT_INCLUDE_CODE:
    Flag for use with createPackageContext(String, int): include the 
    application
    code with the context.  This means loading code into the caller's
    process, so that getClassLoader() can be used to instantiate
    the application's classes.  Setting this flags imposes security
    restrictions on what application context you can access; if the
    requested application can not be safely loaded into your process,
    java.lang.SecurityException will be thrown.  If this flag is not set,
    there will be no restrictions on the packages that can be loaded,
    but getClassLoader() will always return the default system
    class loader.
    """
    CONTEXT_INCLUDE_CODE = 0x00000001
    """
    public static final int CONTEXT_RESTRICTED:
    Flag for use with createPackageContext(String, int): a restricted context 
    may
    disable specific features. For instance, a View associated with a 
    restricted
    context would ignore particular XML attributes.
    """
    CONTEXT_RESTRICTED = 0x00000004
    """
    public static final String CROSS_PROFILE_APPS_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    CROSS_PROFILE_APPS_SERVICE = 'crossprofileapps'
    """
    public static final String DEVICE_POLICY_SERVICE:
    Use with getSystemService(String) to retrieve a
    DevicePolicyManager for working with global
    """
    DEVICE_POLICY_SERVICE = 'device_policy'
    """
    public static final String DISPLAY_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    DISPLAY_SERVICE = 'display'
    """
    public static final String DOWNLOAD_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    DOWNLOAD_SERVICE = 'download'
    """
    public static final String DROPBOX_SERVICE:
    Use with getSystemService(String) to retrieve a
    DropBoxManager instance for recording
    """
    DROPBOX_SERVICE = 'dropbox'
    """
    public static final String EUICC_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    EUICC_SERVICE = 'euicc'
    """
    public static final String FINGERPRINT_SERVICE:
    Use with getSystemService(String) to retrieve a
    FingerprintManager for handling management
    """
    FINGERPRINT_SERVICE = 'fingerprint'
    """
    public static final String HARDWARE_PROPERTIES_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    HARDWARE_PROPERTIES_SERVICE = 'hardware_properties'
    """
    public static final String INPUT_METHOD_SERVICE:
    Use with getSystemService(String) to retrieve a
    InputMethodManager for accessing input
    """
    INPUT_METHOD_SERVICE = 'input_method'
    """
    public static final String INPUT_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    INPUT_SERVICE = 'input'
    """
    public static final String IPSEC_SERVICE:
    Use with getSystemService(String) to retrieve a
    IpSecManager for encrypting Sockets or Networks with
    """
    IPSEC_SERVICE = 'ipsec'
    """
    public static final String JOB_SCHEDULER_SERVICE:
    Use with getSystemService(String) to retrieve a JobScheduler instance for 
    managing occasional
    """
    JOB_SCHEDULER_SERVICE = 'jobscheduler'
    """
    public static final String KEYGUARD_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    KEYGUARD_SERVICE = 'keyguard'
    """
    public static final String LAUNCHER_APPS_SERVICE:
    Use with getSystemService(String) to retrieve a
    LauncherApps for querying and monitoring launchable apps across
    """
    LAUNCHER_APPS_SERVICE = 'launcherapps'
    """
    public static final String LAYOUT_INFLATER_SERVICE:
    Use with getSystemService(String) to retrieve a
    LayoutInflater for inflating layout resources in this
    """
    LAYOUT_INFLATER_SERVICE = 'layout_inflater'
    """
    public static final String LOCATION_SERVICE:
    Use with getSystemService(String) to retrieve a LocationManager for 
    controlling location
    """
    LOCATION_SERVICE = 'location'
    """
    public static final String MEDIA_PROJECTION_SERVICE:
    Use with getSystemService(String) to retrieve a MediaProjectionManager 
    instance for managing
    """
    MEDIA_PROJECTION_SERVICE = 'media_projection'
    """
    public static final String MEDIA_ROUTER_SERVICE:
    Use with getSystemService(String) to retrieve a
    MediaRouter for controlling and managing
    """
    MEDIA_ROUTER_SERVICE = 'media_router'
    """
    public static final String MEDIA_SESSION_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    MEDIA_SESSION_SERVICE = 'media_session'
    """
    public static final String MIDI_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    MIDI_SERVICE = 'midi'
    """
    public static final int MODE_APPEND:
    File creation mode: for use with openFileOutput(String, int), if the file
    already exists then write data to the end of the existing file
    instead of erasing it.See also:openFileOutput(String, int)
    """
    MODE_APPEND = 0x00008000
    """
    public static final int MODE_ENABLE_WRITE_AHEAD_LOGGING:
    Database open flag: when set, the database is opened with write-ahead
    logging enabled by default.See also:openOrCreateDatabase(String, int, 
    CursorFactory)openOrCreateDatabase(String, int, CursorFactory, 
    DatabaseErrorHandler)SQLiteDatabase.enableWriteAheadLogging()
    """
    MODE_ENABLE_WRITE_AHEAD_LOGGING = 0x00000008
    """
    public static final int MODE_MULTI_PROCESS:
    
    This constant was deprecated
    in API level 23.
    MODE_MULTI_PROCESS:
     does not work reliably in
    some versions of Android, and furthermore does not provide any
    mechanism for reconciling concurrent modifications across
    processes.  Applications should not attempt to use it.  Instead,
    they should use an explicit cross-process data management
    approach such as ContentProvider.
    
    SharedPreference loading flag: when set, the file on disk will
    be checked for modification even if the shared preferences
    instance is already loaded in this process.  This behavior is
    sometimes desired in cases where the application has multiple
    processes, all writing to the same SharedPreferences file.
    Generally there are better forms of communication between
    processes, though.
    
    This was the legacy (but undocumented) behavior in and
    before Gingerbread (Android 2.3) and this flag is implied when
    targeting such releases.  For applications targeting SDK
    versions greater than Android 2.3, this flag must be
    explicitly set if desired.See also:getSharedPreferences(String, int)
    """
    MODE_MULTI_PROCESS = 0x00000004
    """
    public static final int MODE_NO_LOCALIZED_COLLATORS:
    Database open flag: when set, the database is opened without support for
    localized collators.See also:openOrCreateDatabase(String, int, 
    CursorFactory)openOrCreateDatabase(String, int, CursorFactory, 
    DatabaseErrorHandler)SQLiteDatabase.NO_LOCALIZED_COLLATORS
    """
    MODE_NO_LOCALIZED_COLLATORS = 0x00000010
    """
    public static final int MODE_PRIVATE:
    File creation mode: the default mode, where the created file can only
    be accessed by the calling application (or all applications sharing the
    same user ID).
    """
    MODE_PRIVATE = 0x00000000
    """
    public static final int MODE_WORLD_READABLE:
    
    This constant was deprecated
    in API level 17.
    Creating world-readable files is very dangerous, and likely
    to cause security holes in applications. It is strongly
    discouraged; instead, applications should use more formal
    mechanism for interactions such as ContentProvider,
    BroadcastReceiver, and Service.
    There are no guarantees that this access mode will remain on
    a file, such as when it goes through a backup and restore.
    File creation mode: allow all other applications to have read access to
    the created file.
    
    Starting from Build.VERSION_CODES.N, attempting to use this
    mode throws a SecurityException.See 
    also:FileProviderIntent.FLAG_GRANT_WRITE_URI_PERMISSION
    """
    MODE_WORLD_READABLE = 0x00000001
    """
    public static final int MODE_WORLD_WRITEABLE:
    
    This constant was deprecated
    in API level 17.
    Creating world-writable files is very dangerous, and likely
    to cause security holes in applications. It is strongly
    discouraged; instead, applications should use more formal
    mechanism for interactions such as ContentProvider,
    BroadcastReceiver, and Service.
    There are no guarantees that this access mode will remain on
    a file, such as when it goes through a backup and restore.
    File creation mode: allow all other applications to have write access to
    the created file.
    
    Starting from Build.VERSION_CODES.N, attempting to use this
    mode will throw a SecurityException.See 
    also:FileProviderIntent.FLAG_GRANT_WRITE_URI_PERMISSION
    """
    MODE_WORLD_WRITEABLE = 0x00000002
    """
    
    """
    NETWORK_STATS_SERVICE = 'netstats'
    """
    public static final String NFC_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    NFC_SERVICE = 'nfc'
    """
    public static final String NOTIFICATION_SERVICE:
    Use with getSystemService(String) to retrieve a
    NotificationManager for informing the user of
    """
    NOTIFICATION_SERVICE = 'notification'
    """
    public static final String NSD_SERVICE:
    Use with getSystemService(String) to retrieve a NsdManager for handling 
    management of network service
    """
    NSD_SERVICE = 'servicediscovery'
    """
    public static final String POWER_SERVICE:
    Use with getSystemService(String) to retrieve a
    PowerManager for controlling power management,
    including "wake locks," which let you keep the device on while
    you're running long tasks.
    """
    POWER_SERVICE = 'power'
    """
    public static final String PRINT_SERVICE:
    PrintManager for printing and managing
    """
    PRINT_SERVICE = 'print'
    """
    public static final int RECEIVER_VISIBLE_TO_INSTANT_APPS:
    Flag for registerReceiver(BroadcastReceiver, IntentFilter): The receiver 
    can receive broadcasts from Instant Apps.
    """
    RECEIVER_VISIBLE_TO_INSTANT_APPS = 0x00000001
    """
    public static final String RESTRICTIONS_SERVICE:
    Use with getSystemService(String) to retrieve a
    RestrictionsManager for retrieving application restrictions
    """
    RESTRICTIONS_SERVICE = 'restrictions'
    """
    public static final String SEARCH_SERVICE:
    Use with getSystemService(String) to retrieve a SearchManager for handling 
    searches.
    
    Configuration.UI_MODE_TYPE_WATCH does not support
    """
    SEARCH_SERVICE = 'search'
    """
    
    """
    SENSOR_SERVICE = 'sensor'
    """
    public static final String SHORTCUT_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    SHORTCUT_SERVICE = 'shortcut'
    """
    public static final String STORAGE_SERVICE:
    Use with getSystemService(String) to retrieve a StorageManager for 
    accessing system storage
    """
    STORAGE_SERVICE = 'storage'
    """
    public static final String STORAGE_STATS_SERVICE:
    Use with getSystemService(String) to retrieve a StorageStatsManager for 
    accessing system storage
    """
    STORAGE_STATS_SERVICE = 'storagestats'
    """
    public static final String SYSTEM_HEALTH_SERVICE:
    Use with getSystemService(String) to retrieve a
    SystemHealthManager for accessing system health (battery, power,
    """
    SYSTEM_HEALTH_SERVICE = 'systemhealth'
    """
    public static final String TELECOM_SERVICE:
    Use with getSystemService(String) to retrieve a
    TelecomManager to manage telecom-related features
    """
    TELECOM_SERVICE = 'telecom'
    """
    public static final String TELEPHONY_SERVICE:
    Use with getSystemService(String) to retrieve a
    TelephonyManager for handling management the
    """
    TELEPHONY_SERVICE = 'phone'
    """
    public static final String TELEPHONY_SUBSCRIPTION_SERVICE:
    Use with getSystemService(String) to retrieve a
    SubscriptionManager for handling management the
    """
    TELEPHONY_SUBSCRIPTION_SERVICE = 'telephony_subscription_service'
    """
    public static final String TEXT_CLASSIFICATION_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    TEXT_CLASSIFICATION_SERVICE = 'textclassification'
    """
    public static final String TEXT_SERVICES_MANAGER_SERVICE:
    Use with getSystemService(String) to retrieve a
    TextServicesManager for accessing
    """
    TEXT_SERVICES_MANAGER_SERVICE = 'textservices'
    """
    public static final String TV_INPUT_SERVICE:
    Use with getSystemService(String) to retrieve a
    TvInputManager for interacting with TV inputs
    """
    TV_INPUT_SERVICE = 'tv_input'
    """
    public static final String UI_MODE_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    UI_MODE_SERVICE = 'uimode'
    """
    
    """
    USAGE_STATS_SERVICE = 'usagestats'
    """
    public static final String USB_SERVICE:
    Use with getSystemService(String) to retrieve a UsbManager for access to 
    USB devices (as a USB host)
    """
    USB_SERVICE = 'usb'
    """
    public static final String USER_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    USER_SERVICE = 'user'
    """
    
    """
    VIBRATOR_SERVICE = 'vibrator'
    """
    public static final String WALLPAPER_SERVICE:
    Use with getSystemService(String) to retrieve a
    """
    WALLPAPER_SERVICE = 'wallpaper'
    """
    public static final String WIFI_AWARE_SERVICE:
    Use with getSystemService(String) to retrieve a
    WifiAwareManager for handling management of
    """
    WIFI_AWARE_SERVICE = 'wifiaware'
    """
    public static final String WIFI_P2P_SERVICE:
    Use with getSystemService(String) to retrieve a WifiP2pManager for 
    handling management of
    """
    WIFI_P2P_SERVICE = 'wifip2p'
    """
    public static final String WIFI_RTT_RANGING_SERVICE:
    Use with getSystemService(String) to retrieve a WifiRttManager for ranging 
    devices with wifi
    
    Note: this is a replacement for WIFI_RTT_SERVICE above. It will
    """
    WIFI_RTT_RANGING_SERVICE = 'wifirtt'
    """
    public static final String WIFI_SERVICE:
    Use with getSystemService(String) to retrieve a WifiManager for handling 
    management of
    """
    WIFI_SERVICE = 'wifi'
    """
    public static final String WINDOW_SERVICE:
    Use with getSystemService(String) to retrieve a
    WindowManager for accessing the system's window
    """
    WINDOW_SERVICE = 'window'

    def __init__(self):
        pass

    def bindService(self, service, conn, flags):
        """
        Connect to an application service, creating it if needed.  This
        defines a dependency between your application and the service.  The
        given conn will receive the service object when it is created and be
        told if it dies and restarts.  The service will be considered required
        by the system only for as long as the calling context exists.  For
        example, if this Context is an Activity that is stopped, the service
        will not be required to continue running until the Activity is
        resumed.  If the service does not support binding, it may return null
        from its onBind() method.  If it does, then the ServiceConnection's
        onNullBinding() method will be invoked instead of
        onServiceConnected().  This method will throw SecurityException if the
        calling app does not have permission to bind to the given service.
        Note: this method cannot be called from a BroadcastReceiver component.
         A pattern you can use to communicate from a BroadcastReceiver to a
        Service is to call startService(Intent) with the arguments containing
        the command to be sent, with the service calling its
        Service.stopSelf(int) method when done executing that command.  See
        the API demo App/Service/Service Start Arguments Controller for an
        illustration of this.  It is okay, however, to use this method from a
        BroadcastReceiver that has been registered with
        registerReceiver(BroadcastReceiver, IntentFilter), since the lifetime
        of this BroadcastReceiver is tied to another object (the one that
        registered it).
        :param service: Intent: Identifies the service to
        :param conn: ect to.  The Intent must specify an explicit component
        name.connServiceConnection: Receives information as the service is
        started and stopped. This must be a valid ServiceConnection object; it
        must not be null.
        :param flags: int: Operation options for the binding.  May be 0,
        BIND_AUTO_CREATE, BIND_DEBUG_UNBIND, BIND_NOT_FOREGROUND,
        BIND_ABOVE_CLIENT, BIND_ALLOW_OOM_MANAGEMENT, or
        BIND_WAIVE_PRIORITY.Value is either 0 or combination of
        BIND_AUTO_CREATE, BIND_DEBUG_UNBIND, BIND_NOT_FOREGROUND,
        BIND_ABOVE_CLIENT, BIND_ALLOW_OOM_MANAGEMENT, BIND_WAIVE_PRIORITY,
        BIND_IMPORTANT or BIND_ADJUST_WITH_ACTIVITY.
        :return: boolean. true if the system is in the process of bringing up
        a service that your client has permission to bind to; false if the
        system couldn't find the service or if your client doesn't have
        permission to bind to it. If this value is true, you should later call
        unbindService(ServiceConnection) to release the connection.
        :raises: SecurityExceptionIf the caller does not have permission to
        access the service or the service can not be found.
        See also:

        unbindService(ServiceConnection)startService(Intent)BIND_AUTO_CREATEBIND_DEBUG_UNBINDBIND_NOT_FOREGROUND
        """
        pass

    def checkCallingOrSelfPermission(self, permission):
        """
        Determine whether the calling process of an IPC or you have been
        granted a particular permission.  This is the same as
        checkCallingPermission(String), except it grants your own permissions
        if you are not currently processing an IPC.  Use with care!
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :return: int. PackageManager.PERMISSION_GRANTED if the calling pid/uid
        is allowed that permission, or PackageManager.PERMISSION_DENIED if it
        is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: PackageManager.checkPermission(String,
        String)checkPermission(String, int, int)checkCallingPermission(String)
        """
        pass

    def checkCallingOrSelfUriPermission(self, uri, modeFlags):
        """
        Determine whether the calling process of an IPC or you has been
        granted permission to access a specific URI.  This is the same as
        checkCallingUriPermission(Uri, int), except it grants your own
        permissions if you are not currently processing an IPC.  Use with care!
        :param uri: Uri: The uri that is being checked.
        :param modeFlags: int: The access modes to check.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :return: int. PackageManager.PERMISSION_GRANTED if the caller is
        allowed to access that uri, or PackageManager.PERMISSION_DENIED if it
        is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: checkCallingUriPermission(Uri, int)
        """
        pass

    def checkCallingPermission(self, permission):
        """
        Determine whether the calling process of an IPC you are handling has
        been granted a particular permission.  This is basically the same as
        calling checkPermission(String, int, int) with the pid and uid
        returned by Binder.getCallingPid() and Binder.getCallingUid().  One
        important difference is that if you are not currently processing an
        IPC, this function will always fail.  This is done to protect against
        accidentally leaking permissions; you can use
        checkCallingOrSelfPermission(String) to avoid this protection.
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :return: int. PackageManager.PERMISSION_GRANTED if the calling pid/uid
        is allowed that permission, or PackageManager.PERMISSION_DENIED if it
        is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: PackageManager.checkPermission(String,
        String)checkPermission(String, int,
        int)checkCallingOrSelfPermission(String)
        """
        pass

    def checkCallingUriPermission(self, uri, modeFlags):
        """
        Determine whether the calling process and user ID has been granted
        permission to access a specific URI.  This is basically the same as
        calling checkUriPermission(Uri, int, int, int) with the pid and uid
        returned by Binder.getCallingPid() and Binder.getCallingUid().  One
        important difference is that if you are not currently processing an
        IPC, this function will always fail.
        :param uri: Uri: The uri that is being checked.
        :param modeFlags: int: The access modes to check.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :return: int. PackageManager.PERMISSION_GRANTED if the caller is
        allowed to access that uri, or PackageManager.PERMISSION_DENIED if it
        is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: checkUriPermission(Uri, int, int, int)
        """
        pass

    def checkPermission(self, permission, pid, uid):
        """
        Determine whether the given permission is allowed for a particular
        process and user ID running in the system.
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :return: int. PackageManager.PERMISSION_GRANTED if the given pid/uid
        is allowed that permission, or PackageManager.PERMISSION_DENIED if it
        is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: PackageManager.checkPermission(String,
        String)checkCallingPermission(String)
        """
        pass

    def checkSelfPermission(self, permission):
        """
        Determine whether you have been granted a particular permission.
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :return: int. PackageManager.PERMISSION_GRANTED if you have the
        permission, or PackageManager.PERMISSION_DENIED if not.Value is
        PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: PackageManager.checkPermission(String,
        String)checkCallingPermission(String)
        """
        pass

    @overload('Uri', 'str', 'str', 'int', 'int', 'int')
    def checkUriPermission(self, uri, readPermission, writePermission, pid, uid, modeFlags):
        """
        Check both a Uri and normal permission.  This allows you to perform
        both checkPermission(String, int, int) and checkUriPermission(Uri,
        int, int, int) in one call.
        :param uri: Uri: The Uri whose permission is to be checked, or null to
        not do this check.
        :param readPermission: String: The permission that provides overall
        read access, or null to not do this check.
        :param writePermission: String: The permission that provides overall
        write access, or null to not do this check.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :param modeFlags: int: The access modes to check.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :return: int. PackageManager.PERMISSION_GRANTED if the caller is
        allowed to access that uri or holds one of the given permissions, or
        PackageManager.PERMISSION_DENIED if it is not. Value is
        PERMISSION_GRANTED or PERMISSION_DENIED.
        """
        pass

    @checkUriPermission.adddef('Uri', 'int', 'int', 'int')
    def checkUriPermission(self, uri, pid, uid, modeFlags):
        """
        Determine whether a particular process and user ID has been granted
        permission to access a specific URI.  This only checks for permissions
        that have been explicitly granted -- if the given process/uid has more
        general access to the URI's content provider then this check will
        always fail.
        :param uri: Uri: The uri that is being checked.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :param modeFlags: int: The access modes to check.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :return: int. PackageManager.PERMISSION_GRANTED if the given pid/uid
        is allowed to access that uri, or PackageManager.PERMISSION_DENIED if
        it is not.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also: checkCallingUriPermission(Uri, int)
        """
        pass

    def clearWallpaper(self):
        """
        This method was deprecated in API level 5. Use
        WallpaperManager.clear() instead. This method requires the caller to
        hold the permission Manifest.permission.SET_WALLPAPER.
        :raises: IOException
        """
        pass

    def createConfigurationContext(self, overrideConfiguration):
        """
        Return a new Context object for the current Context but whose
        resources are adjusted to match the given Configuration.  Each call to
        this method returns a new instance of a Context object; Context
        objects are not shared, however common state (ClassLoader, other
        Resources for the same configuration) may be so the Context itself can
        be fairly lightweight.
        :param overrideConfiguration: Configuration: A Configuration
        specifying what values to modify in the base Configuration of the
        original Context's resources.  If the base configuration changes (such
        as due to an orientation change), the resources of this context will
        also change except for those that have been explicitly overridden with
        a value here.This value must never be null.
        :return: Context. A Context with the given configuration override.
        """
        pass

    def createContextForSplit(self, splitName):
        """
        Return a new Context object for the given split name. The new Context
        has a ClassLoader and Resources object that can access the split's and
        all of its dependencies' code/resources. Each call to this method
        returns a new instance of a Context object; Context objects are not
        shared, however common state (ClassLoader, other Resources for the
        same split) may be so the Context itself can be fairly lightweight.
        :param splitName: String: The name of the split to include, as
        declared in the split's AndroidManifest.xml.
        :return: Context. A Context with the given split's code and/or
        resources loaded.
        :raises: PackageManager.NameNotFoundException
        """
        pass

    def createDeviceProtectedStorageContext(self):
        """
        Return a new Context object for the current Context but whose storage
        APIs are backed by device-protected storage.  On devices with direct
        boot, data stored in this location is encrypted with a key tied to the
        physical device, and it can be accessed immediately after the device
        has booted successfully, both before and after the user has
        authenticated with their credentials (such as a lock pattern or PIN).
        Because device-protected data is available without user
        authentication, you should carefully limit the data you store using
        this Context. For example, storing sensitive authentication tokens or
        passwords in the device-protected area is strongly discouraged.  If
        the underlying device does not have the ability to store
        device-protected and credential-protected data using different keys,
        then both storage areas will become available at the same time. They
        remain as two distinct storage locations on disk, and only the window
        of availability changes.  Each call to this method returns a new
        instance of a Context object; Context objects are not shared, however
        common state (ClassLoader, other Resources for the same configuration)
        may be so the Context itself can be fairly lightweight.
        :return: Context.
        See also: isDeviceProtectedStorage()
        """
        pass

    def createDisplayContext(self, display):
        """
        Return a new Context object for the current Context but whose
        resources are adjusted to match the metrics of the given Display.
        Each call to this method returns a new instance of a Context object;
        Context objects are not shared, however common state (ClassLoader,
        other Resources for the same configuration) may be so the Context
        itself can be fairly lightweight.  The returned display Context
        provides a WindowManager (see getSystemService(String)) that is
        configured to show windows on the given display.  The WindowManager's
        WindowManager.getDefaultDisplay() method can be used to retrieve the
        Display from the returned Context.
        :param display: Display: A Display object specifying the display for
        whose metrics the Context's resources should be tailored and upon
        which new windows should be shown.This value must never be null.
        :return: Context. A Context for the display.
        """
        pass

    def createPackageContext(self, packageName, flags):
        """
        Return a new Context object for the given application name.  This
        Context is the same as what the named application gets when it is
        launched, containing the same resources and class loader.  Each call
        to this method returns a new instance of a Context object; Context
        objects are not shared, however they share common state (Resources,
        ClassLoader, etc) so the Context instance itself is fairly
        lightweight.  Throws PackageManager.NameNotFoundException if there is
        no application with the given package name.  Throws SecurityException
        if the Context requested can not be loaded into the caller's process
        for security reasons (see CONTEXT_INCLUDE_CODE for more information}.
        :param packageName: String: Name of the application's package.
        :param flags: int: Option flags.Value is either 0 or combination of
        CONTEXT_INCLUDE_CODE, CONTEXT_IGNORE_SECURITY or CONTEXT_RESTRICTED.
        :return: Context. A Context for the application.
        :raises SecurityException: if there is no application with the
        given package name. PackageManager.NameNotFoundException
        """
        pass

    def databaseList(self):
        """
        Returns an array of strings naming the private databases associated
        with this Context's application package.
        :return: String[]. Array of strings naming the private databases.
        See also:
        openOrCreateDatabase(String, int,SQLiteDatabase.CursorFactory)
        deleteDatabase(String)
        """
        pass

    def deleteDatabase(self, name):
        """
        Delete an existing private SQLiteDatabase associated with this
        Context's application package.
        :param name: String: The name (unique in the application package) of
        the database.
        :return: boolean. true if the database was successfully deleted; else
        false.
        See also:
        openOrCreateDatabase(String, int,SQLiteDatabase.CursorFactory)
        """
        pass

    def deleteFile(self, name):
        """
        Delete the given private file associated with this Context's
        application package.
        :param name: String: The name of the file to delete; can not contain
        path separators.
        :return: boolean. true if the file was successfully deleted; else
        false.
        See also: openFileInput(String)openFileOutput(String,
        int)fileList()File.delete()
        """
        pass

    def deleteSharedPreferences(self, name):
        """
        Delete an existing shared preferences file.
        :param name: String: The name (unique in the application package) of
        the shared preferences file.
        :return: boolean. true if the shared preferences file was successfully
        deleted; else false.
        See also: getSharedPreferences(String, int)
        """
        pass

    def enforceCallingOrSelfPermission(self, permission, message):
        """
        If neither you nor the calling process of an IPC you are handling has
        been granted a particular permission, throw a SecurityException.  This
        is the same as enforceCallingPermission(String, String), except it
        grants your own permissions if you are not currently processing an
        IPC.  Use with care!
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :param message: String: A message to include in the exception if it is
        thrown.This value may be null.
        See also: checkCallingOrSelfPermission(String)
        """
        pass

    def enforceCallingOrSelfUriPermission(self, uri, modeFlags, message):
        """
        If the calling process of an IPC or you has not been granted
        permission to access a specific URI, throw SecurityException.  This is
        the same as enforceCallingUriPermission(Uri, int, String), except it
        grants your own permissions if you are not currently processing an
        IPC.  Use with care!
        :param uri: Uri: The uri that is being checked.
        :param modeFlags: int: The access modes to enforce.Value is either 0
        or combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :param message: String: A message to include in the exception if it is
        thrown.
        See also: checkCallingOrSelfUriPermission(Uri, int)
        """
        pass

    def enforceCallingPermission(self, permission, message):
        """
        If the calling process of an IPC you are handling has not been granted
        a particular permission, throw a SecurityException.  This is basically
        the same as calling enforcePermission(String, int, int, String) with
        the pid and uid returned by Binder.getCallingPid() and
        Binder.getCallingUid().  One important difference is that if you are
        not currently processing an IPC, this function will always throw the
        SecurityException.  This is done to protect against accidentally
        leaking permissions; you can use
        enforceCallingOrSelfPermission(String, String) to avoid this
        protection.
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :param message: String: A message to include in the exception if it is
        thrown.This value may be null.
        See also: checkCallingPermission(String)
        """
        pass

    def enforceCallingUriPermission(self, uri, modeFlags, message):
        """
        If the calling process and user ID has not been granted permission to
        access a specific URI, throw SecurityException.  This is basically the
        same as calling enforceUriPermission(Uri, int, int, int, String) with
        the pid and uid returned by Binder.getCallingPid() and
        Binder.getCallingUid().  One important difference is that if you are
        not currently processing an IPC, this function will always throw a
        SecurityException.
        :param uri: Uri: The uri that is being checked.
        :param modeFlags: int: The access modes to enforce.Value is either 0
        or combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :param message: String: A message to include in the exception if it is
        thrown.
        See also: checkCallingUriPermission(Uri, int)
        """
        pass

    def enforcePermission(self, permission, pid, uid, message):
        """
        If the given permission is not allowed for a particular process and
        user ID running in the system, throw a SecurityException.
        :param permission: String: The name of the permission being
        checked.This value must never be null.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :param message: String: A message to include in the exception if it is
        thrown.This value may be null.
        See also: checkPermission(String, int, int)
        """
        pass

    @overload('Uri', 'str', 'str', 'int', 'int', 'int', 'str')
    def enforceUriPermission(self, uri, readPermission, writePermission, pid, uid, modeFlags, message):
        """
        Enforce both a Uri and normal permission.  This allows you to perform
        both enforcePermission(String, int, int, String) and
        enforceUriPermission(Uri, int, int, int, String) in one call.
        :param uri: Uri: The Uri whose permission is to be checked, or null to
        not do this check.
        :param readPermission: String: The permission that provides overall
        read access, or null to not do this check.
        :param writePermission: String: The permission that provides overall
        write access, or null to not do this check.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :param modeFlags: int: The access modes to enforce.Value is either 0
        or combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :param message: String: A message to include in the exception if it is
        thrown.This value may be null.
        See also: checkUriPermission(Uri, String, String, int, int, int)
        """
        pass

    @enforceUriPermission.adddef('Uri', 'int', 'int', 'int', 'str')
    def enforceUriPermission(self, uri, pid, uid, modeFlags, message):
        """
        If a particular process and user ID has not been granted permission to
        access a specific URI, throw SecurityException.  This only checks for
        permissions that have been explicitly granted -- if the given
        process/uid has more general access to the URI's content provider then
        this check will always fail.
        :param uri: Uri: The uri that is being checked.
        :param pid: int: The process ID being checked against.  Must be > 0.
        :param uid: int: The user ID being checked against.  A uid of 0 is the
        root user, which will pass every permission check.
        :param modeFlags: int: The access modes to enforce.Value is either 0
        or combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        :param message: String: A message to include in the exception if it is
        thrown.
        See also: checkUriPermission(Uri, int, int, int)
        """
        pass

    def fileList(self):
        """
        Returns an array of strings naming the private files associated with
        this Context's application package.
        :return: String[]. Array of strings naming the private files.
        See also: openFileInput(String)openFileOutput(String,
        int)deleteFile(String)
        """
        pass

    def getApplicationContext(self):
        """
        Return the context of the single, global Application object of the
        current process.  This generally should only be used if you need a
        Context whose lifecycle is separate from the current context, that is
        tied to the lifetime of the process rather than the current component.
         Consider for example how this interacts with
        registerReceiver(BroadcastReceiver, IntentFilter): If used from an
        Activity context, the receiver is being registered within that
        activity.  This means that you are expected to unregister before the
        activity is done being destroyed; in fact if you do not do so, the
        framework will clean up your leaked registration as it removes the
        activity and log an error.  Thus, if you use the Activity context to
        register a receiver that is static (global to the process, not
        associated with an Activity instance) then that registration will be
        removed on you at whatever point the activity you used is destroyed.
        If used from the Context returned here, the receiver is being
        registered with the global state associated with your application.
        Thus it will never be unregistered for you.  This is necessary if the
        receiver is associated with static data, not a particular component.
        However using the ApplicationContext elsewhere can easily lead to
        serious leaks if you forget to unregister, unbind, etc.
        :return: Context.
        """
        pass

    def getApplicationInfo(self):
        """
        Return the full application info for this context's package.
        :return: ApplicationInfo.
        """
        pass

    def getAssets(self):
        """
        Returns an AssetManager instance for the application's package. Note:
        Implementations of this method should return an AssetManager instance
        that is consistent with the Resources instance returned by
        getResources(). For example, they should share the same Configuration
        object.
        :return: AssetManager. an AssetManager instance for the application's
        package
        See also: getResources()
        """
        pass

    def getCacheDir(self):
        """
        Returns the absolute path to the application specific cache directory
        on the filesystem.  The system will automatically delete files in this
        directory as disk space is needed elsewhere on the device. The system
        will always delete older files first, as reported by
        File.lastModified(). If desired, you can exert more control over how
        files are deleted using StorageManager.setCacheBehaviorGroup(File,
        boolean) and StorageManager.setCacheBehaviorTombstone(File, boolean).
        Apps are strongly encouraged to keep their usage of cache space below
        the quota returned by
        StorageManager.getCacheQuotaBytes(java.util.UUID). If your app goes
        above this quota, your cached files will be some of the first to be
        deleted when additional disk space is needed. Conversely, if your app
        stays under this quota, your cached files will be some of the last to
        be deleted when additional disk space is needed.  Note that your cache
        quota will change over time depending on how frequently the user
        interacts with your app, and depending on how much system-wide disk
        space is used.  The returned path may change over time if the calling
        app is moved to an adopted storage device, so only relative paths
        should be persisted.  Apps require no extra permissions to read or
        write to the returned path, since this path lives in their private
        storage.
        :return: File. The path of the directory holding application cache
        files.
        See also: openFileOutput(String,int)
        getFileStreamPath(String)getDir(String, int)
        getExternalCacheDir()
        """
        pass

    def getClassLoader(self):
        """
        Return a class loader you can use to retrieve classes in this package.
        :return: ClassLoader.
        """
        pass

    def getCodeCacheDir(self):
        """
        Returns the absolute path to the application specific cache directory
        on the filesystem designed for storing cached code.  The system will
        delete any files stored in this location both when your specific
        application is upgraded, and when the entire platform is upgraded.
        This location is optimal for storing compiled or optimized code
        generated by your application at runtime.  The returned path may
        change over time if the calling app is moved to an adopted storage
        device, so only relative paths should be persisted.  Apps require no
        extra permissions to read or write to the returned path, since this
        path lives in their private storage.
        :return: File. The path of the directory holding application code
        cache files.
        """
        pass

    def getColor(self, id):
        """
        Returns a color associated with a particular resource ID and styled
        for the current theme.
        :param id: int: The desired resource identifier, as generated by the
        aapt tool. This integer encodes the package, type, and resource entry.
        The value 0 is an invalid identifier.
        :return: int. A single color value in the form 0xAARRGGBB.
        :raises: Resources.NotFoundExceptionif the given ID does not exist.
        """
        pass

    def getColorStateList(self, id):
        """
        Returns a color state list associated with a particular resource ID
        and styled for the current theme.
        :param id: int: The desired resource identifier, as generated by the
        aapt tool. This integer encodes the package, type, and resource entry.
        The value 0 is an invalid identifier.
        :return: ColorStateList. A color state list.This value will never be
        null.
        :raises: Resources.NotFoundExceptionif the given ID does not exist.
        """
        pass

    def getContentResolver(self):
        """
        Return a ContentResolver instance for your application's package.
        :return: ContentResolver.
        """
        pass

    def getDataDir(self):
        """
        Returns the absolute path to the directory on the filesystem where all
        private files belonging to this app are stored. Apps should not use
        this path directly; they should instead use getFilesDir(),
        getCacheDir(), getDir(String, int), or other storage APIs on this
        class.  The returned path may change over time if the calling app is
        moved to an adopted storage device, so only relative paths should be
        persisted.  No additional permissions are required for the calling app
        to read or write files under the returned path.
        :return: File.
        See also: ApplicationInfo.dataDir
        """
        pass

    def getDatabasePath(self, name):
        """
        Returns the absolute path on the filesystem where a database created
        with openOrCreateDatabase(String, int, SQLiteDatabase.CursorFactory)
        is stored.  The returned path may change over time if the calling app
        is moved to an adopted storage device, so only relative paths should
        be persisted.
        :param name: String: The name of the database for which you would like
        to get its path.
        :return: File. An absolute path to the given database.
        See also: openOrCreateDatabase(String, int,
        SQLiteDatabase.CursorFactory)
        """
        pass

    def getDir(self, name, mode):
        """
        Retrieve, creating if needed, a new directory in which the application
        can place its own custom data files.  You can use the returned File
        object to create and access files in this directory.  Note that files
        created through a File object will only be accessible by your own
        application; you can only set the mode of the entire directory, not of
        individual files.  The returned path may change over time if the
        calling app is moved to an adopted storage device, so only relative
        paths should be persisted.  Apps require no extra permissions to read
        or write to the returned path, since this path lives in their private
        storage.
        :param name: String: Name of the directory to retrieve.  This is a
        directory that is created as part of your application data.
        :param mode: int: Operating mode.Value is either 0 or combination of
        MODE_PRIVATE, MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE or MODE_APPEND.
        :return: File. A File object for the requested directory.  The
        directory will have been created if it does not already exist.
        See also: openFileOutput(String, int)
        """
        pass

    def getDrawable(self, id):
        """
        Returns a drawable object associated with a particular resource ID and
        styled for the current theme.
        :param id: int: The desired resource identifier, as generated by the
        aapt tool. This integer encodes the package, type, and resource entry.
        The value 0 is an invalid identifier.
        :return: Drawable. An object that can be used to draw this
        resource.This value may be null.
        :raises: Resources.NotFoundExceptionif the given ID does not exist.
        """
        pass

    def getExternalCacheDir(self):
        """
        Returns absolute path to application-specific directory on the primary
        shared/external storage device where the application can place cache
        files it owns. These files are internal to the application, and not
        typically visible to the user as media.  This is like getCacheDir() in
        that these files will be deleted when the application is uninstalled,
        however there are some important differences: The platform does not
        always monitor the space available in shared storage, and thus may not
        automatically delete these files. Apps should always manage the
        maximum space used in this location. Currently the only time files
        here will be deleted by the platform is when running on
        Build.VERSION_CODES.JELLY_BEAN_MR1 or later and
        Environment.isExternalStorageEmulated(File) returns true. Shared
        storage may not always be available, since removable media can be
        ejected by the user. Media state can be checked using
        Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        If a shared storage device is emulated (as determined by
        Environment.isExternalStorageEmulated(File)), its contents are backed
        by a private user data partition, which means there is little benefit
        to storing data here instead of the private directory returned by
        getCacheDir().  Starting in Build.VERSION_CODES.KITKAT, no permissions
        are required to read or write to the returned path; it's always
        accessible to the calling app. This only applies to paths generated
        for package name of the calling application. To access paths belonging
        to other packages, Manifest.permission.WRITE_EXTERNAL_STORAGE and/or
        Manifest.permission.READ_EXTERNAL_STORAGE are required.  On devices
        with multiple users (as described by UserManager), each user has their
        own isolated shared storage. Applications only have access to the
        shared storage for the user they're running as.  The returned path may
        change over time if different shared storage media is inserted, so
        only relative paths should be persisted.
        :return: File. the absolute path to application-specific directory.
        May return null if shared storage is not currently available.
        See also:

        getCacheDir()getExternalCacheDirs()Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getExternalCacheDirs(self):
        """
        Returns absolute paths to application-specific directories on all
        shared/external storage devices where the application can place cache
        files it owns. These files are internal to the application, and not
        typically visible to the user as media.  This is like getCacheDir() in
        that these files will be deleted when the application is uninstalled,
        however there are some important differences: The platform does not
        always monitor the space available in shared storage, and thus may not
        automatically delete these files. Apps should always manage the
        maximum space used in this location. Currently the only time files
        here will be deleted by the platform is when running on
        Build.VERSION_CODES.JELLY_BEAN_MR1 or later and
        Environment.isExternalStorageEmulated(File) returns true. Shared
        storage may not always be available, since removable media can be
        ejected by the user. Media state can be checked using
        Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        If a shared storage device is emulated (as determined by
        Environment.isExternalStorageEmulated(File)), it's contents are backed
        by a private user data partition, which means there is little benefit
        to storing data here instead of the private directory returned by
        getCacheDir().  Shared storage devices returned here are considered a
        stable part of the device, including physical media slots under a
        protective cover. The returned paths do not include transient devices,
        such as USB flash drives connected to handheld devices.  An
        application may store data on any or all of the returned devices. For
        example, an app may choose to store large files on the device with the
        most available space, as measured by StatFs.  No additional
        permissions are required for the calling app to read or write files
        under the returned path. Write access outside of these paths on
        secondary external storage devices is not available.  The returned
        paths may change over time if different shared storage media is
        inserted, so only relative paths should be persisted.
        :return: File[]. the absolute paths to application-specific
        directories. Some individual paths may be null if that shared storage
        is not currently available. The first path returned is the same as
        getExternalCacheDir().
        See also:

        getExternalCacheDir()Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getExternalFilesDir(self, type):
        """
        Returns the absolute path to the directory on the primary
        shared/external storage device where the application can place
        persistent files it owns. These files are internal to the
        applications, and not typically visible to the user as media.  This is
        like getFilesDir() in that these files will be deleted when the
        application is uninstalled, however there are some important
        differences: Shared storage may not always be available, since
        removable media can be ejected by the user. Media state can be checked
        using Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        If a shared storage device is emulated (as determined by
        Environment.isExternalStorageEmulated(File)), it's contents are backed
        by a private user data partition, which means there is little benefit
        to storing data here instead of the private directories returned by
        getFilesDir(), etc.  Starting in Build.VERSION_CODES.KITKAT, no
        permissions are required to read or write to the returned path; it's
        always accessible to the calling app. This only applies to paths
        generated for package name of the calling application. To access paths
        belonging to other packages,
        Manifest.permission.WRITE_EXTERNAL_STORAGE and/or
        Manifest.permission.READ_EXTERNAL_STORAGE are required.  On devices
        with multiple users (as described by UserManager), each user has their
        own isolated shared storage. Applications only have access to the
        shared storage for the user they're running as.  The returned path may
        change over time if different shared storage media is inserted, so
        only relative paths should be persisted.  Here is an example of
        typical code to manipulate a file in an application's shared storage:
        void createExternalStoragePrivateFile() { // Create a path where we
        will place our private file on external // storage. File file = new
        File(getExternalFilesDir(null), "DemoFile.jpg");  try { // Very simple
        code to copy a picture from the application's // resource into the
        external file.  Note that this code does // no error checking, and
        assumes the picture is small (does not // try to copy it in chunks).
        Note that if external storage is // not currently mounted this will
        silently fail. InputStream is =
        getResources().openRawResource(R.drawable.balloons); OutputStream os =
        new FileOutputStream(file); byte[] data = new byte[is.available()];
        is.read(data); os.write(data); is.close(); os.close(); } catch
        (IOException e) { // Unable to create file, likely because external
        storage is // not currently mounted. Log.w("ExternalStorage", "Error
        writing " + file, e); } }  void deleteExternalStoragePrivateFile() {
        // Get path for the file on external storage.  If external // storage
        is not currently mounted this will fail. File file = new
        File(getExternalFilesDir(null), "DemoFile.jpg"); if (file != null) {
        file.delete(); } }  boolean hasExternalStoragePrivateFile() { // Get
        path for the file on external storage.  If external // storage is not
        currently mounted this will fail. File file = new
        File(getExternalFilesDir(null), "DemoFile.jpg"); if (file != null) {
        return file.exists(); } return false; } If you supply a non-null type
        to this function, the returned file will be a path to a sub-directory
        of the given type. Though these files are not automatically scanned by
        the media scanner, you can explicitly add them to the media database
        with MediaScannerConnection.scanFile. Note that this is not the same
        as Environment.getExternalStoragePublicDirectory(), which provides
        directories of media shared by all applications. The directories
        returned here are owned by the application, and their contents will be
        removed when the application is uninstalled. Unlike
        Environment.getExternalStoragePublicDirectory(), the directory
        returned here will be automatically created for you.  Here is an
        example of typical code to manipulate a picture in an application's
        shared storage and add it to the media database: void
        createExternalStoragePrivatePicture() { // Create a path where we will
        place our picture in our own private // pictures directory.  Note that
        we don't really need to place a // picture in DIRECTORY_PICTURES,
        since the media scanner will see // all media in these directories;
        this may be useful with other // media types such as DIRECTORY_MUSIC
        however to help it classify // your media for display to the user.
        File path = getExternalFilesDir(Environment.DIRECTORY_PICTURES); File
        file = new File(path, "DemoPicture.jpg");  try { // Very simple code
        to copy a picture from the application's // resource into the external
        file.  Note that this code does // no error checking, and assumes the
        picture is small (does not // try to copy it in chunks).  Note that if
        external storage is // not currently mounted this will silently fail.
        InputStream is = getResources().openRawResource(R.drawable.balloons);
        OutputStream os = new FileOutputStream(file); byte[] data = new
        byte[is.available()]; is.read(data); os.write(data); is.close();
        os.close();  // Tell the media scanner about the new file so that it
        is // immediately available to the user.
        MediaScannerConnection.scanFile(this, new String[] { file.toString()
        }, null, new MediaScannerConnection.OnScanCompletedListener() { public
        void onScanCompleted(String path, Uri uri) { Log.i("ExternalStorage",
        "Scanned " + path + ":"); Log.i("ExternalStorage", "-> uri=" + uri); }
        }); } catch (IOException e) { // Unable to create file, likely because
        external storage is // not currently mounted. Log.w("ExternalStorage",
        "Error writing " + file, e); } }  void
        deleteExternalStoragePrivatePicture() { // Create a path where we will
        place our picture in the user's // public pictures directory and
        delete the file.  If external // storage is not currently mounted this
        will fail. File path =
        getExternalFilesDir(Environment.DIRECTORY_PICTURES); if (path != null)
        { File file = new File(path, "DemoPicture.jpg"); file.delete(); } }
        boolean hasExternalStoragePrivatePicture() { // Create a path where we
        will place our picture in the user's // public pictures directory and
        check if the file exists.  If // external storage is not currently
        mounted this will think the // picture doesn't exist. File path =
        getExternalFilesDir(Environment.DIRECTORY_PICTURES); if (path != null)
        { File file = new File(path, "DemoPicture.jpg"); return file.exists();
        } return false; }
        :param type: String: The type of files directory to return. May be
        null for the root of the files directory or one of the following
        constants for a subdirectory: Environment.DIRECTORY_MUSIC,
        Environment.DIRECTORY_PODCASTS, Environment.DIRECTORY_RINGTONES,
        Environment.DIRECTORY_ALARMS, Environment.DIRECTORY_NOTIFICATIONS,
        Environment.DIRECTORY_PICTURES, or Environment.DIRECTORY_MOVIES.
        :return: File. the absolute path to application-specific directory.
        May return null if shared storage is not currently available.
        See also:

        getFilesDir()getExternalFilesDirs(String)Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getExternalFilesDirs(self, type):
        """
        Returns absolute paths to application-specific directories on all
        shared/external storage devices where the application can place
        persistent files it owns. These files are internal to the application,
        and not typically visible to the user as media.  This is like
        getFilesDir() in that these files will be deleted when the application
        is uninstalled, however there are some important differences: Shared
        storage may not always be available, since removable media can be
        ejected by the user. Media state can be checked using
        Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        If a shared storage device is emulated (as determined by
        Environment.isExternalStorageEmulated(File)), it's contents are backed
        by a private user data partition, which means there is little benefit
        to storing data here instead of the private directories returned by
        getFilesDir(), etc.  Shared storage devices returned here are
        considered a stable part of the device, including physical media slots
        under a protective cover. The returned paths do not include transient
        devices, such as USB flash drives connected to handheld devices.  An
        application may store data on any or all of the returned devices. For
        example, an app may choose to store large files on the device with the
        most available space, as measured by StatFs.  No additional
        permissions are required for the calling app to read or write files
        under the returned path. Write access outside of these paths on
        secondary external storage devices is not available.  The returned
        path may change over time if different shared storage media is
        inserted, so only relative paths should be persisted.
        :param type: String: The type of files directory to return. May be
        null for the root of the files directory or one of the following
        constants for a subdirectory: Environment.DIRECTORY_MUSIC,
        Environment.DIRECTORY_PODCASTS, Environment.DIRECTORY_RINGTONES,
        Environment.DIRECTORY_ALARMS, Environment.DIRECTORY_NOTIFICATIONS,
        Environment.DIRECTORY_PICTURES, or Environment.DIRECTORY_MOVIES.
        :return: File[]. the absolute paths to application-specific
        directories. Some individual paths may be null if that shared storage
        is not currently available. The first path returned is the same as
        getExternalFilesDir(String).
        See also:

        getExternalFilesDir(String)Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getExternalMediaDirs(self):
        """
        Returns absolute paths to application-specific directories on all
        shared/external storage devices where the application can place media
        files. These files are scanned and made available to other apps
        through MediaStore.  This is like getExternalFilesDirs(String) in that
        these files will be deleted when the application is uninstalled,
        however there are some important differences: Shared storage may not
        always be available, since removable media can be ejected by the user.
        Media state can be checked using
        Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        Shared storage devices returned here are considered a stable part of
        the device, including physical media slots under a protective cover.
        The returned paths do not include transient devices, such as USB flash
        drives connected to handheld devices.  An application may store data
        on any or all of the returned devices. For example, an app may choose
        to store large files on the device with the most available space, as
        measured by StatFs.  No additional permissions are required for the
        calling app to read or write files under the returned path. Write
        access outside of these paths on secondary external storage devices is
        not available.  The returned paths may change over time if different
        shared storage media is inserted, so only relative paths should be
        persisted.
        :return: File[]. the absolute paths to application-specific
        directories. Some individual paths may be null if that shared storage
        is not currently available.
        See also:

        Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getFileStreamPath(self, name):
        """
        Returns the absolute path on the filesystem where a file created with
        openFileOutput(String, int) is stored.  The returned path may change
        over time if the calling app is moved to an adopted storage device, so
        only relative paths should be persisted.
        :param name: String: The name of the file for which you would like to
        get its path.
        :return: File. An absolute path to the given file.
        See also: openFileOutput(String, int)getFilesDir()getDir(String, int)
        """
        pass

    def getFilesDir(self):
        """
        Returns the absolute path to the directory on the filesystem where
        files created with openFileOutput(String, int) are stored.  The
        returned path may change over time if the calling app is moved to an
        adopted storage device, so only relative paths should be persisted.
        No additional permissions are required for the calling app to read or
        write files under the returned path.
        :return: File. The path of the directory holding application files.
        See also: openFileOutput(String,
        int)getFileStreamPath(String)getDir(String, int)
        """
        pass

    def getMainExecutor(self):
        """
        Return an Executor that will run enqueued tasks on the main thread
        associated with this context. This is the thread used to dispatch
        calls to application components (activities, services, etc).
        :return: Executor.
        """
        pass

    def getMainLooper(self):
        """
        Return the Looper for the main thread of the current process.  This is
        the thread used to dispatch calls to application components
        (activities, services, etc).  By definition, this method returns the
        same result as would be obtained by calling Looper.getMainLooper().
        :return: Looper. The main looper.
        """
        pass

    def getNoBackupFilesDir(self):
        """
        Returns the absolute path to the directory on the filesystem similar
        to getFilesDir(). The difference is that files placed under this
        directory will be excluded from automatic backup to remote storage.
        See BackupAgent for a full discussion of the automatic backup
        mechanism in Android.  The returned path may change over time if the
        calling app is moved to an adopted storage device, so only relative
        paths should be persisted.  No additional permissions are required for
        the calling app to read or write files under the returned path.
        :return: File. The path of the directory holding application files
        that will not be automatically backed up to remote storage.
        See also: openFileOutput(String,
        int)getFileStreamPath(String)getDir(String, int)BackupAgent
        """
        pass

    def getObbDir(self):
        """
        Return the primary shared/external storage directory where this
        application's OBB files (if there are any) can be found. Note if the
        application does not have any OBB files, this directory may not exist.
         This is like getFilesDir() in that these files will be deleted when
        the application is uninstalled, however there are some important
        differences: Shared storage may not always be available, since
        removable media can be ejected by the user. Media state can be checked
        using Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        Starting in Build.VERSION_CODES.KITKAT, no permissions are required to
        read or write to the path that this method returns. However, starting
        from Build.VERSION_CODES.M, to read the OBB expansion files, you must
        declare the Manifest.permission.READ_EXTERNAL_STORAGE permission in
        the app manifest and ask for permission at runtime as follows:
        <uses-permission
        android:name="android.permission.READ_EXTERNAL_STORAGE"
        android:maxSdkVersion="23" /> Starting from Build.VERSION_CODES.N,
        Manifest.permission.READ_EXTERNAL_STORAGE permission is not required,
        so don’t ask for this permission at runtime. To handle both cases,
        your app must first try to read the OBB file, and if it fails, you
        must request Manifest.permission.READ_EXTERNAL_STORAGE permission at
        runtime.  The following code snippet shows how to do this:  File obb =
        new File(obb_filename); boolean open_failed = false;  try {
        BufferedReader br = new BufferedReader(new FileReader(obb));
        open_failed = false; ReadObbFile(br); } catch (IOException e) {
        open_failed = true; }  if (open_failed) { // request
        READ_EXTERNAL_STORAGE permission before reading OBB file
        ReadObbFileWithPermission(); }   On devices with multiple users (as
        described by UserManager), multiple users may share the same OBB
        storage location. Applications should ensure that multiple instances
        running under different users don't interfere with each other.
        :return: File. the absolute path to application-specific directory.
        May return null if shared storage is not currently available.
        See also:

        getObbDirs()Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getObbDirs(self):
        """
        Returns absolute paths to application-specific directories on all
        shared/external storage devices where the application's OBB files (if
        there are any) can be found. Note if the application does not have any
        OBB files, these directories may not exist.  This is like
        getFilesDir() in that these files will be deleted when the application
        is uninstalled, however there are some important differences: Shared
        storage may not always be available, since removable media can be
        ejected by the user. Media state can be checked using
        Environment.getExternalStorageState(File). There is no security
        enforced with these files. For example, any application holding
        Manifest.permission.WRITE_EXTERNAL_STORAGE can write to these files.
        Shared storage devices returned here are considered a stable part of
        the device, including physical media slots under a protective cover.
        The returned paths do not include transient devices, such as USB flash
        drives connected to handheld devices.  An application may store data
        on any or all of the returned devices. For example, an app may choose
        to store large files on the device with the most available space, as
        measured by StatFs.  No additional permissions are required for the
        calling app to read or write files under the returned path. Write
        access outside of these paths on secondary external storage devices is
        not available.
        :return: File[]. the absolute paths to application-specific
        directories. Some individual paths may be null if that shared storage
        is not currently available. The first path returned is the same as
        getObbDir()
        See also:

        getObbDir()Environment.getExternalStorageState(File)Environment.isExternalStorageEmulated(File)Environment.isExternalStorageRemovable(File)
        """
        pass

    def getPackageCodePath(self):
        """
        Return the full path to this context's primary Android package. The
        Android package is a ZIP file which contains application's primary
        code and assets.  Note: this is not generally useful for applications,
        since they should not be directly accessing the file system.
        :return: String. String Path to the code and assets.
        """
        pass

    def getPackageManager(self):
        """
        Return PackageManager instance to find global package information.
        :return: PackageManager.
        """
        pass

    def getPackageName(self):
        """
        Return the name of this application's package.
        :return: String.
        """
        pass

    def getPackageResourcePath(self):
        """
        Return the full path to this context's primary Android package. The
        Android package is a ZIP file which contains the application's primary
        resources.  Note: this is not generally useful for applications, since
        they should not be directly accessing the file system.
        :return: String. String Path to the resources.
        """
        pass

    def getResources(self):
        """
        Returns a Resources instance for the application's package. Note:
        Implementations of this method should return a Resources instance that
        is consistent with the AssetManager instance returned by getAssets().
        For example, they should share the same Configuration object.
        :return: Resources. a Resources instance for the application's package
        See also: getAssets()
        """
        pass

    def getSharedPreferences(self, name, mode):
        """
        Retrieve and hold the contents of the preferences file 'name',
        returning a SharedPreferences through which you can retrieve and
        modify its values.  Only one instance of the SharedPreferences object
        is returned to any callers for the same name, meaning they will see
        each other's edits as soon as they are made.  This method is
        thead-safe.
        :param name: String: Desired preferences file. If a preferences file
        by this name does not exist, it will be created when you retrieve an
        editor (SharedPreferences.edit()) and then commit changes
        (Editor.commit()).
        :param mode: int: Operating mode.Value is either 0 or combination of
        MODE_PRIVATE, MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE or
        MODE_MULTI_PROCESS.
        :return: SharedPreferences. The single SharedPreferences instance that
        can be used to retrieve and modify the preference values.
        See also: MODE_PRIVATE
        """
        pass

    @overload('int', 'Object')
    def getString(self, resId, formatArgs):
        """
        Returns a localized formatted string from the application's package's
        default string table, substituting the format arguments as defined in
        Formatter and String.format(String, Object...).
        :param resId: int: Resource id for the format string
        :param formatArgs: Object: The format arguments that will be used for
        substitution.
        :return: String. The string data associated with the resource,
        formatted and stripped of styled text information. This value will
        never be null.
        """
        pass

    @getString.adddef('int')
    def getString(self, resId):
        """
        Returns a localized string from the application's package's default
        string table.
        :param resId: int: Resource id for the string
        :return: String. The string data associated with the resource,
        stripped of styled text information. This value will never be null.
        """
        pass

    @overload('type')
    def getSystemService(self, serviceClass):
        """
        Return the handle to a system-level service by class.  Currently
        available classes are: WindowManager, LayoutInflater, ActivityManager,
        PowerManager, AlarmManager, NotificationManager, KeyguardManager,
        LocationManager, SearchManager, Vibrator, ConnectivityManager,
        WifiManager, AudioManager, MediaRouter, TelephonyManager,
        SubscriptionManager, InputMethodManager, UiModeManager,
        DownloadManager, BatteryManager, JobScheduler, NetworkStatsManager.
        Note: System services obtained via this API may be closely associated
        with the Context in which they are obtained from.  In general, do not
        share the service objects between various different contexts
        (Activities, Applications, Services, Providers, etc.) Note: Instant
        apps, for which PackageManager.isInstantApp() returns true, don't have
        access to the following system services: DEVICE_POLICY_SERVICE,
        FINGERPRINT_SERVICE, SHORTCUT_SERVICE, USB_SERVICE, WALLPAPER_SERVICE,
        WIFI_P2P_SERVICE, WIFI_SERVICE, WIFI_AWARE_SERVICE. For these services
        this method will return null. Generally, if you are running as an
        instant app you should always check whether the result of this method
        is null.
        :param serviceClass: Class: The class of the desired service.This
        value must never be null.
        :return: T. The service or null if the class is not a supported system
        service.
        """
        pass

    @getSystemService.adddef('str')
    def getSystemService(self, name):
        """
        Return the handle to a system-level service by name. The class of the
        returned object varies by the requested name. Currently available
        names are:  WINDOW_SERVICE ("window") The top-level window manager in
        which you can place custom windows.  The returned object is a
        WindowManager. LAYOUT_INFLATER_SERVICE ("layout_inflater") A
        LayoutInflater for inflating layout resources in this context.
        ACTIVITY_SERVICE ("activity") A ActivityManager for interacting with
        the global activity state of the system. POWER_SERVICE ("power") A
        PowerManager for controlling power management. ALARM_SERVICE ("alarm")
        A AlarmManager for receiving intents at the time of your choosing.
        NOTIFICATION_SERVICE ("notification") A NotificationManager for
        informing the user of background events. KEYGUARD_SERVICE ("keyguard")
        A KeyguardManager for controlling keyguard. LOCATION_SERVICE
        ("location") A LocationManager for controlling location (e.g., GPS)
        updates. SEARCH_SERVICE ("search") A SearchManager for handling
        search. VIBRATOR_SERVICE ("vibrator") A Vibrator for interacting with
        the vibrator hardware. CONNECTIVITY_SERVICE ("connection") A
        ConnectivityManager for handling management of network connections.
        IPSEC_SERVICE ("ipsec") A IpSecManager for managing IPSec on sockets
        and networks. WIFI_SERVICE ("wifi") A WifiManager for management of
        Wi-Fi connectivity.  On releases before NYC, it should only be
        obtained from an application context, and not from any other derived
        context to avoid memory leaks within the calling process.
        WIFI_AWARE_SERVICE ("wifiaware") A WifiAwareManager for management of
        Wi-Fi Aware discovery and connectivity. WIFI_P2P_SERVICE ("wifip2p") A
        WifiP2pManager for management of Wi-Fi Direct connectivity.
        INPUT_METHOD_SERVICE ("input_method") An InputMethodManager for
        management of input methods. UI_MODE_SERVICE ("uimode") An
        UiModeManager for controlling UI modes. DOWNLOAD_SERVICE ("download")
        A DownloadManager for requesting HTTP downloads BATTERY_SERVICE
        ("batterymanager") A BatteryManager for managing battery state
        JOB_SCHEDULER_SERVICE ("taskmanager") A JobScheduler for managing
        scheduled tasks NETWORK_STATS_SERVICE ("netstats") A
        NetworkStatsManager for querying network usage statistics.
        HARDWARE_PROPERTIES_SERVICE ("hardware_properties") A
        HardwarePropertiesManager for accessing hardware properties. Note:
        System services obtained via this API may be closely associated with
        the Context in which they are obtained from.  In general, do not share
        the service objects between various different contexts (Activities,
        Applications, Services, Providers, etc.)  Note: Instant apps, for
        which PackageManager.isInstantApp() returns true, don't have access to
        the following system services: DEVICE_POLICY_SERVICE,
        FINGERPRINT_SERVICE, SHORTCUT_SERVICE, USB_SERVICE, WALLPAPER_SERVICE,
        WIFI_P2P_SERVICE, WIFI_SERVICE, WIFI_AWARE_SERVICE. For these services
        this method will return null. Generally, if you are running as an
        instant app you should always check whether the result of this method
        is null.
        :param name: String: The name of the desired service.Value is
        POWER_SERVICE, WINDOW_SERVICE, LAYOUT_INFLATER_SERVICE,
        ACCOUNT_SERVICE, ACTIVITY_SERVICE, ALARM_SERVICE,
        NOTIFICATION_SERVICE, ACCESSIBILITY_SERVICE, CAPTIONING_SERVICE,
        KEYGUARD_SERVICE, LOCATION_SERVICE, SEARCH_SERVICE, SENSOR_SERVICE,
        STORAGE_SERVICE, STORAGE_STATS_SERVICE, WALLPAPER_SERVICE,
        VIBRATOR_SERVICE, CONNECTIVITY_SERVICE, IPSEC_SERVICE,
        NETWORK_STATS_SERVICE, WIFI_SERVICE, WIFI_AWARE_SERVICE,
        WIFI_P2P_SERVICE, WIFI_RTT_RANGING_SERVICE, NSD_SERVICE,
        AUDIO_SERVICE, FINGERPRINT_SERVICE, MEDIA_ROUTER_SERVICE,
        TELEPHONY_SERVICE, TELEPHONY_SUBSCRIPTION_SERVICE,
        CARRIER_CONFIG_SERVICE, TELECOM_SERVICE, CLIPBOARD_SERVICE,
        INPUT_METHOD_SERVICE, TEXT_SERVICES_MANAGER_SERVICE,
        TEXT_CLASSIFICATION_SERVICE, APPWIDGET_SERVICE, DROPBOX_SERVICE,
        DEVICE_POLICY_SERVICE, UI_MODE_SERVICE, DOWNLOAD_SERVICE, NFC_SERVICE,
        BLUETOOTH_SERVICE, USB_SERVICE, LAUNCHER_APPS_SERVICE, INPUT_SERVICE,
        DISPLAY_SERVICE, USER_SERVICE, RESTRICTIONS_SERVICE, APP_OPS_SERVICE,
        CAMERA_SERVICE, PRINT_SERVICE, CONSUMER_IR_SERVICE, TV_INPUT_SERVICE,
        USAGE_STATS_SERVICE, MEDIA_SESSION_SERVICE, BATTERY_SERVICE,
        JOB_SCHEDULER_SERVICE, MEDIA_PROJECTION_SERVICE, MIDI_SERVICE,
        HARDWARE_PROPERTIES_SERVICE, SHORTCUT_SERVICE, SYSTEM_HEALTH_SERVICE,
        COMPANION_DEVICE_SERVICE or CROSS_PROFILE_APPS_SERVICE.This value must
        never be null.
        :return: Object. The service or null if the name does not exist.
        See also:

        WINDOW_SERVICEWindowManagerLAYOUT_INFLATER_SERVICELayoutInflaterACTIVITY_SERVICEActivityManagerPOWER_SERVICEPowerManagerALARM_SERVICEAlarmManagerNOTIFICATION_SERVICENotificationManagerKEYGUARD_SERVICEKeyguardManagerLOCATION_SERVICELocationManagerSEARCH_SERVICESearchManagerSENSOR_SERVICESensorManagerSTORAGE_SERVICEStorageManagerVIBRATOR_SERVICEVibratorCONNECTIVITY_SERVICEConnectivityManagerWIFI_SERVICEWifiManagerAUDIO_SERVICEAudioManagerMEDIA_ROUTER_SERVICEMediaRouterTELEPHONY_SERVICETelephonyManagerTELEPHONY_SUBSCRIPTION_SERVICESubscriptionManagerCARRIER_CONFIG_SERVICECarrierConfigManagerINPUT_METHOD_SERVICEInputMethodManagerUI_MODE_SERVICEUiModeManagerDOWNLOAD_SERVICEDownloadManagerBATTERY_SERVICEBatteryManagerJOB_SCHEDULER_SERVICEJobSchedulerNETWORK_STATS_SERVICENetworkStatsManagerHardwarePropertiesManagerHARDWARE_PROPERTIES_SERVICE
        """
        pass

    def getSystemServiceName(self, serviceClass):
        """
        Gets the name of the system-level service that is represented by the
        specified class.
        :param serviceClass: Class: The class of the desired service.This
        value must never be null.
        :return: String. The service name or null if the class is not a
        supported system service.
        """
        pass

    def getText(self, resId):
        """
        Return a localized, styled CharSequence from the application's
        package's default string table.
        :param resId: int: Resource id for the CharSequence text
        :return: CharSequence. This value will never be null.
        """
        pass

    def getTheme(self):
        """
        Return the Theme object associated with this Context.
        :return: Resources.Theme.
        """
        pass

    def getWallpaper(self):
        """
        This method was deprecated in API level 5. Use WallpaperManager.get()
        instead.
        :return: Drawable.
        """
        pass

    def getWallpaperDesiredMinimumHeight(self):
        """
        This method was deprecated in API level 5. Use
        WallpaperManager.getDesiredMinimumHeight() instead.
        :return: int.
        """
        pass

    def getWallpaperDesiredMinimumWidth(self):
        """
        This method was deprecated in API level 5. Use
        WallpaperManager.getDesiredMinimumWidth() instead.
        :return: int.
        """
        pass

    def grantUriPermission(self, toPackage, uri, modeFlags):
        """
        Grant permission to access a specific Uri to another package,
        regardless of whether that package has general permission to access
        the Uri's content provider.  This can be used to grant specific,
        temporary permissions, typically in response to user interaction (such
        as the user opening an attachment that you would like someone else to
        display).  Normally you should use
        Intent.FLAG_GRANT_READ_URI_PERMISSION or
        Intent.FLAG_GRANT_WRITE_URI_PERMISSION with the Intent being used to
        start an activity instead of this function directly.  If you use this
        function directly, you should be sure to call revokeUriPermission(Uri,
        int) when the target should no longer be allowed to access it.  To
        succeed, the content provider owning the Uri must have set the
        grantUriPermissions attribute in its manifest or included the
        <grant-uri-permissions> tag.
        :param toPackage: String: The package you would like to allow to
        access the Uri.
        :param uri: Uri: The Uri you would like to grant access to.
        :param modeFlags: int: The desired access modes.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION,
        FLAG_GRANT_WRITE_URI_PERMISSION, FLAG_GRANT_PERSISTABLE_URI_PERMISSION
        or FLAG_GRANT_PREFIX_URI_PERMISSION.
        See also: revokeUriPermission(Uri, int)
        """
        pass

    def isDeviceProtectedStorage(self):
        """
        Indicates if the storage APIs of this Context are backed by
        device-protected storage.
        :return: boolean.
        See also: createDeviceProtectedStorageContext()
        """
        pass

    def isRestricted(self):
        """
        Indicates whether this Context is restricted.
        :return: boolean. true if this Context is restricted, false otherwise.
        See also: CONTEXT_RESTRICTED
        """
        pass

    def moveDatabaseFrom(self, sourceContext, name):
        """
        Move an existing database file from the given source storage context
        to this context. This is typically used to migrate data between
        storage locations after an upgrade, such as migrating to device
        protected storage.  The database must be closed before being moved.
        :param sourceContext: Context: The source context which contains the
        existing database to move.
        :param name: String: The name of the database file.
        :return: boolean. true if the move was successful or if the database
        didn't exist in the source context, otherwise false.
        See also: createDeviceProtectedStorageContext()
        """
        pass

    def moveSharedPreferencesFrom(self, sourceContext, name):
        """
        Move an existing shared preferences file from the given source storage
        context to this context. This is typically used to migrate data
        between storage locations after an upgrade, such as moving to device
        protected storage.
        :param sourceContext: Context: The source context which contains the
        existing shared preferences to move.
        :param name: String: The name of the shared preferences file.
        :return: boolean. true if the move was successful or if the shared
        preferences didn't exist in the source context, otherwise false.
        See also: createDeviceProtectedStorageContext()
        """
        pass

    @overload('AttributeSet', 'int')
    def obtainStyledAttributes(self, set, attrs):
        """
        Retrieve styled attribute information in this Context's theme.  See
        Resources.Theme.obtainStyledAttributes(AttributeSet, int[], int, int)
        for more information.
        :param set: AttributeSet
        :param attrs: int
        :return: TypedArray.
        See also: Resources.Theme.obtainStyledAttributes(AttributeSet, int[],
        int, int)
        """
        pass

    @obtainStyledAttributes.adddef('AttributeSet', 'int[]', 'int', 'int')
    def obtainStyledAttributes(self, set, attrs, defStyleAttr, defStyleRes):
        """
        Retrieve styled attribute information in this Context's theme.  See
        Resources.Theme.obtainStyledAttributes(AttributeSet, int[], int, int)
        for more information.
        :param set: AttributeSet
        :param attrs: int
        :param defStyleAttr: int
        :param defStyleRes: int
        :return: TypedArray.
        See also: Resources.Theme.obtainStyledAttributes(AttributeSet, int[],
        int, int)
        """
        pass

    @obtainStyledAttributes.adddef('int', 'int[]')
    def obtainStyledAttributes(self, resid, attrs):
        """
        Retrieve styled attribute information in this Context's theme.  See
        Resources.Theme.obtainStyledAttributes(int, int[]) for more
        information.
        :param resid: int
        :param attrs: int
        :return: TypedArray.
        :raises: Resources.NotFoundException
        See also: Resources.Theme.obtainStyledAttributes(int, int[])
        """
        pass

    @obtainStyledAttributes.adddef('int[]')
    def obtainStyledAttributes(self, attrs):
        """
        Retrieve styled attribute information in this Context's theme.  See
        Resources.Theme.obtainStyledAttributes(int[]) for more information.
        :param attrs: int
        :return: TypedArray.
        See also: Resources.Theme.obtainStyledAttributes(int[])
        """
        pass

    def openFileInput(self, name):
        """
        Open a private file associated with this Context's application package
        for reading.
        :param name: String: The name of the file to open; can not contain
        path separators.
        :return: FileInputStream. The resulting FileInputStream.
        :raises: FileNotFoundException
        See also: openFileOutput(String,
        int)fileList()deleteFile(String)FileInputStream.FileInputStream(String)
        """
        pass

    def openFileOutput(self, name, mode):
        """
        Open a private file associated with this Context's application package
        for writing. Creates the file if it doesn't already exist.  No
        additional permissions are required for the calling app to read or
        write the returned file.
        :param name: String: The name of the file to open; can not contain
        path separators.
        :param mode: int: Operating mode.Value is either 0 or combination of
        MODE_PRIVATE, MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE or MODE_APPEND.
        :return: FileOutputStream. The resulting FileOutputStream.
        :raises: FileNotFoundException
        See also:

        MODE_APPENDMODE_PRIVATEopenFileInput(String)fileList()deleteFile(String)FileOutputStream.FileOutputStream(String)
        """
        pass

    @overload('str', 'int', 'SQLiteDatabase.CursorFactory', 'DatabaseErrorHandler')
    def openOrCreateDatabase(self, name, mode, factory, errorHandler):
        """
        Open a new private SQLiteDatabase associated with this Context's
        application package. Creates the database file if it doesn't exist.
        Accepts input param: a concrete instance of DatabaseErrorHandler to be
        used to handle corruption when sqlite reports database corruption.
        :param name: String: The name (unique in the application package) of
        the database.
        :param mode: int: Operating mode.Value is either 0 or combination of
        MODE_PRIVATE, MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE,
        MODE_ENABLE_WRITE_AHEAD_LOGGING or MODE_NO_LOCALIZED_COLLATORS.
        :param factory: SQLiteDatabase.CursorFactory: An optional factory
        class that is called to instantiate a cursor when query is called.
        :param errorHandler: DatabaseErrorHandler: the DatabaseErrorHandler to
        be used when sqlite reports database corruption. if null,
        DefaultDatabaseErrorHandler is assumed.
        :return: SQLiteDatabase. The contents of a newly created database with
        the given name.
        :raises SQLiteException: if the database file could not be opened.
        See also:
        MODE_PRIVATE
        MODE_ENABLE_WRITE_AHEAD_LOGGING
        MODE_NO_LOCALIZED_COLLATORS
        deleteDatabase(String)
        """
        pass

    @openOrCreateDatabase.adddef('str', 'int', 'SQLiteDatabase.CursorFactory')
    def openOrCreateDatabase(self, name, mode, factory):
        """
        Open a new private SQLiteDatabase associated with this Context's
        application package. Create the database file if it doesn't exist.
        :param name: String: The name (unique in the application package) of
        the database.
        :param mode: int: Operating mode.Value is either 0 or combination of
        MODE_PRIVATE, MODE_WORLD_READABLE, MODE_WORLD_WRITEABLE,
        MODE_ENABLE_WRITE_AHEAD_LOGGING or MODE_NO_LOCALIZED_COLLATORS.
        :param factory: SQLiteDatabase.CursorFactory: An optional factory
        class that is called to instantiate a cursor when query is called.
        :return: SQLiteDatabase. The contents of a newly created database with
        the given name.
        :raises: SQLiteExceptionif the database file could not be opened.
        See also:

        MODE_PRIVATEMODE_ENABLE_WRITE_AHEAD_LOGGINGMODE_NO_LOCALIZED_COLLATORSdeleteDatabase(String)
        """
        pass

    def peekWallpaper(self):
        """
        This method was deprecated in API level 5. Use WallpaperManager.peek()
        instead.
        :return: Drawable.
        """
        pass

    def registerComponentCallbacks(self, callback):
        """
        Add a new ComponentCallbacks to the base application of the Context,
        which will be called at the same times as the ComponentCallbacks
        methods of activities and other components are called.  Note that you
        must be sure to use unregisterComponentCallbacks(ComponentCallbacks)
        when appropriate in the future; this will not be removed for you.
        :param callback: ComponentCallbacks: The interface to call.  This can
        be either a ComponentCallbacks or ComponentCallbacks2 interface.
        """
        pass

    @overload('BroadcastReceiver', 'IntentFilter')
    def registerReceiver(self, receiver, filter):
        """
        Register a BroadcastReceiver to be run in the main activity thread.
        The receiver will be called with any broadcast Intent that matches
        filter, in the main application thread.  The system may broadcast
        Intents that are "sticky" -- these stay around after the broadcast has
        finished, to be sent to any later registrations. If your IntentFilter
        matches one of these sticky Intents, that Intent will be returned by
        this function and sent to your receiver as if it had just been
        broadcast.  There may be multiple sticky Intents that match filter, in
        which case each of these will be sent to receiver.  In this case, only
        one of these can be returned directly by the function; which of these
        that is returned is arbitrarily decided by the system.  If you know
        the Intent your are registering for is sticky, you can supply null for
        your receiver.  In this case, no receiver is registered -- the
        function simply returns the sticky Intent that matches filter.  In the
        case of multiple matches, the same rules as described above apply.
        See BroadcastReceiver for more information on Intent broadcasts.  As
        of Build.VERSION_CODES.ICE_CREAM_SANDWICH, receivers registered with
        this method will correctly respect the Intent.setPackage(String)
        specified for an Intent being broadcast. Prior to that, it would be
        ignored and delivered to all matching registered receivers.  Be
        careful if using this for security.Note: this method cannot be called
        from a BroadcastReceiver component; that is, from a BroadcastReceiver
        that is declared in an application's manifest.  It is okay, however,
        to call this method from another BroadcastReceiver that has itself
        been registered at run time with registerReceiver(BroadcastReceiver,
        IntentFilter), since the lifetime of such a registered
        BroadcastReceiver is tied to the object that registered it.
        :param receiver: BroadcastReceiver: The BroadcastReceiver to handle
        the broadcast.This value may be null.
        :param filter: IntentFilter: Selects the Intent broadcasts to be
        received.
        :return: Intent. The first sticky intent found that matches filter, or
        null if there are none.
        See also: registerReceiver(BroadcastReceiver, IntentFilter, String,
        Handler)sendBroadcast(Intent)unregisterReceiver(BroadcastReceiver)
        """
        pass

    @registerReceiver.adddef('BroadcastReceiver', 'IntentFilter', 'int')
    def registerReceiver(self, receiver, filter, flags):
        """
        Register to receive intent broadcasts, with the receiver optionally
        being exposed to Instant Apps. See registerReceiver(BroadcastReceiver,
        IntentFilter) for more information. By default Instant Apps cannot
        interact with receivers in other applications, this allows you to
        expose a receiver that Instant Apps can interact with.  See
        BroadcastReceiver for more information on Intent broadcasts.  As of
        Build.VERSION_CODES.ICE_CREAM_SANDWICH, receivers registered with this
        method will correctly respect the Intent.setPackage(String) specified
        for an Intent being broadcast. Prior to that, it would be ignored and
        delivered to all matching registered receivers.  Be careful if using
        this for security.
        :param receiver: BroadcastReceiver: The BroadcastReceiver to handle
        the broadcast.This value may be null.
        :param filter: IntentFilter: Selects the Intent broadcasts to be
        received.
        :param flags: int: Additional options for the receiver. May be 0 or
        RECEIVER_VISIBLE_TO_INSTANT_APPS.Value is either 0 or
        RECEIVER_VISIBLE_TO_INSTANT_APPS.
        :return: Intent. The first sticky intent found that matches filter, or
        null if there are none.
        See also: registerReceiver(BroadcastReceiver,
        IntentFilter)sendBroadcast(Intent)unregisterReceiver(BroadcastReceiver)
        """
        pass

    @registerReceiver.adddef('BroadcastReceiver', 'IntentFilter', 'str', 'Handler', 'int')
    def registerReceiver(self, receiver, filter, broadcastPermission, scheduler, flags):
        """
        Register to receive intent broadcasts, to run in the context of
        scheduler. See registerReceiver(BroadcastReceiver, IntentFilter, int)
        and registerReceiver(BroadcastReceiver, IntentFilter, String, Handler)
        for more information.  See BroadcastReceiver for more information on
        Intent broadcasts.  As of Build.VERSION_CODES.ICE_CREAM_SANDWICH,
        receivers registered with this method will correctly respect the
        Intent.setPackage(String) specified for an Intent being broadcast.
        Prior to that, it would be ignored and delivered to all matching
        registered receivers.  Be careful if using this for security.
        :param receiver: BroadcastReceiver: The BroadcastReceiver to handle
        the broadcast.
        :param filter: IntentFilter: Selects the Intent broadcasts to be
        received.
        :param broadcastPermission: String: String naming a permissions that a
        broadcaster must hold in order to send an Intent to you.  If null, no
        permission is required.
        :param scheduler: Handler: Handler identifying the thread that will
        receive the Intent.  If null, the main thread of the process will be
        used.
        :param flags: int: Additional options for the receiver. May be 0 or
        RECEIVER_VISIBLE_TO_INSTANT_APPS.Value is either 0 or
        RECEIVER_VISIBLE_TO_INSTANT_APPS.
        :return: Intent. The first sticky intent found that matches filter, or
        null if there are none.
        See also: registerReceiver(BroadcastReceiver, IntentFilter,
        int)registerReceiver(BroadcastReceiver, IntentFilter, String,
        Handler)sendBroadcast(Intent)unregisterReceiver(BroadcastReceiver)
        """
        pass

    @registerReceiver.adddef('BroadcastReceiver', 'IntentFilter', 'str', 'Handler')
    def registerReceiver(self, receiver, filter, broadcastPermission, scheduler):
        """
        Register to receive intent broadcasts, to run in the context of
        scheduler.  See registerReceiver(BroadcastReceiver, IntentFilter) for
        more information.  This allows you to enforce permissions on who can
        broadcast intents to your receiver, or have the receiver run in a
        different thread than the main application thread.  See
        BroadcastReceiver for more information on Intent broadcasts.  As of
        Build.VERSION_CODES.ICE_CREAM_SANDWICH, receivers registered with this
        method will correctly respect the Intent.setPackage(String) specified
        for an Intent being broadcast. Prior to that, it would be ignored and
        delivered to all matching registered receivers.  Be careful if using
        this for security.
        :param receiver: BroadcastReceiver: The BroadcastReceiver to handle
        the broadcast.
        :param filter: IntentFilter: Selects the Intent broadcasts to be
        received.
        :param broadcastPermission: String: String naming a permissions that a
        broadcaster must hold in order to send an Intent to you.  If null, no
        permission is required.
        :param scheduler: Handler: Handler identifying the thread that will
        receive the Intent.  If null, the main thread of the process will be
        used.
        :return: Intent. The first sticky intent found that matches filter, or
        null if there are none.
        See also: registerReceiver(BroadcastReceiver,
        IntentFilter)sendBroadcast(Intent)unregisterReceiver(BroadcastReceiver)
        """
        pass

    def removeStickyBroadcast(self, intent):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Remove the data previously sent with
        sendStickyBroadcast(Intent), so that it is as if the sticky broadcast
        had never happened.Requires the BROADCAST_STICKY permission.
        :param intent: Intent: The Intent that was previously broadcast.
        See also: sendStickyBroadcast(Intent)
        """
        pass

    def removeStickyBroadcastAsUser(self, intent, user):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Version of
        removeStickyBroadcast(Intent) that allows you to specify the user the
        broadcast will be sent to.  This is not available to applications that
        are not pre-installed on the system image.  You must hold the
        Manifest.permission.BROADCAST_STICKY permission in order to use this
        API.  If you do not hold that permission, SecurityException will be
        thrown.Requires the BROADCAST_STICKY permission.
        :param intent: Intent: The Intent that was previously broadcast.
        :param user: UserHandle: UserHandle to remove the sticky broadcast
        from.
        See also: sendStickyBroadcastAsUser(Intent, UserHandle)
        """
        pass

    @overload('Uri', 'int')
    def revokeUriPermission(self, uri, modeFlags):
        """
        Remove all permissions to access a particular content provider Uri
        that were previously added with grantUriPermission(String, Uri, int)
        or any other mechanism. The given Uri will match all previously
        granted Uris that are the same or a sub-path of the given Uri.  That
        is, revoking "content://foo/target" will revoke both
        "content://foo/target" and "content://foo/target/sub", but not
        "content://foo".  It will not remove any prefix grants that exist at a
        higher level.  Prior to Build.VERSION_CODES.LOLLIPOP, if you did not
        have regular permission access to a Uri, but had received access to it
        through a specific Uri permission grant, you could not revoke that
        grant with this function and a SecurityException would be thrown.  As
        of Build.VERSION_CODES.LOLLIPOP, this function will not throw a
        security exception, but will remove whatever permission grants to the
        Uri had been given to the app (or none).Unlike
        revokeUriPermission(String, Uri, int), this method impacts all
        permission grants matching the given Uri, for any package they had
        been granted to, through any mechanism this had happened (such as
        indirectly through the clipboard, activity launch, service start,
        etc).  That means this can be potentially dangerous to use, as it can
        revoke grants that another app could be strongly expecting to stick
        around.
        :param uri: Uri: The Uri you would like to revoke access to.
        :param modeFlags: int: The access modes to revoke.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        See also: grantUriPermission(String, Uri, int)
        """
        pass

    @revokeUriPermission.adddef('str', 'Uri', 'int')
    def revokeUriPermission(self, toPackage, uri, modeFlags):
        """
        Remove permissions to access a particular content provider Uri that
        were previously added with grantUriPermission(String, Uri, int) for a
        specific target package.  The given Uri will match all previously
        granted Uris that are the same or a sub-path of the given Uri.  That
        is, revoking "content://foo/target" will revoke both
        "content://foo/target" and "content://foo/target/sub", but not
        "content://foo".  It will not remove any prefix grants that exist at a
        higher level.  Unlike revokeUriPermission(Uri, int), this method will
        only revoke permissions that had been explicitly granted through
        grantUriPermission(String, Uri, int) and only for the package
        specified.  Any matching grants that have happened through other
        mechanisms (clipboard, activity launching, service starting, etc) will
        not be removed.
        :param toPackage: String: The package you had previously granted
        access to.
        :param uri: Uri: The Uri you would like to revoke access to.
        :param modeFlags: int: The access modes to revoke.Value is either 0 or
        combination of FLAG_GRANT_READ_URI_PERMISSION or
        FLAG_GRANT_WRITE_URI_PERMISSION.
        See also: grantUriPermission(String, Uri, int)
        """
        pass

    @overload('Intent', 'str')
    def sendBroadcast(self, intent, receiverPermission):
        """
        Broadcast the given intent to all interested BroadcastReceivers,
        allowing an optional required permission to be enforced.  This call is
        asynchronous; it returns immediately, and you will continue executing
        while the receivers are run.  No results are propagated from receivers
        and receivers can not abort the broadcast. If you want to allow
        receivers to propagate results or abort the broadcast, you must send
        an ordered broadcast using sendOrderedBroadcast(Intent, String).  See
        BroadcastReceiver for more information on Intent broadcasts.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param receiverPermission: String: (optional) String naming a
        permission that a receiver must hold in order to receive your
        broadcast. If null, no permission is required.
        See also: BroadcastReceiverregisterReceiver(BroadcastReceiver,
        IntentFilter)sendBroadcast(Intent)sendOrderedBroadcast(Intent,
        String)sendOrderedBroadcast(Intent, String, BroadcastReceiver,
        Handler, int, String, Bundle)
        """
        pass

    @sendBroadcast.adddef('Intent')
    def sendBroadcast(self, intent):
        """
        Broadcast the given intent to all interested BroadcastReceivers.  This
        call is asynchronous; it returns immediately, and you will continue
        executing while the receivers are run.  No results are propagated from
        receivers and receivers can not abort the broadcast. If you want to
        allow receivers to propagate results or abort the broadcast, you must
        send an ordered broadcast using sendOrderedBroadcast(Intent, String).
        See BroadcastReceiver for more information on Intent broadcasts.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        See also: BroadcastReceiverregisterReceiver(BroadcastReceiver,
        IntentFilter)sendBroadcast(Intent, String)sendOrderedBroadcast(Intent,
        String)sendOrderedBroadcast(Intent, String, BroadcastReceiver,
        Handler, int, String, Bundle)
        """
        pass

    @overload('Intent', 'UserHandle')
    def sendBroadcastAsUser(self, intent, user):
        """
        Version of sendBroadcast(Intent) that allows you to specify the user
        the broadcast will be sent to.  This is not available to applications
        that are not pre-installed on the system image.Requires the
        permission.
        :param intent: Intent: The intent to broadcast
        :param user: UserHandle: UserHandle to send the intent to.
        See also: sendBroadcast(Intent)
        """
        pass

    @sendBroadcastAsUser.adddef('Intent', 'UserHandle', 'str')
    def sendBroadcastAsUser(self, intent, user, receiverPermission):
        """
        Version of sendBroadcast(Intent, String) that allows you to specify
        the user the broadcast will be sent to.  This is not available to
        applications that are not pre-installed on the system image.Requires
        the  permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param user: UserHandle: UserHandle to send the intent to.
        :param receiverPermission: String: (optional) String naming a
        permission that a receiver must hold in order to receive your
        broadcast. If null, no permission is required.
        See also: sendBroadcast(Intent, String)
        """
        pass

    @overload('Intent', 'str', 'BroadcastReceiver', 'Handler', 'int', 'str', 'Bundle')
    def sendOrderedBroadcast(self, intent, receiverPermission, resultReceiver,
                             scheduler, initialCode, initialData, initialExtras):
        """
        Version of sendBroadcast(Intent) that allows you to receive data back
        from the broadcast.  This is accomplished by supplying your own
        BroadcastReceiver when calling, which will be treated as a final
        receiver at the end of the broadcast -- its
        BroadcastReceiver.onReceive(Context, Intent) method will be called
        with the result values collected from the other receivers.  The
        broadcast will be serialized in the same way as calling
        sendOrderedBroadcast(Intent, String).  Like sendBroadcast(Intent),
        this method is asynchronous; it will return before
        resultReceiver.onReceive() is called.  See BroadcastReceiver for more
        information on Intent broadcasts.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.This value must never be null.
        :param receiverPermission: String: String naming a permissions that a
        receiver must hold in order to receive your broadcast. If null, no
        permission is required.
        :param resultReceiver: BroadcastReceiver: Your own BroadcastReceiver
        to treat as the final receiver of the broadcast.This value may be null.
        :param scheduler: Handler: A custom Handler with which to schedule the
        resultReceiver callback; if null it will be scheduled in the Context's
        main thread.
        :param initialCode: int: An initial value for the result code.  Often
        Activity.RESULT_OK.
        :param initialData: String: An initial value for the result data.
        Often null.
        :param initialExtras: Bundle: An initial value for the result extras.
        Often null.
        See also: sendBroadcast(Intent)sendBroadcast(Intent,
        String)sendOrderedBroadcast(Intent,
        String)BroadcastReceiverregisterReceiver(BroadcastReceiver,
        IntentFilter)Activity.RESULT_OK
        """
        pass

    @sendOrderedBroadcast.adddef('Intent', 'str')
    def sendOrderedBroadcast(self, intent, receiverPermission):
        """
        Broadcast the given intent to all interested BroadcastReceivers,
        delivering them one at a time to allow more preferred receivers to
        consume the broadcast before it is delivered to less preferred
        receivers.  This call is asynchronous; it returns immediately, and you
        will continue executing while the receivers are run.  See
        BroadcastReceiver for more information on Intent broadcasts.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param receiverPermission: String: (optional) String naming a
        permissions that a receiver must hold in order to receive your
        broadcast. If null, no permission is required.
        See also: BroadcastReceiverregisterReceiver(BroadcastReceiver,
        IntentFilter)sendBroadcast(Intent)sendOrderedBroadcast(Intent, String,
        BroadcastReceiver, Handler, int, String, Bundle)
        """
        pass

    def sendOrderedBroadcastAsUser(self, intent, user, receiverPermission, resultReceiver, scheduler, initialCode,
                                   initialData, initialExtras):
        """
        Version of sendOrderedBroadcast(Intent, String, BroadcastReceiver,
        Handler, int, String, Bundle) that allows you to specify the user the
        broadcast will be sent to.  This is not available to applications that
        are not pre-installed on the system image.  See BroadcastReceiver for
        more information on Intent broadcasts.Requires the  permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param user: UserHandle: UserHandle to send the intent to.
        :param receiverPermission: String: String naming a permissions that a
        receiver must hold in order to receive your broadcast. If null, no
        permission is required.
        :param resultReceiver: BroadcastReceiver: Your own BroadcastReceiver
        to treat as the final receiver of the broadcast.
        :param scheduler: Handler: A custom Handler with which to schedule the
        resultReceiver callback; if null it will be scheduled in the Context's
        main thread.
        :param initialCode: int: An initial value for the result code.  Often
        Activity.RESULT_OK.
        :param initialData: String: An initial value for the result data.
        Often null.
        :param initialExtras: Bundle: An initial value for the result extras.
        Often null.
        See also: sendOrderedBroadcast(Intent, String, BroadcastReceiver,
        Handler, int, String, Bundle)
        """
        pass

    def sendStickyBroadcast(self, intent):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Perform a sendBroadcast(Intent) that
        is "sticky," meaning the Intent you are sending stays around after the
        broadcast is complete, so that others can quickly retrieve that data
        through the return value of registerReceiver(BroadcastReceiver,
        IntentFilter).  In all other ways, this behaves the same as
        sendBroadcast(Intent).Requires the BROADCAST_STICKY permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast, and the Intent will be held to
        be re-broadcast to future receivers.
        See also: sendBroadcast(Intent)sendStickyOrderedBroadcast(Intent,
        BroadcastReceiver, Handler, int, String, Bundle)
        """
        pass

    def sendStickyBroadcastAsUser(self, intent, user):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Version of sendStickyBroadcast(Intent)
        that allows you to specify the user the broadcast will be sent to.
        This is not available to applications that are not pre-installed on
        the system image.Requires the BROADCAST_STICKY permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast, and the Intent will be held to
        be re-broadcast to future receivers.
        :param user: UserHandle: UserHandle to send the intent to.
        See also: sendBroadcast(Intent)
        """
        pass

    def sendStickyOrderedBroadcast(self, intent, resultReceiver, scheduler, initialCode, initialData, initialExtras):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Version of sendStickyBroadcast(Intent)
        that allows you to receive data back from the broadcast.  This is
        accomplished by supplying your own BroadcastReceiver when calling,
        which will be treated as a final receiver at the end of the broadcast
        -- its BroadcastReceiver.onReceive(Context, Intent) method will be
        called with the result values collected from the other receivers.  The
        broadcast will be serialized in the same way as calling
        sendOrderedBroadcast(Intent, String).  Like sendBroadcast(Intent),
        this method is asynchronous; it will return before
        resultReceiver.onReceive() is called.  Note that the sticky data
        stored is only the data you initially supply to the broadcast, not the
        result of any changes made by the receivers.  See BroadcastReceiver
        for more information on Intent broadcasts.Requires the
        BROADCAST_STICKY permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param resultReceiver: BroadcastReceiver: Your own BroadcastReceiver
        to treat as the final receiver of the broadcast.
        :param scheduler: Handler: A custom Handler with which to schedule the
        resultReceiver callback; if null it will be scheduled in the Context's
        main thread.
        :param initialCode: int: An initial value for the result code.  Often
        Activity.RESULT_OK.
        :param initialData: String: An initial value for the result data.
        Often null.
        :param initialExtras: Bundle: An initial value for the result extras.
        Often null.
        See also: sendBroadcast(Intent)sendBroadcast(Intent,
        String)sendOrderedBroadcast(Intent,

        String)sendStickyBroadcast(Intent)BroadcastReceiverregisterReceiver(BroadcastReceiver, IntentFilter)Activity.RESULT_OK
        """
        pass

    def sendStickyOrderedBroadcastAsUser(self, intent, user, resultReceiver, scheduler, initialCode, initialData,
                                         initialExtras):
        """
        This method was deprecated in API level 21. Sticky broadcasts should
        not be used.  They provide no security (anyone can access them), no
        protection (anyone can modify them), and many other problems. The
        recommended pattern is to use a non-sticky broadcast to report that
        something has changed, with another mechanism for apps to retrieve the
        current value whenever desired. Version of
        sendStickyOrderedBroadcast(Intent, BroadcastReceiver, Handler, int,
        String, Bundle) that allows you to specify the user the broadcast will
        be sent to.  This is not available to applications that are not
        pre-installed on the system image.  See BroadcastReceiver for more
        information on Intent broadcasts.Requires the BROADCAST_STICKY
        permission.
        :param intent: Intent: The Intent to broadcast; all receivers matching
        this Intent will receive the broadcast.
        :param user: UserHandle: UserHandle to send the intent to.
        :param resultReceiver: BroadcastReceiver: Your own BroadcastReceiver
        to treat as the final receiver of the broadcast.
        :param scheduler: Handler: A custom Handler with which to schedule the
        resultReceiver callback; if null it will be scheduled in the Context's
        main thread.
        :param initialCode: int: An initial value for the result code.  Often
        Activity.RESULT_OK.
        :param initialData: String: An initial value for the result data.
        Often null.
        :param initialExtras: Bundle: An initial value for the result extras.
        Often null.
        See also: sendStickyOrderedBroadcast(Intent, BroadcastReceiver,
        Handler, int, String, Bundle)
        """
        pass

    def setTheme(self, resid):
        """
        Set the base theme for this context.  Note that this should be called
        before any views are instantiated in the Context (for example before
        calling Activity.setContentView(View) or LayoutInflater.inflate(int,
        ViewGroup)).
        :param resid: int: The style resource describing the theme.
        """
        pass

    @overload('Bitmap')
    def setWallpaper(self, bitmap):
        """
        This method was deprecated in API level 5. Use WallpaperManager.set()
        instead. This method requires the caller to hold the permission
        Manifest.permission.SET_WALLPAPER.
        :param bitmap: Bitmap
        :raises: IOException
        """
        pass

    @setWallpaper.adddef('InputStream')
    def setWallpaper(self, data):
        """
        This method was deprecated in API level 5. Use WallpaperManager.set()
        instead. This method requires the caller to hold the permission
        Manifest.permission.SET_WALLPAPER.
        :param data: InputStream
        :raises: IOException
        """
        pass

    @overload('Intent[]', 'Bundle')
    def startActivities(self, intents, options):
        """
        Launch multiple new activities.  This is generally the same as calling
        startActivity(Intent) for the first Intent in the array, that activity
        during its creation calling startActivity(Intent) for the second
        entry, etc.  Note that unlike that approach, generally none of the
        activities except the last in the array will be created at this point,
        but rather will be created when the user first visits them (due to
        pressing back from the activity on top).  This method throws
        ActivityNotFoundException if there was no Activity found for any given
        Intent.  In this case the state of the activity stack is undefined
        (some Intents in the list may be on it, some not), so you probably
        want to avoid such situations.
        :param intents: Intent: An array of Intents to be started.
        :param options: Bundle: Additional options for how the Activity should
        be started. See startActivity(Intent, Bundle)
        Context.startActivity(Intent, Bundle)} for more details.
        :raises: ActivityNotFoundException&nbsp;
        See also:
        startActivities(Intent[])PackageManager.resolveActivity(Intent, int)
        """
        pass

    @startActivities.adddef('Intent[]')
    def startActivities(self, intents):
        """
        Same as startActivities(Intent[], Bundle) with no options specified.
        :param intents: Intent: An array of Intents to be started.
        :raises: ActivityNotFoundException&nbsp;
        See also: startActivities(Intent[],
        Bundle)PackageManager.resolveActivity(Intent, int)
        """
        pass

    @overload('Intent')
    def startActivity(self, intent):
        """
        Same as startActivity(Intent, Bundle) with no options specified.
        :param intent: Intent: The description of the activity to start.
        :raises: ActivityNotFoundException&nbsp; `
        See also: startActivity(Intent,
        Bundle)PackageManager.resolveActivity(Intent, int)
        """
        pass

    @startActivity.adddef('Intent', 'Bundle')
    def startActivity(self, intent, options):
        """
        Launch a new activity.  You will not receive any information about
        when the activity exits.  Note that if this method is being called
        from outside of an Activity Context, then the Intent must include the
        Intent.FLAG_ACTIVITY_NEW_TASK launch flag.  This is because, without
        being started from an existing Activity, there is no existing task in
        which to place the new activity and thus it needs to be placed in its
        own separate task.  This method throws ActivityNotFoundException if
        there was no Activity found to run the given Intent.
        :param intent: Intent: The description of the activity to start.
        :param options: Bundle: Additional options for how the Activity should
        be started. May be null if there are no options.  See ActivityOptions
        for how to build the Bundle supplied here; there are no supported
        definitions for building it manually.
        :raises: ActivityNotFoundException&nbsp;
        See also: startActivity(Intent)PackageManager.resolveActivity(Intent,
        int)
        """
        pass

    def startForegroundService(self, service):
        """
        Similar to startService(Intent), but with an implicit promise that the
        Service will call startForeground(int, android.app.Notification) once
        it begins running.  The service is given an amount of time comparable
        to the ANR interval to do this, otherwise the system will
        automatically stop the service and declare the app ANR.  Unlike the
        ordinary startService(Intent), this method can be used at any time,
        regardless of whether the app hosting the service is in a foreground
        state.
        :param service: Intent: Identifies the service to be started.  The
        Intent must be fully explicit (supplying a component name).
        Additional values may be included in the Intent extras to supply
        arguments along with this specific start call.
        :return: ComponentName. If the service is being started or is already
        running, the ComponentName of the actual service that was started is
        returned; else if the service does not exist null is returned.
        :raises: SecurityExceptionIf the caller does not have permission to
        access the service or the service can not be found.
        See also: stopService(Intent)Service.startForeground(int,
        android.app.Notification)
        """
        pass

    def startInstrumentation(self, className, profileFile, arguments):
        """
        Start executing an Instrumentation class.  The given Instrumentation
        component will be run by killing its target application (if currently
        running), starting the target process, instantiating the
        instrumentation component, and then letting it drive the application.
        This function is not synchronous -- it returns as soon as the
        instrumentation has started and while it is running.  Instrumentation
        is normally only allowed to run against a package that is either
        unsigned or signed with a signature that the the instrumentation
        package is also signed with (ensuring the target trusts the
        instrumentation).
        :param className: ComponentName: Name of the Instrumentation component
        to be run.This value must never be null.
        :param profileFile: String: Optional path to write profiling data as
        the instrumentation runs, or null for no profiling.
        :param arguments: Bundle: Additional optional arguments to pass to the
        instrumentation, or null.
        :return: boolean. true if the instrumentation was successfully
        started, else false if it could not be found.
        """
        pass

    @overload('IntentSender', 'Intent', 'int', 'int', 'int')
    def startIntentSender(self, intent, fillInIntent, flagsMask, flagsValues, extraFlags):
        """
        Same as startIntentSender(IntentSender, Intent, int, int, int, Bundle)
        with no options specified.
        :param intent: IntentSender: The IntentSender to launch.
        :param fillInIntent: Intent: If non-null, this will be provided as the
        intent parameter to IntentSender.sendIntent(Context, int, Intent,
        IntentSender.OnFinished, Handler).
        :param flagsMask: int: Intent flags in the original IntentSender that
        you would like to change.Value is either 0 or combination of
        FLAG_FROM_BACKGROUND, FLAG_DEBUG_LOG_RESOLUTION,
        FLAG_EXCLUDE_STOPPED_PACKAGES, FLAG_INCLUDE_STOPPED_PACKAGES,
        FLAG_ACTIVITY_MATCH_EXTERNAL, FLAG_RECEIVER_REGISTERED_ONLY,
        FLAG_RECEIVER_REPLACE_PENDING, FLAG_RECEIVER_FOREGROUND,
        FLAG_RECEIVER_NO_ABORT, FLAG_ACTIVITY_CLEAR_TOP,
        FLAG_ACTIVITY_FORWARD_RESULT, FLAG_ACTIVITY_PREVIOUS_IS_TOP,
        FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS, FLAG_ACTIVITY_BROUGHT_TO_FRONT,
        FLAG_RECEIVER_VISIBLE_TO_INSTANT_APPS,
        FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY, FLAG_ACTIVITY_NEW_DOCUMENT,
        FLAG_ACTIVITY_NO_USER_ACTION, FLAG_ACTIVITY_REORDER_TO_FRONT,
        FLAG_ACTIVITY_NO_ANIMATION, FLAG_ACTIVITY_CLEAR_TASK,
        FLAG_ACTIVITY_TASK_ON_HOME, FLAG_ACTIVITY_RETAIN_IN_RECENTS or
        FLAG_ACTIVITY_LAUNCH_ADJACENT.
        :param flagsValues: int: Desired values for any bits set in
        flagsMaskValue is either 0 or combination of FLAG_FROM_BACKGROUND,
        FLAG_DEBUG_LOG_RESOLUTION, FLAG_EXCLUDE_STOPPED_PACKAGES,
        FLAG_INCLUDE_STOPPED_PACKAGES, FLAG_ACTIVITY_MATCH_EXTERNAL,
        FLAG_RECEIVER_REGISTERED_ONLY, FLAG_RECEIVER_REPLACE_PENDING,
        FLAG_RECEIVER_FOREGROUND, FLAG_RECEIVER_NO_ABORT,
        FLAG_ACTIVITY_CLEAR_TOP, FLAG_ACTIVITY_FORWARD_RESULT,
        FLAG_ACTIVITY_PREVIOUS_IS_TOP, FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS,
        FLAG_ACTIVITY_BROUGHT_TO_FRONT, FLAG_RECEIVER_VISIBLE_TO_INSTANT_APPS,
        FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY, FLAG_ACTIVITY_NEW_DOCUMENT,
        FLAG_ACTIVITY_NO_USER_ACTION, FLAG_ACTIVITY_REORDER_TO_FRONT,
        FLAG_ACTIVITY_NO_ANIMATION, FLAG_ACTIVITY_CLEAR_TASK,
        FLAG_ACTIVITY_TASK_ON_HOME, FLAG_ACTIVITY_RETAIN_IN_RECENTS or
        FLAG_ACTIVITY_LAUNCH_ADJACENT.
        :param extraFlags: int: Always set to 0.
        :raises: IntentSender.SendIntentException
        See also: startActivity(Intent)startIntentSender(IntentSender, Intent,
        int, int, int, Bundle)
        """
        pass

    @startIntentSender.adddef('IntentSender', 'Intent', 'int', 'int', 'int', 'Bundle')
    def startIntentSender(self, intent, fillInIntent, flagsMask, flagsValues, extraFlags, options):
        """
        Like startActivity(Intent, Bundle), but taking a IntentSender to
        start.  If the IntentSender is for an activity, that activity will be
        started as if you had called the regular startActivity(Intent) here;
        otherwise, its associated action will be executed (such as sending a
        broadcast) as if you had called IntentSender.sendIntent on it.
        :param intent: IntentSender: The IntentSender to launch.
        :param fillInIntent: Intent: If non-null, this will be provided as the
        intent parameter to IntentSender.sendIntent(Context, int, Intent,
        IntentSender.OnFinished, Handler).
        :param flagsMask: int: Intent flags in the original IntentSender that
        you would like to change.Value is either 0 or combination of
        FLAG_FROM_BACKGROUND, FLAG_DEBUG_LOG_RESOLUTION,
        FLAG_EXCLUDE_STOPPED_PACKAGES, FLAG_INCLUDE_STOPPED_PACKAGES,
        FLAG_ACTIVITY_MATCH_EXTERNAL, FLAG_RECEIVER_REGISTERED_ONLY,
        FLAG_RECEIVER_REPLACE_PENDING, FLAG_RECEIVER_FOREGROUND,
        FLAG_RECEIVER_NO_ABORT, FLAG_ACTIVITY_CLEAR_TOP,
        FLAG_ACTIVITY_FORWARD_RESULT, FLAG_ACTIVITY_PREVIOUS_IS_TOP,
        FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS, FLAG_ACTIVITY_BROUGHT_TO_FRONT,
        FLAG_RECEIVER_VISIBLE_TO_INSTANT_APPS,
        FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY, FLAG_ACTIVITY_NEW_DOCUMENT,
        FLAG_ACTIVITY_NO_USER_ACTION, FLAG_ACTIVITY_REORDER_TO_FRONT,
        FLAG_ACTIVITY_NO_ANIMATION, FLAG_ACTIVITY_CLEAR_TASK,
        FLAG_ACTIVITY_TASK_ON_HOME, FLAG_ACTIVITY_RETAIN_IN_RECENTS or
        FLAG_ACTIVITY_LAUNCH_ADJACENT.
        :param flagsValues: int: Desired values for any bits set in
        flagsMaskValue is either 0 or combination of FLAG_FROM_BACKGROUND,
        FLAG_DEBUG_LOG_RESOLUTION, FLAG_EXCLUDE_STOPPED_PACKAGES,
        FLAG_INCLUDE_STOPPED_PACKAGES, FLAG_ACTIVITY_MATCH_EXTERNAL,
        FLAG_RECEIVER_REGISTERED_ONLY, FLAG_RECEIVER_REPLACE_PENDING,
        FLAG_RECEIVER_FOREGROUND, FLAG_RECEIVER_NO_ABORT,
        FLAG_ACTIVITY_CLEAR_TOP, FLAG_ACTIVITY_FORWARD_RESULT,
        FLAG_ACTIVITY_PREVIOUS_IS_TOP, FLAG_ACTIVITY_EXCLUDE_FROM_RECENTS,
        FLAG_ACTIVITY_BROUGHT_TO_FRONT, FLAG_RECEIVER_VISIBLE_TO_INSTANT_APPS,
        FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY, FLAG_ACTIVITY_NEW_DOCUMENT,
        FLAG_ACTIVITY_NO_USER_ACTION, FLAG_ACTIVITY_REORDER_TO_FRONT,
        FLAG_ACTIVITY_NO_ANIMATION, FLAG_ACTIVITY_CLEAR_TASK,
        FLAG_ACTIVITY_TASK_ON_HOME, FLAG_ACTIVITY_RETAIN_IN_RECENTS or
        FLAG_ACTIVITY_LAUNCH_ADJACENT.
        :param extraFlags: int: Always set to 0.
        :param options: Bundle: Additional options for how the Activity should
        be started. See startActivity(Intent, Bundle)
        Context.startActivity(Intent, Bundle)} for more details.  If options
        have also been supplied by the IntentSender, options given here will
        override any that conflict with those given by the IntentSender.This
        value may be null.
        :raises: IntentSender.SendIntentException
        See also: startActivity(Intent, Bundle)startIntentSender(IntentSender,
        Intent, int, int, int)
        """
        pass

    def startService(self, service):
        """
        Request that a given application service be started.  The Intent
        should either contain the complete class name of a specific service
        implementation to start, or a specific package name to target.  If the
        Intent is less specified, it logs a warning about this.  In this case
        any of the multiple matching services may be used.  If this service is
        not already running, it will be instantiated and started (creating a
        process for it if needed); if it is running then it remains running.
        Every call to this method will result in a corresponding call to the
        target service's Service.onStartCommand(Intent, int, int) method, with
        the intent given here.  This provides a convenient way to submit jobs
        to a service without having to bind and call on to its interface.
        Using startService() overrides the default service lifetime that is
        managed by bindService(Intent, ServiceConnection, int): it requires
        the service to remain running until stopService(Intent) is called,
        regardless of whether any clients are connected to it.  Note that
        calls to startService() do not nest: no matter how many times you call
        startService(), a single call to stopService(Intent) will stop it.
        The system attempts to keep running services around as much as
        possible.  The only time they should be stopped is if the current
        foreground application is using so many resources that the service
        needs to be killed.  If any errors happen in the service's process, it
        will automatically be restarted.  This function will throw
        SecurityException if you do not have permission to start the given
        service.  Note: Each call to startService() results in significant
        work done by the system to manage service lifecycle surrounding the
        processing of the intent, which can take multiple milliseconds of CPU
        time. Due to this cost, startService() should not be used for frequent
        intent delivery to a service, and only for scheduling significant
        work. Use bound services for high frequency calls.
        :param service: Intent: Identifies the service to be started.  The
        Intent must be fully explicit (supplying a component name).
        Additional values may be included in the Intent extras to supply
        arguments along with this specific start call.
        :return: ComponentName. If the service is being started or is already
        running, the ComponentName of the actual service that was started is
        returned; else if the service does not exist null is returned.
        :raises: SecurityExceptionIf the caller does not have permission to
        access the service or the service can not be
        found.IllegalStateExceptionIf the application is in a state where the
        service can not be started (such as not in the foreground in a state
        when services are allowed).
        See also: stopService(Intent)bindService(Intent, ServiceConnection,
        int)
        """
        pass

    def stopService(self, service):
        """
        Request that a given application service be stopped.  If the service
        is not running, nothing happens.  Otherwise it is stopped.  Note that
        calls to startService() are not counted -- this stops the service no
        matter how many times it was started.  Note that if a stopped service
        still has ServiceConnection objects bound to it with the
        BIND_AUTO_CREATE set, it will not be destroyed until all of these
        bindings are removed.  See the Service documentation for more details
        on a service's lifecycle.  This function will throw SecurityException
        if you do not have permission to stop the given service.
        :param service: Intent: Description of the service to be stopped.  The
        Intent must be either fully explicit (supplying a component name) or
        specify a specific package name it is targeted to.
        :return: boolean. If there is a service matching the given Intent that
        is already running, then it is stopped and true is returned; else
        false is returned.
        :raises: SecurityExceptionIf the caller does not have permission to
        access the service or the service can not be
        found.IllegalStateExceptionIf the application is in a state where the
        service can not be started (such as not in the foreground in a state
        when services are allowed).
        See also: startService(Intent)
        """
        pass

    def unbindService(self, conn):
        """
        Disconnect from an application service.  You will no longer receive
        calls as the service is restarted, and the service is now allowed to
        stop at any time.
        :param conn: ServiceConnection: The connection interface previously
        supplied to bindService().  This parameter must not be null.
        See also: bindService(Intent, ServiceConnection, int)
        """
        pass

    def unregisterComponentCallbacks(self, callback):
        """
        Remove a ComponentCallbacks object that was previously registered with
        registerComponentCallbacks(ComponentCallbacks).
        :param callback: ComponentCallbacks
        """
        pass

    def unregisterReceiver(self, receiver):
        """
        Unregister a previously registered BroadcastReceiver.  All filters
        that have been registered for this BroadcastReceiver will be removed.
        :param receiver: BroadcastReceiver: The BroadcastReceiver to
        unregister.
        See also: registerReceiver(BroadcastReceiver, IntentFilter)
        """
        pass
