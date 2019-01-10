# -*- coding: utf-8 -*-
"""https://developer.android.com/reference/android/content/pm/PackageManager"""
import abc

from Android import overload

"""
public static final int CERT_INPUT_RAW_X509:
Certificate input bytes: the input bytes represent an encoded X.509 
Certificate which could
be generated using an CertificateFactory
"""
CERT_INPUT_RAW_X509 = 0x00000000

"""
public static final int CERT_INPUT_SHA256:
Certificate input bytes: the input bytes represent the SHA256 output of an 
encoded X.509
Certificate.
"""
CERT_INPUT_SHA256 = 0x00000001

"""
public static final int COMPONENT_ENABLED_STATE_DEFAULT:
Flag for setApplicationEnabledSetting(String, int, int) and
setComponentEnabledSetting(ComponentName, int, int): This
component or application is in its default enabled state (as specified in
its manifest).

Explicitly setting the component state to this value restores it's
enabled state to whatever is set in the manifest.
"""
COMPONENT_ENABLED_STATE_DEFAULT = 0x00000000

"""
public static final int COMPONENT_ENABLED_STATE_DISABLED:
Flag for setApplicationEnabledSetting(String, int, int)
and setComponentEnabledSetting(ComponentName, int, int): This
component or application has been explicitly disabled, regardless of
what it has specified in its manifest.
"""
COMPONENT_ENABLED_STATE_DISABLED = 0x00000002

"""
public static final int COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED:
Flag for setApplicationEnabledSetting(String, int, int) only: This
application should be considered, until the point where the user actually
wants to use it.  This means that it will not normally show up to the user
(such as in the launcher), but various parts of the user interface can
use GET_DISABLED_UNTIL_USED_COMPONENTS to still see it and allow
the user to select it (as for example an IME, device admin, etc).  Such code,
once the user has selected the app, should at that point also make it enabled.
This option currently can not be used with
setComponentEnabledSetting(ComponentName, int, int).
"""
COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED = 0x00000004

"""
public static final int COMPONENT_ENABLED_STATE_DISABLED_USER:
Flag for setApplicationEnabledSetting(String, int, int) only: The
user has explicitly disabled the application, regardless of what it has
specified in its manifest.  Because this is due to the user's request,
they may re-enable it if desired through the appropriate system UI.  This
option currently cannot be used with
setComponentEnabledSetting(ComponentName, int, int).
"""
COMPONENT_ENABLED_STATE_DISABLED_USER = 0x00000003

"""
public static final int COMPONENT_ENABLED_STATE_ENABLED:
Flag for setApplicationEnabledSetting(String, int, int)
and setComponentEnabledSetting(ComponentName, int, int): This
component or application has been explictily enabled, regardless of
what it has specified in its manifest.
"""
COMPONENT_ENABLED_STATE_ENABLED = 0x00000001

"""
public static final int DONT_KILL_APP:
Flag parameter for
setComponentEnabledSetting(android.content.ComponentName, int, int) to indicate
that you don't want to kill the app containing the component.  Be careful when 
you set this
since changing component states can make the containing application's behavior 
unpredictable.
"""
DONT_KILL_APP = 0x00000001

"""
public static final String EXTRA_VERIFICATION_ID:
Extra field name for the ID of a package pending verification. Passed to
a package verifier and is used to call back to
"""
EXTRA_VERIFICATION_ID = 'android.content.pm.extra.VERIFICATION_ID'

"""
public static final String EXTRA_VERIFICATION_RESULT:
Extra field name for the result of a verification, either
VERIFICATION_ALLOW, or VERIFICATION_REJECT.
Passed to package verifiers after a package is verified.
"""
EXTRA_VERIFICATION_RESULT = 'android.content.pm.extra.VERIFICATION_RESULT'

"""
public static final String FEATURE_ACTIVITIES_ON_SECONDARY_DISPLAYS:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports running activities on secondary displays.
"""
FEATURE_ACTIVITIES_ON_SECONDARY_DISPLAYS = 'android.software.activities_on_secondary_displays'

"""
public static final String FEATURE_APP_WIDGETS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports app widgets.
"""
FEATURE_APP_WIDGETS = 'android.software.app_widgets'

"""
public static final String FEATURE_AUDIO_LOW_LATENCY:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): The 
device's
audio pipeline is low-latency, more suitable for audio applications sensitive 
to delays or
lag in sound input or output.
"""
FEATURE_AUDIO_LOW_LATENCY = 'android.hardware.audio.low_latency'

"""
public static final String FEATURE_AUDIO_OUTPUT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes at least one form of audio
output, as defined in the Android Compatibility Definition Document (CDD)
section 7.8 Audio.
"""
FEATURE_AUDIO_OUTPUT = 'android.hardware.audio.output'

"""
public static final String FEATURE_AUDIO_PRO:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device has professional audio level of functionality and performance.
"""
FEATURE_AUDIO_PRO = 'android.hardware.audio.pro'

"""
public static final String FEATURE_AUTOFILL:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports autofill of user credentials, addresses, credit cards, etc
via integration with autofill
providers.
"""
FEATURE_AUTOFILL = 'android.software.autofill'

"""
public static final String FEATURE_AUTOMOTIVE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This is a device dedicated to showing UI
on a vehicle headunit. A headunit here is defined to be inside a
vehicle that may or may not be moving. A headunit uses either a
primary display in the center console and/or additional displays in
the instrument cluster or elsewhere in the vehicle. Headunit display(s)
have limited size and resolution. The user will likely be focused on
driving so limiting driver distraction is a primary concern. User input
can be a variety of hard buttons, touch, rotary controllers and even mouse-
like interfaces.
"""
FEATURE_AUTOMOTIVE = 'android.hardware.type.automotive'

"""
public static final String FEATURE_BACKUP:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device can perform backup and restore operations on installed applications.
"""
FEATURE_BACKUP = 'android.software.backup'

"""
public static final String FEATURE_BLUETOOTH:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device is capable of communicating with
other devices via Bluetooth.
"""
FEATURE_BLUETOOTH = 'android.hardware.bluetooth'

"""
public static final String FEATURE_BLUETOOTH_LE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device is capable of communicating with
other devices via Bluetooth Low Energy radio.
"""
FEATURE_BLUETOOTH_LE = 'android.hardware.bluetooth_le'

"""
public static final String FEATURE_CAMERA:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a camera facing away
from the screen.
"""
FEATURE_CAMERA = 'android.hardware.camera'

"""
public static final String FEATURE_CAMERA_ANY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has at least one camera pointing in
some direction, or can support an external camera being connected to it.
"""
FEATURE_CAMERA_ANY = 'android.hardware.camera.any'

"""
public static final String FEATURE_CAMERA_AR:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): At 
least one
of the cameras on the device supports the
MOTION_TRACKING capability level.
"""
FEATURE_CAMERA_AR = 'android.hardware.camera.ar'

"""
public static final String FEATURE_CAMERA_AUTOFOCUS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's camera supports auto-focus.
"""
FEATURE_CAMERA_AUTOFOCUS = 'android.hardware.camera.autofocus'

"""
public static final String FEATURE_CAMERA_CAPABILITY_MANUAL_POST_PROCESSING:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): At 
least one
of the cameras on the device supports the
manual post-processing
capability level.
"""
FEATURE_CAMERA_CAPABILITY_MANUAL_POST_PROCESSING = 'android.hardware.camera.capability.manual_post_processing'

"""
public static final String FEATURE_CAMERA_CAPABILITY_MANUAL_SENSOR:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): At 
least one
of the cameras on the device supports the
manual sensor
capability level.
"""
FEATURE_CAMERA_CAPABILITY_MANUAL_SENSOR = 'android.hardware.camera.capability.manual_sensor'

"""
public static final String FEATURE_CAMERA_CAPABILITY_RAW:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): At 
least one
of the cameras on the device supports the
RAW
capability level.
"""
FEATURE_CAMERA_CAPABILITY_RAW = 'android.hardware.camera.capability.raw'

"""
public static final String FEATURE_CAMERA_EXTERNAL:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device can support having an external camera 
connected to it.
The external camera may not always be connected or available to applications 
to use.
"""
FEATURE_CAMERA_EXTERNAL = 'android.hardware.camera.external'

"""
public static final String FEATURE_CAMERA_FLASH:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's camera supports flash.
"""
FEATURE_CAMERA_FLASH = 'android.hardware.camera.flash'

"""
public static final String FEATURE_CAMERA_FRONT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a front facing camera.
"""
FEATURE_CAMERA_FRONT = 'android.hardware.camera.front'

"""
public static final String FEATURE_CAMERA_LEVEL_FULL:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): At 
least one
of the cameras on the device supports the
full hardware
capability level.
"""
FEATURE_CAMERA_LEVEL_FULL = 'android.hardware.camera.level.full'

"""
public static final String FEATURE_COMPANION_DEVICE_SETUP:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports associating
with devices via CompanionDeviceManager.
"""
FEATURE_COMPANION_DEVICE_SETUP = 'android.software.companion_device_setup'

"""
public static final String FEATURE_CONNECTION_SERVICE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The Connection Service API is enabled on the device.
"""
FEATURE_CONNECTION_SERVICE = 'android.software.connectionservice'

"""
public static final String FEATURE_CONSUMER_IR:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device is capable of communicating with
consumer IR devices.
"""
FEATURE_CONSUMER_IR = 'android.hardware.consumerir'

"""
public static final String FEATURE_DEVICE_ADMIN:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports device policy enforcement via 
device admins.
"""
FEATURE_DEVICE_ADMIN = 'android.software.device_admin'

"""
public static final String FEATURE_EMBEDDED:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This is a device for IoT and may not have an UI. An 
embedded
device is defined as a full stack Android device with or without a display and 
no
user-installable apps.
"""
FEATURE_EMBEDDED = 'android.hardware.type.embedded'

"""
public static final String FEATURE_ETHERNET:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This device supports ethernet.
"""
FEATURE_ETHERNET = 'android.hardware.ethernet'

"""
public static final String FEATURE_FAKETOUCH:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device does not have a touch screen, but
does support touch emulation for basic events. For instance, the
device might use a mouse or remote control to drive a cursor, and
emulate basic touch pointer events like down, up, drag, etc. All
devices that support android.hardware.touchscreen or a sub-feature are
presumed to also support faketouch.
"""
FEATURE_FAKETOUCH = 'android.hardware.faketouch'

"""
public static final String FEATURE_FAKETOUCH_MULTITOUCH_DISTINCT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device does not have a touch screen, but
does support touch emulation for basic events that supports distinct
tracking of two or more fingers.  This is an extension of
FEATURE_FAKETOUCH for input devices with this capability.  Note
that unlike a distinct multitouch screen as defined by
FEATURE_TOUCHSCREEN_MULTITOUCH_DISTINCT, these kinds of input
devices will not actually provide full two-finger gestures since the
input is being transformed to cursor movement on the screen.  That is,
single finger gestures will move a cursor; two-finger swipes will
result in single-finger touch events; other two-finger gestures will
result in the corresponding two-finger touch event.
"""
FEATURE_FAKETOUCH_MULTITOUCH_DISTINCT = 'android.hardware.faketouch.multitouch.distinct'

"""
public static final String FEATURE_FAKETOUCH_MULTITOUCH_JAZZHAND:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device does not have a touch screen, but
does support touch emulation for basic events that supports tracking
a hand of fingers (5 or more fingers) fully independently.
This is an extension of
FEATURE_FAKETOUCH for input devices with this capability.  Note
that unlike a multitouch screen as defined by
FEATURE_TOUCHSCREEN_MULTITOUCH_JAZZHAND, not all two finger
gestures can be detected due to the limitations described for
FEATURE_FAKETOUCH_MULTITOUCH_DISTINCT.
"""
FEATURE_FAKETOUCH_MULTITOUCH_JAZZHAND = 'android.hardware.faketouch.multitouch.jazzhand'

"""
public static final String FEATURE_FINGERPRINT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has biometric hardware to detect a 
fingerprint.
"""
FEATURE_FINGERPRINT = 'android.hardware.fingerprint'

"""
public static final String FEATURE_FREEFORM_WINDOW_MANAGEMENT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports freeform window management.
Windows have title bars and can be moved and resized.
"""
FEATURE_FREEFORM_WINDOW_MANAGEMENT = 'android.software.freeform_window_management'

"""
public static final String FEATURE_GAMEPAD:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device has all of the inputs necessary to be considered a compatible game 
controller, or
includes a compatible game controller in the box.
"""
FEATURE_GAMEPAD = 'android.hardware.gamepad'

"""
public static final String FEATURE_HIFI_SENSORS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports high fidelity sensor processing
capabilities.
"""
FEATURE_HIFI_SENSORS = 'android.hardware.sensor.hifi_sensors'

"""
public static final String FEATURE_HOME_SCREEN:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports a home screen that is replaceable
by third party applications.
"""
FEATURE_HOME_SCREEN = 'android.software.home_screen'

"""
public static final String FEATURE_INPUT_METHODS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports adding new input methods 
implemented
with the InputMethodService API.
"""
FEATURE_INPUT_METHODS = 'android.software.input_methods'

"""
public static final String FEATURE_LEANBACK:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports leanback UI. This is
typically used in a living room television experience, but is a software
feature unlike FEATURE_TELEVISION. Devices running with this
feature will use resources associated with the "television" UI mode.
"""
FEATURE_LEANBACK = 'android.software.leanback'

"""
public static final String FEATURE_LEANBACK_ONLY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports only leanback UI. Only
applications designed for this experience should be run, though this is
not enforced by the system.
"""
FEATURE_LEANBACK_ONLY = 'android.software.leanback_only'

"""
public static final String FEATURE_LIVE_TV:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports live TV and can display
contents from TV inputs implemented with the
TvInputService API.
"""
FEATURE_LIVE_TV = 'android.software.live_tv'

"""
public static final String FEATURE_LIVE_WALLPAPER:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports live wallpapers.
"""
FEATURE_LIVE_WALLPAPER = 'android.software.live_wallpaper'

"""
public static final String FEATURE_LOCATION:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports one or more methods of
reporting current location.
"""
FEATURE_LOCATION = 'android.hardware.location'

"""
public static final String FEATURE_LOCATION_GPS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a Global Positioning System
receiver and can report precise location.
"""
FEATURE_LOCATION_GPS = 'android.hardware.location.gps'

"""
public static final String FEATURE_LOCATION_NETWORK:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device can report location with coarse
accuracy using a network-based geolocation system.
"""
FEATURE_LOCATION_NETWORK = 'android.hardware.location.network'

"""
public static final String FEATURE_MANAGED_USERS:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports creating secondary users and managed profiles via
DevicePolicyManager.
"""
FEATURE_MANAGED_USERS = 'android.software.managed_users'

"""
public static final String FEATURE_MICROPHONE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device can record audio via a
microphone.
"""
FEATURE_MICROPHONE = 'android.hardware.microphone'

"""
public static final String FEATURE_MIDI:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device has a full implementation of the android.media.midi.* APIs.
"""
FEATURE_MIDI = 'android.software.midi'

"""
public static final String FEATURE_NFC:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device can communicate using Near-Field
Communications (NFC).
"""
FEATURE_NFC = 'ndroid.hardware.nfc'

"""
public static final String FEATURE_NFC_HOST_CARD_EMULATION:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports host-
based NFC card emulation.
"""
FEATURE_NFC_HOST_CARD_EMULATION = 'android.hardware.nfc.hce'

"""
public static final String FEATURE_NFC_HOST_CARD_EMULATION_NFCF:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports host-
based NFC-F card emulation.
"""
FEATURE_NFC_HOST_CARD_EMULATION_NFCF = 'android.hardware.nfc.hcef'

"""
public static final String FEATURE_OPENGLES_EXTENSION_PACK:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports the OpenGL ES

Android Extension Pack.
"""
FEATURE_OPENGLES_EXTENSION_PACK = 'android.hardware.opengles.aep'

"""
public static final String FEATURE_PC:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This is a device dedicated to be primarily used
with keyboard, mouse or touchpad. This includes traditional desktop
computers, laptops and variants such as convertibles or detachables.
Due to the larger screen, the device will most likely use the
FEATURE_FREEFORM_WINDOW_MANAGEMENT feature as well.
"""
FEATURE_PC = 'android.hardware.type.pc'

"""
public static final String FEATURE_PICTURE_IN_PICTURE:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports picture-in-picture multi-window mode.
"""
FEATURE_PICTURE_IN_PICTURE = 'android.software.picture_in_picture'

"""
public static final String FEATURE_PRINTING:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports printing.
"""
FEATURE_PRINTING = 'android.software.print'

"""
public static final String FEATURE_RAM_LOW:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's
ActivityManager.isLowRamDevice() method returns
true.
"""
FEATURE_RAM_LOW = 'android.hardware.ram.low'

"""
public static final String FEATURE_RAM_NORMAL:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's
ActivityManager.isLowRamDevice() method returns
false.
"""
FEATURE_RAM_NORMAL = 'android.hardware.ram.normal'

"""
public static final String FEATURE_SCREEN_LANDSCAPE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports landscape orientation
screens.  For backwards compatibility, you can assume that if neither
this nor FEATURE_SCREEN_PORTRAIT is set then the device supports
both portrait and landscape.
"""
FEATURE_SCREEN_LANDSCAPE = 'android.hardware.screen.landscape'

"""
public static final String FEATURE_SCREEN_PORTRAIT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports portrait orientation
screens.  For backwards compatibility, you can assume that if neither
this nor FEATURE_SCREEN_LANDSCAPE is set then the device supports
both portrait and landscape.
"""
FEATURE_SCREEN_PORTRAIT = 'android.hardware.screen.portrait'

"""
public static final String FEATURE_SECURELY_REMOVES_USERS:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports secure removal of users. When a user is deleted the data 
associated
with that user is securely deleted and no longer available.
"""
FEATURE_SECURELY_REMOVES_USERS = 'android.software.securely_removes_users'

"""
public static final String FEATURE_SENSOR_ACCELEROMETER:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes an accelerometer.
"""
FEATURE_SENSOR_ACCELEROMETER = 'android.hardware.sensor.accelerometer'

"""
public static final String FEATURE_SENSOR_AMBIENT_TEMPERATURE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes an ambient temperature sensor.
"""
FEATURE_SENSOR_AMBIENT_TEMPERATURE = 'android.hardware.sensor.ambient_temperature'

"""
public static final String FEATURE_SENSOR_BAROMETER:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a barometer (air
pressure sensor.)
"""
FEATURE_SENSOR_BAROMETER = 'android.hardware.sensor.barometer'

"""
public static final String FEATURE_SENSOR_COMPASS:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a magnetometer (compass).
"""
FEATURE_SENSOR_COMPASS = 'android.hardware.sensor.compass'

"""
public static final String FEATURE_SENSOR_GYROSCOPE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a gyroscope.
"""
FEATURE_SENSOR_GYROSCOPE = 'android.hardware.sensor.gyroscope'

"""
public static final String FEATURE_SENSOR_HEART_RATE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a heart rate monitor.
"""
FEATURE_SENSOR_HEART_RATE = 'android.hardware.sensor.heartrate'

"""
public static final String FEATURE_SENSOR_HEART_RATE_ECG:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The heart rate sensor on this device is an 
Electrocardiogram.
"""
FEATURE_SENSOR_HEART_RATE_ECG = 'android.hardware.sensor.heartrate.ecg'

"""
public static final String FEATURE_SENSOR_LIGHT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a light sensor.
"""
FEATURE_SENSOR_LIGHT = 'android.hardware.sensor.light'

"""
public static final String FEATURE_SENSOR_PROXIMITY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a proximity sensor.
"""
FEATURE_SENSOR_PROXIMITY = 'android.hardware.sensor.proximity'

"""
public static final String FEATURE_SENSOR_RELATIVE_HUMIDITY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a relative humidity sensor.
"""
FEATURE_SENSOR_RELATIVE_HUMIDITY = 'android.hardware.sensor.relative_humidity'

"""
public static final String FEATURE_SENSOR_STEP_COUNTER:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a hardware step counter.
"""
FEATURE_SENSOR_STEP_COUNTER = 'android.hardware.sensor.stepcounter'

"""
public static final String FEATURE_SENSOR_STEP_DETECTOR:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device includes a hardware step detector.
"""
FEATURE_SENSOR_STEP_DETECTOR = 'android.hardware.sensor.stepdetector'

"""
public static final String FEATURE_SIP:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The SIP API is enabled on the device.
"""
FEATURE_SIP = 'android.software.sip'

"""
public static final String FEATURE_SIP_VOIP:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports SIP-based VOIP.
"""
FEATURE_SIP_VOIP = 'android.software.sip.voip'

"""
public static final String FEATURE_STRONGBOX_KEYSTORE:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device has a StrongBox hardware-backed Keystore.
"""
FEATURE_STRONGBOX_KEYSTORE = 'android.hardware.strongbox_keystore'

"""
public static final String FEATURE_TELEPHONY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a telephony radio with data
communication support.
"""
FEATURE_TELEPHONY = 'android.hardware.telephony'

"""
public static final String FEATURE_TELEPHONY_CDMA:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a CDMA telephony stack.
"""
FEATURE_TELEPHONY_CDMA = 'android.hardware.telephony.cdma'

"""
public static final String FEATURE_TELEPHONY_EUICC:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): The 
device
supports embedded subscriptions on eUICCs.
"""
FEATURE_TELEPHONY_EUICC = 'android.hardware.telephony.euicc'

"""
public static final String FEATURE_TELEPHONY_GSM:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device has a GSM telephony stack.
"""
FEATURE_TELEPHONY_GSM = 'android.hardware.telephony.gsm'

"""
public static final String FEATURE_TELEPHONY_MBMS:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String): The 
device
supports cell-broadcast reception using the MBMS APIs.
"""
FEATURE_TELEPHONY_MBMS = 'android.hardware.telephony.mbms'

"""
public static final String FEATURE_TELEVISION:

This constant was deprecated
in API level 21.
use FEATURE_LEANBACK instead.

Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This is a device dedicated to showing UI
on a television.  Television here is defined to be a typical living
room television experience: displayed on a big screen, where the user
is sitting far away from it, and the dominant form of input will be
"""
FEATURE_TELEVISION = 'android.hardware.type.television'

"""
public static final String FEATURE_TOUCHSCREEN:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's display has a touch screen.
"""
FEATURE_TOUCHSCREEN = 'android.hardware.touchscreen'

"""
public static final String FEATURE_TOUCHSCREEN_MULTITOUCH:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's touch screen supports
multitouch sufficient for basic two-finger gesture detection.
"""
FEATURE_TOUCHSCREEN_MULTITOUCH = 'android.hardware.touchscreen.multitouch'

"""
public static final String FEATURE_TOUCHSCREEN_MULTITOUCH_DISTINCT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's touch screen is capable of
tracking two or more fingers fully independently.
"""
FEATURE_TOUCHSCREEN_MULTITOUCH_DISTINCT = 'android.hardware.touchscreen.multitouch.distinct'

"""
public static final String FEATURE_TOUCHSCREEN_MULTITOUCH_JAZZHAND:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device's touch screen is capable of
tracking a full hand of fingers fully independently -- that is, 5 or
more simultaneous independent pointers.
"""
FEATURE_TOUCHSCREEN_MULTITOUCH_JAZZHAND = 'android.hardware.touchscreen.multitouch.jazzhand'

"""
public static final String FEATURE_USB_ACCESSORY:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports connecting to USB accessories.
"""
FEATURE_USB_ACCESSORY = 'android.hardware.usb.accessory'

"""
public static final String FEATURE_USB_HOST:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports connecting to USB devices
as the USB host.
"""
FEATURE_USB_HOST = 'android.hardware.usb.host'

"""
public static final String FEATURE_VERIFIED_BOOT:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device supports verified boot.
"""
FEATURE_VERIFIED_BOOT = 'android.software.verified_boot'

"""
public static final String FEATURE_VR_HEADTRACKING:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device implements headtracking suitable for a VR device.
"""
FEATURE_VR_HEADTRACKING = 'android.hardware.vr.headtracking'

"""
public static final String FEATURE_VR_MODE:

This constant was deprecated
in API level 28.
use FEATURE_VR_MODE:
_HIGH_PERFORMANCE instead.

Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device implements an optimized mode for virtual reality (VR) applications 
that handles
stereoscopic rendering of notifications, and disables most monocular system UI 
components
while a VR application has user focus.
Devices declaring this feature must include an application implementing a
VrListenerService that can be targeted by VR applications via
"""
FEATURE_VR_MODE = 'android.software.vr.mode'

"""
public static final String FEATURE_VR_MODE_HIGH_PERFORMANCE:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device implements an optimized mode for virtual reality (VR) applications 
that handles
stereoscopic rendering of notifications, disables most monocular system UI 
components
while a VR application has user focus and meets extra CDD requirements to 
provide a
high-quality VR experience.
Devices declaring this feature must include an application implementing a
VrListenerService that can be targeted by VR applications via
Activity.setVrModeEnabled(boolean, ComponentName).
and must meet CDD requirements to provide a high-quality VR experience.
"""
FEATURE_VR_MODE_HIGH_PERFORMANCE = 'android.hardware.vr.high_performance'

"""
public static final String FEATURE_VULKAN_HARDWARE_COMPUTE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String, int): If this feature is supported, the Vulkan native 
API
will enumerate at least one VkPhysicalDevice, and the feature version will 
indicate
what level of optional compute features that device supports beyond the Vulkan 
1.0
requirements.

Compute level 0 indicates:
The VK_KHR_variable_pointers extension and
VkPhysicalDeviceVariablePointerFeaturesKHR::variablePointers feature are
"""
FEATURE_VULKAN_HARDWARE_COMPUTE = 'android.hardware.vulkan.compute'

"""
public static final String FEATURE_VULKAN_HARDWARE_LEVEL:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String, int): If this feature is supported, the Vulkan native 
API
will enumerate at least one VkPhysicalDevice, and the feature version will 
indicate
what level of optional hardware features limits it supports.

Level 0 includes the base Vulkan requirements as well as:
VkPhysicalDeviceFeatures::textureCompressionETC2
Level 1 additionally includes:
"""
FEATURE_VULKAN_HARDWARE_LEVEL = 'android.hardware.vulkan.level'

"""
public static final String FEATURE_VULKAN_HARDWARE_VERSION:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String, int): The version of this feature indicates the 
highest
VkPhysicalDeviceProperties::apiVersion supported by the physical devices that 
support
the hardware level indicated by FEATURE_VULKAN_HARDWARE_LEVEL. The feature 
version
uses the same encoding as Vulkan version numbers:
Major version number in bits 31-22Minor version number in bits 21-12Patch 
version number in bits 11-0
A version of 1.1.0 or higher also indicates:
SYNC_FD external semaphore and fence handles are 

supported.VkPhysicalDeviceSamplerYcbcrConversionFeatures::samplerYcbcrConversion is
"""
FEATURE_VULKAN_HARDWARE_VERSION = 'android.hardware.vulkan.version'

"""
public static final String FEATURE_WATCH:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): This is a device dedicated to showing UI
on a watch. A watch here is defined to be a device worn on the body, perhaps on
the wrist. The user is very close when interacting with the device.
"""
FEATURE_WATCH = 'android.hardware.type.watch'

"""
public static final String FEATURE_WEBVIEW:
Feature for getSystemAvailableFeatures() and hasSystemFeature(String):
The device has a full implementation of the android.webkit.* APIs. Devices
lacking this feature will not have a functioning WebView implementation.
"""
FEATURE_WEBVIEW = 'android.software.webview'

"""
public static final String FEATURE_WIFI:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports WiFi (802.11) networking.
"""
FEATURE_WIFI = 'android.hardware.wifi'

"""
public static final String FEATURE_WIFI_AWARE:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports Wi-Fi Aware.
"""
FEATURE_WIFI_AWARE = 'android.hardware.wifi.aware'

"""
public static final String FEATURE_WIFI_DIRECT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports Wi-Fi Direct networking.
"""
FEATURE_WIFI_DIRECT = 'android.hardware.wifi.direct'

"""
public static final String FEATURE_WIFI_PASSPOINT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports Wi-Fi Passpoint and all
Passpoint related APIs in WifiManager are supported. Refer to
WifiManager.addOrUpdatePasspointConfiguration(PasspointConfiguration) for more 
info.
"""
FEATURE_WIFI_PASSPOINT = 'android.hardware.wifi.passpoint'

"""
public static final String FEATURE_WIFI_RTT:
Feature for getSystemAvailableFeatures() and
hasSystemFeature(String): The device supports Wi-Fi RTT (IEEE 802.11mc).
"""
FEATURE_WIFI_RTT = 'android.hardware.wifi.rtt'

"""
public static final int GET_ACTIVITIES:
PackageInfo flag: return information about
activities in the package in PackageInfo.activities.
"""
GET_ACTIVITIES = 0x00000001

"""
public static final int GET_CONFIGURATIONS:
PackageInfo flag: return information about
hardware preferences in
PackageInfo.configPreferences,
and requested features in PackageInfo.reqFeatures and
PackageInfo.featureGroups.
"""
GET_CONFIGURATIONS = 0x00004000

"""
public static final int GET_DISABLED_COMPONENTS:

This constant was deprecated
in API level 24.
replaced with MATCH_DISABLED_COMPONENTS
"""
GET_DISABLED_COMPONENTS = 0x00000200

"""
public static final int GET_DISABLED_UNTIL_USED_COMPONENTS:

This constant was deprecated
in API level 24.
replaced with MATCH_DISABLED_UNTIL_USED_COMPONENTS.
"""
GET_DISABLED_UNTIL_USED_COMPONENTS = 0x00008000

"""
public static final int GET_GIDS:
PackageInfo flag: return the
group ids that are associated with an
application.
This applies for any API returning a PackageInfo class, either
directly or nested inside of another.
"""
GET_GIDS = 0x00000100

"""
public static final int GET_INSTRUMENTATION:
PackageInfo flag: return information about
instrumentation in the package in
PackageInfo.instrumentation.
"""
GET_INSTRUMENTATION = 0x00000010

"""
public static final int GET_INTENT_FILTERS:
PackageInfo flag: return information about the
intent filters supported by the activity.
"""
GET_INTENT_FILTERS = 0x00000020

"""
public static final int GET_META_DATA:
ComponentInfo flag: return the PackageItemInfo.metaData
data Bundles that are associated with a component.
This applies for any API returning a ComponentInfo subclass.
"""
GET_META_DATA = 0x00000080

"""
public static final int GET_PERMISSIONS:
PackageInfo flag: return information about
permissions in the package in
PackageInfo.permissions.
"""
GET_PERMISSIONS = 0x00001000

"""
public static final int GET_PROVIDERS:
PackageInfo flag: return information about
content providers in the package in
PackageInfo.providers.
"""
GET_PROVIDERS = 0x00000008

"""
public static final int GET_RECEIVERS:
PackageInfo flag: return information about
intent receivers in the package in
PackageInfo.receivers.
"""
GET_RECEIVERS = 0x00000002

"""
public static final int GET_RESOLVED_FILTER:
ResolveInfo flag: return the IntentFilter that
was matched for a particular ResolveInfo in
ResolveInfo.filter.
"""
GET_RESOLVED_FILTER = 0x00000040

"""
public static final int GET_SERVICES:
PackageInfo flag: return information about
services in the package in PackageInfo.services.
"""
GET_SERVICES = 0x00000004

"""
public static final int GET_SHARED_LIBRARY_FILES:
ApplicationInfo flag: return the
paths to the shared libraries
that are associated with an application.
This applies for any API returning an ApplicationInfo class, either
directly or nested inside of another.
"""
GET_SHARED_LIBRARY_FILES = 0x00000400

"""
public static final int GET_SIGNATURES:

This constant was deprecated
in API level 28.
use GET_SIGNING_CERTIFICATES instead

PackageInfo flag: return information about the
signatures included in the package.
"""
GET_SIGNATURES = 0x00000040

"""
public static final int GET_SIGNING_CERTIFICATES:
PackageInfo flag: return the signing certificates associated with
this package.  Each entry is a signing certificate that the package
has proven it is authorized to use, usually a past signing certificate from
which it has rotated.
"""
GET_SIGNING_CERTIFICATES = 0x08000000

"""
public static final int GET_UNINSTALLED_PACKAGES:

This constant was deprecated
in API level 24.
replaced with MATCH_UNINSTALLED_PACKAGES
"""
GET_UNINSTALLED_PACKAGES = 0x00002000

"""
public static final int GET_URI_PERMISSION_PATTERNS:
ProviderInfo flag: return the
URI permission patterns
that are associated with a content provider.
This applies for any API returning a ProviderInfo class, either
directly or nested inside of another.
"""
GET_URI_PERMISSION_PATTERNS = 0x00000800

"""
public static final int INSTALL_REASON_DEVICE_RESTORE:
Code indicating that this package was installed as part of restoring from 
another device.
"""
INSTALL_REASON_DEVICE_RESTORE = 0x00000002

"""
public static final int INSTALL_REASON_DEVICE_SETUP:
Code indicating that this package was installed as part of device setup.
"""
INSTALL_REASON_DEVICE_SETUP = 0x00000003

"""
public static final int INSTALL_REASON_POLICY:
Code indicating that this package was installed due to enterprise policy.
"""
INSTALL_REASON_POLICY = 0x00000001

"""
public static final int INSTALL_REASON_UNKNOWN:
Code indicating that the reason for installing this package is unknown.
"""
INSTALL_REASON_UNKNOWN = 0x00000000

"""
public static final int INSTALL_REASON_USER:
Code indicating that the package installation was initiated by the user.
"""
INSTALL_REASON_USER = 0x00000004

"""
public static final int MATCH_ALL:
Querying flag: if set and if the platform is doing any filtering of the
results, then the filtering will not happen. This is a synonym for saying
that all results should be returned.
This flag should be used with extreme care.
"""
MATCH_ALL = 0x00020000

"""
public static final int MATCH_DEFAULT_ONLY:
Resolution and querying flag: if set, only filters that support the
Intent.CATEGORY_DEFAULT will be considered for
matching.  This is a synonym for including the CATEGORY_DEFAULT in your
supplied Intent.
"""
MATCH_DEFAULT_ONLY = 0x00010000

"""
public static final int MATCH_DIRECT_BOOT_AWARE:
Querying flag: match components which are direct boot aware in
the returned info, regardless of the current user state.

When neither MATCH_DIRECT_BOOT_AWARE:
 nor
MATCH_DIRECT_BOOT_UNAWARE are specified, the default behavior is
to match only runnable components based on the user state. For example,
when a user is started but credentials have not been presented yet, the
user is running "locked" and only MATCH_DIRECT_BOOT_AWARE:

components are returned. Once the user credentials have been presented,
the user is running "unlocked" and both MATCH_DIRECT_BOOT_AWARE:

and MATCH_DIRECT_BOOT_UNAWARE components are returned.See 
also:UserManager.isUserUnlocked()
"""
MATCH_DIRECT_BOOT_AWARE = 0x00080000

"""
public static final int MATCH_DIRECT_BOOT_UNAWARE:
Querying flag: match components which are direct boot unaware in
the returned info, regardless of the current user state.

When neither MATCH_DIRECT_BOOT_AWARE nor
MATCH_DIRECT_BOOT_UNAWARE:
 are specified, the default behavior is
to match only runnable components based on the user state. For example,
when a user is started but credentials have not been presented yet, the
user is running "locked" and only MATCH_DIRECT_BOOT_AWARE
components are returned. Once the user credentials have been presented,
the user is running "unlocked" and both MATCH_DIRECT_BOOT_AWARE
and MATCH_DIRECT_BOOT_UNAWARE:
 components are returned.
 See also:UserManager.isUserUnlocked()
"""
MATCH_DIRECT_BOOT_UNAWARE = 0x00040000

"""
public static final int MATCH_DISABLED_COMPONENTS:
PackageInfo flag: include disabled components in the returned info.
"""
MATCH_DISABLED_COMPONENTS = 0x00000200

"""
public static final int MATCH_DISABLED_UNTIL_USED_COMPONENTS:
PackageInfo flag: include disabled components which are in
that state only because of COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED
in the returned info.  Note that if you set this flag, applications
that are in this disabled state will be reported as enabled.
"""
MATCH_DISABLED_UNTIL_USED_COMPONENTS = 0x00008000

"""
public static final int MATCH_SYSTEM_ONLY:
Querying flag: include only components from applications that are marked
with ApplicationInfo.FLAG_SYSTEM.
"""
MATCH_SYSTEM_ONLY = 0x00100000

"""
public static final int MATCH_UNINSTALLED_PACKAGES:
Flag parameter to retrieve some information about all applications (even
uninstalled ones) which have data directories. This state could have
resulted if applications have been deleted with flag
DONT_DELETE_DATA with a possibility of being replaced or
reinstalled in future.

Note: this flag may cause less information about currently installed
applications to be returned.
"""
MATCH_UNINSTALLED_PACKAGES = 0x00002000

"""
public static final long MAXIMUM_VERIFICATION_TIMEOUT:
Can be used as the millisecondsToDelay argument for
extendVerificationTimeout(int, int, long). This is the
maximum time PackageManager waits for the verification
agent to return (in milliseconds).
"""
MAXIMUM_VERIFICATION_TIMEOUT = 0x000000000036ee80

"""
public static final int PERMISSION_DENIED:
Permission check result: this is returned by checkPermission(String, String)
if the permission has not been granted to the given package.
"""
PERMISSION_DENIED = 0xffffffff

"""
public static final int PERMISSION_GRANTED:
Permission check result: this is returned by checkPermission(String, String)
if the permission has been granted to the given package.
"""
PERMISSION_GRANTED = 0x00000000

"""
public static final int SIGNATURE_FIRST_NOT_SIGNED:
Signature check result: this is returned by checkSignatures(int, int)
if the first package is not signed but the second is.
"""
SIGNATURE_FIRST_NOT_SIGNED = 0xffffffff

"""
public static final int SIGNATURE_MATCH:
Signature check result: this is returned by checkSignatures(int, int)
if all signatures on the two packages match.
"""
SIGNATURE_MATCH = 0x00000000

"""
public static final int SIGNATURE_NEITHER_SIGNED:
Signature check result: this is returned by checkSignatures(int, int)
if neither of the two packages is signed.
"""
SIGNATURE_NEITHER_SIGNED = 0x00000001

"""
public static final int SIGNATURE_NO_MATCH:
Signature check result: this is returned by checkSignatures(int, int)
if not all signatures on both packages match.
"""
SIGNATURE_NO_MATCH = 0xfffffffd

"""
public static final int SIGNATURE_SECOND_NOT_SIGNED:
Signature check result: this is returned by checkSignatures(int, int)
if the second package is not signed but the first is.
"""
SIGNATURE_SECOND_NOT_SIGNED = 0xfffffffe

"""
public static final int SIGNATURE_UNKNOWN_PACKAGE:
Signature check result: this is returned by checkSignatures(int, int)
if either of the packages are not valid.
"""
SIGNATURE_UNKNOWN_PACKAGE = 0xfffffffc

"""
public static final int VERIFICATION_ALLOW:
Used as the verificationCode argument for
verifyPendingInstall(int, int) to indicate that the calling
package verifier allows the installation to proceed.
"""
VERIFICATION_ALLOW = 0x00000001

"""
public static final int VERIFICATION_REJECT:
Used as the verificationCode argument for
verifyPendingInstall(int, int) to indicate the calling
package verifier does not vote to allow the installation to proceed.
"""
VERIFICATION_REJECT = 0xffffffff

"""
public static final int VERSION_CODE_HIGHEST:
Constant for specifying the highest installed package version code.
"""
VERSION_CODE_HIGHEST = 0xffffffff


class IPackageManager(object):
    """
    Class for retrieving various kinds of information related to the
    application packages that are currently installed on the device. You can
    find this class through Context.getPackageManager() .
    """
    __metaclass__ = abc.ABCMeta

    def addPackageToPreferred(self, packageName):
        """
        This method was deprecated in API level 7. This function no longer
        does anything; it was an old approach to managing preferred
        activities, which has been superseded by (and conflicts with) the
        modern activity-based preferences.
        :param packageName: String
        """
        pass

    def addPermission(self, info):
        """
        Add a new dynamic permission to the system.  For this to work, your
        package must have defined a permission tree through the
        <permission-tree> tag in its manifest.  A package can only add
        permissions to trees that were defined by either its own package or
        another with the same user id; a permission is in a tree if it matches
        the name of the permission tree + ".": for example, "com.foo.bar" is a
        member of the permission tree "com.foo".  It is good to make your
        permission tree name descriptive, because you are taking possession of
        that entire set of permission names.  Thus, it must be under a domain
        you control, with a suffix that will not match any normal permissions
        that may be declared in any applications that are part of that domain.
         New permissions must be added before any .apks are installed that use
        those permissions.  Permissions you add through this method are
        remembered across reboots of the device. If the given permission
        already exists, the info you supply here will be used to update it.
        :param info: PermissionInfo: Description of the permission to be added.
        :return boolean: Returns true if a new permission was created, false
        if an existing one was updated.
        :raises: SecurityExceptionif you are not allowed to add the given
        permission name.
        See also:
        removePermission(String)
        """
        pass

    def addPermissionAsync(self, info):
        """
        Like addPermission(PermissionInfo) but asynchronously persists the
        package manager state after returning from the call, allowing it to
        return quicker and batch a series of adds at the expense of no
        guarantee the added permission will be retained if the device is
        rebooted before it is written.
        :param info: PermissionInfo
        :return boolean:
        """
        pass

    def addPreferredActivity(self, filter, match, set, activity):
        """
        This method was deprecated in API level 8. This is a protected API
        that should not have been available to third party applications.  It
        is the platform's responsibility for assigning preferred activities
        and this cannot be directly modified.  Add a new preferred activity
        mapping to the system.  This will be used to automatically select the
        given activity component when Context.startActivity() finds multiple
        matching activities and also matches the given filter.
        :param filter: IntentFilter: The set of intents under which this
        activity will be made preferred.
        :param match: int: The IntentFilter match category that this
        preference applies to.
        :param set: ComponentName: The set of activities that the user was
        picking from when this preference was made.
        :param activity: ComponentName: The component name of the activity
        that is to be preferred.
        """
        pass

    def canRequestPackageInstalls(self):
        """
        Checks whether the calling package is allowed to request package
        installs through package installer. Apps are encouraged to call this
        API before launching the package installer via intent
        Intent.ACTION_INSTALL_PACKAGE. Starting from Android O, the user can
        explicitly choose what external sources they trust to install apps on
        the device. If this API returns false, the install request will be
        blocked by the package installer and a dialog will be shown to the
        user with an option to launch settings to change their preference. An
        application must target Android O or higher and declare permission
        Manifest.permission.REQUEST_INSTALL_PACKAGES in order to use this API.
        :return boolean: true if the calling package is trusted by the user
        to request install packages on the device, false otherwise.
        See also:
        Intent.ACTION_INSTALL_PACKAGE
        Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES
        """
        pass

    def canonicalToCurrentPackageNames(self, names):
        """
        Map from a packages canonical name to the current name in use on the
        device.
        :param names: String: Array of new names to be mapped.
        :return String[]: Returns an array of the same size as the original,
        containing the current name for each package.
        """
        pass

    def checkPermission(self, permName, pkgName):
        """
        Check whether a particular package has been granted a particular
        permission.
        :param permName: String: The name of the permission you are checking
        for.
        :param pkgName: String: The name of the package you are checking
        against.
        :return int: If the package has the permission, PERMISSION_GRANTED is
        returned.  If it does not have the permission, PERMISSION_DENIED is
        returned.Value is PERMISSION_GRANTED or PERMISSION_DENIED.
        See also:
        PERMISSION_GRANTED
        PERMISSION_DENIED
        """
        pass

    @overload('str', 'str')
    def checkSignatures(self, pkg1, pkg2):
        """
        Compare the signatures of two packages to determine if the same
        signature appears in both of them.  If they do contain the same
        signature, then they are allowed special privileges when working with
        each other: they can share the same user-id, run instrumentation
        against each other, etc.
        :param pkg1: String: First package name whose signature will be
        compared.
        :param pkg2: String: Second package name whose signature will be
        compared.
        :return int: Returns an integer indicating whether all signatures on
        the two packages match. The value is >= 0 (SIGNATURE_MATCH) if all
        signatures match or < 0 if there is not a match (SIGNATURE_NO_MATCH or
        SIGNATURE_UNKNOWN_PACKAGE).Value is SIGNATURE_MATCH,
        SIGNATURE_NEITHER_SIGNED, SIGNATURE_FIRST_NOT_SIGNED,
        SIGNATURE_SECOND_NOT_SIGNED, SIGNATURE_NO_MATCH or
        SIGNATURE_UNKNOWN_PACKAGE.
        See also:
        checkSignatures(int, int)
        """
        pass

    @checkSignatures.adddef('int', 'int')
    def checkSignatures(self, uid1, uid2):
        """
        Like checkSignatures(String, String), but takes UIDs of the two
        packages to be checked.  This can be useful, for example, when doing
        the check in an IPC, where the UID is the only identity available.  It
        is functionally identical to determining the package associated with
        the UIDs and checking their signatures.
        :param uid1: int: First UID whose signature will be compared.
        :param uid2: int: Second UID whose signature will be compared.
        :return int: Returns an integer indicating whether all signatures on
        the two packages match. The value is >= 0 (SIGNATURE_MATCH) if all
        signatures match or < 0 if there is not a match (SIGNATURE_NO_MATCH or
        SIGNATURE_UNKNOWN_PACKAGE).Value is SIGNATURE_MATCH,
        SIGNATURE_NEITHER_SIGNED, SIGNATURE_FIRST_NOT_SIGNED,
        SIGNATURE_SECOND_NOT_SIGNED, SIGNATURE_NO_MATCH or
        SIGNATURE_UNKNOWN_PACKAGE.
        See also:
        checkSignatures(String, String)
        """
        pass

    def clearInstantAppCookie(self):
        """
        Clears the instant application cookie for the calling app.
        See also:
        isInstantApp()
        isInstantApp(String)
        getInstantAppCookieMaxBytes()
        getInstantAppCookie()
        clearInstantAppCookie()
        """
        pass

    def clearPackagePreferredActivities(self, packageName):
        """
        Remove all preferred activity mappings, previously added with
        addPreferredActivity(IntentFilter, int, ComponentName[],
        ComponentName), from the system whose activities are implemented in
        the given package name. An application can only clear its own
        package(s).
        :param packageName: String: The name of the package whose preferred
        activity mappings are to be removed.
        """
        pass

    def currentToCanonicalPackageNames(self, names):
        """
        Map from the current package names in use on the device to whatever
        the current canonical name of that package is.
        :param names: String: Array of current names to be mapped.
        :return String[]: Returns an array of the same size as the original,
        containing the canonical name for each package.
        """
        pass

    def extendVerificationTimeout(self, id, verificationCodeAtTimeout, millisecondsToDelay):
        """
        Allows a package listening to the package verification broadcast to
        extend the default timeout for a response and declare what action to
        perform after the timeout occurs. The response must include the
        verificationCodeAtTimeout which is one of VERIFICATION_ALLOW or
        VERIFICATION_REJECT.  This method may only be called once per package
        id. Additional calls will have no effect.
        :param id: int: pending package identifier as passed via the
        EXTRA_VERIFICATION_ID Intent extra.
        :param verificationCodeAtTimeout: int: either VERIFICATION_ALLOW or
        VERIFICATION_REJECT. If verificationCodeAtTimeout is neither
        VERIFICATION_ALLOW or VERIFICATION_REJECT, then
        verificationCodeAtTimeout will default to VERIFICATION_REJECT.
        :param millisecondsToDelay: long: the amount of time requested for the
        timeout. Must be positive and less than MAXIMUM_VERIFICATION_TIMEOUT.
        If millisecondsToDelay is out of bounds, millisecondsToDelay will be
        set to the closest in bounds value; namely, 0 or
        MAXIMUM_VERIFICATION_TIMEOUT.
        :raises: SecurityExceptionif the caller does not have the
        PACKAGE_VERIFICATION_AGENT permission.
        """
        pass

    @overload('ComponentName')
    def getActivityBanner(self, activityName):
        """
        Retrieve the banner associated with an activity. Given the full name
        of an activity, retrieves the information about it and calls
        ComponentInfo.loadIcon() to return its banner. If the activity cannot
        be found, NameNotFoundException is thrown.
        :param activityName: ComponentName: Name of the activity whose banner
        is to be retrieved.
        :return Drawable: Returns the image of the banner, or null if the
        activity has no banner specified.
        :raises: PackageManager.NameNotFoundException. Thrown if the resources
        for the given activity could not be loaded.
        See also:
        getActivityBanner(Intent)
        """
        pass

    @getActivityBanner.adddef('Intent')
    def getActivityBanner(self, intent):
        """
        Retrieve the banner associated with an Intent. If
        intent.getClassName() is set, this simply returns the result of
        getActivityBanner(intent.getClassName()). Otherwise it resolves the
        intent's component and returns the banner associated with the resolved
        component. If intent.getClassName() cannot be found or the Intent
        cannot be resolved to a component, NameNotFoundException is thrown.
        :param intent: Intent: The intent for which you would like to retrieve
        a banner.
        :return Drawable: Returns the image of the banner, or null if the
        activity has no banner specified.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for application matching the given intent could not be loaded.
        See also:
        getActivityBanner(ComponentName)
        """
        pass

    @overload('Intent')
    def getActivityIcon(self, intent):
        """
        Retrieve the icon associated with an Intent.  If intent.getClassName()
        is set, this simply returns the result of
        getActivityIcon(intent.getClassName()).  Otherwise it resolves the
        intent's component and returns the icon associated with the resolved
        component. If intent.getClassName() cannot be found or the Intent
        cannot be resolved to a component, NameNotFoundException is thrown.
        :param intent: Intent: The intent for which you would like to retrieve
        an icon.
        :return Drawable: Returns the image of the icon, or the default
        activity icon if it could not be found.  Does not return null.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for application matching the given intent could not be loaded.
        See also:
        getActivityIcon(ComponentName)
        """
        pass

    @getActivityIcon.adddef('ComponentName')
    def getActivityIcon(self, activityName):
        """
        Retrieve the icon associated with an activity.  Given the full name of
        an activity, retrieves the information about it and calls
        ComponentInfo.loadIcon() to return its icon. If the activity cannot be
        found, NameNotFoundException is thrown.
        :param activityName: ComponentName: Name of the activity whose icon is
        to be retrieved.
        :return Drawable: Returns the image of the icon, or the default
        activity icon if it could not be found.  Does not return null.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given activity could not be loaded.
        See also:
        getActivityIcon(Intent)
        """
        pass

    def getActivityInfo(self, component, flags):
        """
        Retrieve all of the information we know about a particular activity
        class.
        :param component: ComponentName: The full component name (i.e.
        com.google.apps.contacts/com.google.apps.contacts. ContactsList) of an
        Activity class.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return ActivityInfo: An ActivityInfo containing information about
        the activity.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    @overload('Intent')
    def getActivityLogo(self, intent):
        """
        Retrieve the logo associated with an Intent.  If intent.getClassName()
        is set, this simply returns the result of
        getActivityLogo(intent.getClassName()).  Otherwise it resolves the
        intent's component and returns the logo associated with the resolved
        component. If intent.getClassName() cannot be found or the Intent
        cannot be resolved to a component, NameNotFoundException is thrown.
        :param intent: Intent: The intent for which you would like to retrieve
        a logo.
        :return Drawable: Returns the image of the logo, or null if the
        activity has no logo specified.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for application matching the given intent could not be loaded.
        See also:
        getActivityLogo(ComponentName)
        """
        pass

    @getActivityLogo.adddef('ComponentName')
    def getActivityLogo(self, activityName):
        """
        Retrieve the logo associated with an activity. Given the full name of
        an activity, retrieves the information about it and calls
        ComponentInfo.loadLogo() to return its logo. If the activity cannot be
        found, NameNotFoundException is thrown.
        :param activityName: ComponentName: Name of the activity whose logo is
        to be retrieved.
        :return Drawable: Returns the image of the logo or null if the
        activity has no logo specified.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given activity could not be loaded.
        See also:
        getActivityLogo(Intent)
        """
        pass

    def getAllPermissionGroups(self, flags):
        """
        Retrieve all of the known permission groups in the system.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return List<PermissionGroupInfo>: Returns a list of
        PermissionGroupInfo containing information about all of the known
        permission groups.
        """
        pass

    @overload('str')
    def getApplicationBanner(self, packageName):
        """
        Retrieve the banner associated with an application. Given the name of
        the application's package, retrieves the information about it and
        calls getApplicationIcon() to return its banner. If the application
        cannot be found, NameNotFoundException is thrown.
        :param packageName: String: Name of the package whose application
        banner is to be retrieved.
        :return Drawable: Returns the image of the banner or null if the
        application has no banner specified.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded.
        See also:
        getApplicationBanner(ApplicationInfo)
        """
        pass

    @getApplicationBanner.adddef('ApplicationInfo')
    def getApplicationBanner(self, info):
        """
        Retrieve the banner associated with an application.
        :param info: ApplicationInfo: Information about application being
        queried.
        :return Drawable: Returns the image of the banner or null if the
        application has no banner specified.
        See also:
        getApplicationBanner(String)
        """
        pass

    def getApplicationEnabledSetting(self, packageName):
        """
        Return the enabled setting for an application. This returns the last
        value set by setApplicationEnabledSetting(String, int, int); in most
        cases this value will be COMPONENT_ENABLED_STATE_DEFAULT since the
        value originally specified in the manifest has not been modified.
        :param packageName: String: The package name of the application to
        retrieve.
        :return int: Returns the current enabled state for the
        application.Value is COMPONENT_ENABLED_STATE_DEFAULT,
        COMPONENT_ENABLED_STATE_ENABLED, COMPONENT_ENABLED_STATE_DISABLED,
        COMPONENT_ENABLED_STATE_DISABLED_USER or
        COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED.
        :raises: IllegalArgumentExceptionif the named package does not exist.
        """
        pass

    @overload('ApplicationInfo')
    def getApplicationIcon(self, info):
        """
        Retrieve the icon associated with an application.  If it has not
        defined an icon, the default app icon is returned.  Does not return
        null.
        :param info: ApplicationInfo: Information about application being
        queried.
        :return Drawable: Returns the image of the icon, or the default
        application icon if it could not be found.
        See also:
        getApplicationIcon(String)
        """
        pass

    @getApplicationIcon.adddef('str')
    def getApplicationIcon(self, packageName):
        """
        Retrieve the icon associated with an application.  Given the name of
        the application's package, retrieves the information about it and
        calls getApplicationIcon() to return its icon. If the application
        cannot be found, NameNotFoundException is thrown.
        :param packageName: String: Name of the package whose application icon
        is to be retrieved.
        :return Drawable: Returns the image of the icon, or the default
        application icon if it could not be found.  Does not return null.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded.
        See also:
        getApplicationIcon(ApplicationInfo)
        """
        pass

    def getApplicationInfo(self, packageName, flags):
        """
        Retrieve all of the information we know about a particular
        package/application.
        :param packageName: String: The full name (i.e.
        com.google.apps.contacts) of an application.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_UNINSTALLED_PACKAGES,
        MATCH_SYSTEM_ONLY, MATCH_DISABLED_COMPONENTS or
        MATCH_DISABLED_UNTIL_USED_COMPONENTS.
        :return ApplicationInfo: An ApplicationInfo containing information
        about the package. If flag MATCH_UNINSTALLED_PACKAGES is set and if
        the package is not found in the list of installed applications, the
        application information is retrieved from the list of uninstalled
        applications (which includes installed applications as well as
        applications with data directory i.e. applications which had been
        deleted with DONT_DELETE_DATA flag set).
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getApplicationLabel(self, info):
        """
        Return the label to use for this application.
        :param info: ApplicationInfo: The application to get the label of.
        :return CharSequence: Returns the label associated with this
        application, or null if it could not be found for any reason.
        """
        pass

    @overload('str')
    def getApplicationLogo(self, packageName):
        """
        Retrieve the logo associated with an application.  Given the name of
        the application's package, retrieves the information about it and
        calls getApplicationLogo() to return its logo. If the application
        cannot be found, NameNotFoundException is thrown.
        :param packageName: String: Name of the package whose application logo
        is to be retrieved.
        :return Drawable: Returns the image of the logo, or null if no
        application logo has been specified.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded.
        See also:
        getApplicationLogo(ApplicationInfo)
        """
        pass

    @getApplicationLogo.adddef('ApplicationInfo')
    def getApplicationLogo(self, info):
        """
        Retrieve the logo associated with an application.  If it has not
        specified a logo, this method returns null.
        :param info: ApplicationInfo: Information about application being
        queried.
        :return Drawable: Returns the image of the logo, or null if no logo
        is specified by the application.
        See also:
        getApplicationLogo(String)
        """
        pass

    def getChangedPackages(self, sequenceNumber):
        """
        Returns the names of the packages that have been changed [eg. added,
        removed or updated] since the given sequence number. If no packages
        have been changed, returns null. The sequence number starts at 0 and
        is reset every boot.
        :param sequenceNumber: int: The first sequence number for which to
        retrieve package changes.
        :return ChangedPackages: This value may be null.
        See also:
        ERROR(/Settings.Global#BOOT_COUNT)
        """
        pass

    def getComponentEnabledSetting(self, componentName):
        """
        Return the enabled setting for a package component (activity,
        receiver, service, provider).  This returns the last value set by
        setComponentEnabledSetting(ComponentName, int, int); in most cases
        this value will be COMPONENT_ENABLED_STATE_DEFAULT since the value
        originally specified in the manifest has not been modified.
        :param componentName: ComponentName: The component to retrieve.
        :return int: Returns the current enabled state for the component.
        Value is COMPONENT_ENABLED_STATE_DEFAULT,
        COMPONENT_ENABLED_STATE_ENABLED, COMPONENT_ENABLED_STATE_DISABLED,
        COMPONENT_ENABLED_STATE_DISABLED_USER or
        COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED.
        """
        pass

    def getDefaultActivityIcon(self):
        """
        Return the generic icon for an activity that is used when no specific
        icon is defined.
        :return Drawable: Drawable Image of the icon.
        """
        pass

    def getDrawable(self, packageName, resid, appInfo):
        """
        Retrieve an image from a package.  This is a low-level API used by the
        various package manager info structures (such as ComponentInfo to
        implement retrieval of their associated icon.
        :param packageName: String: The name of the package that this icon is
        coming from. Cannot be null.
        :param resid: int: The resource identifier of the desired image.
        Cannot be 0.
        :param appInfo: ApplicationInfo: Overall information about
        packageName.  This may be null, in which case the application
        information will be retrieved for you if needed; if you already have
        this information around, it can be much more efficient to supply it
        here.
        :return Drawable: Returns a Drawable holding the requested image.
        Returns null if an image could not be found for any reason.
        """
        pass

    def getInstalledApplications(self, flags):
        """
        Return a List of all application packages that are installed for the
        current user. If flag GET_UNINSTALLED_PACKAGES has been set, a list of
        all applications including those deleted with DONT_DELETE_DATA
        (partially installed apps with data directory) will be returned.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_UNINSTALLED_PACKAGES,
        MATCH_SYSTEM_ONLY, MATCH_DISABLED_COMPONENTS or
        MATCH_DISABLED_UNTIL_USED_COMPONENTS.
        :return List<ApplicationInfo>: A List of ApplicationInfo objects, one
        for each installed application. In the unlikely case there are no
        installed packages, an empty list is returned. If flag
        MATCH_UNINSTALLED_PACKAGES is set, the application information is
        retrieved from the list of uninstalled applications (which includes
        installed applications as well as applications with data directory
        i.e. applications which had been deleted with DONT_DELETE_DATA flag
        set).
        """
        pass

    def getInstalledPackages(self, flags):
        """
        Return a List of all packages that are installed for the current user.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return List<PackageInfo>: A List of PackageInfo objects, one for
        each installed package, containing information about the package. In
        the unlikely case there are no installed packages, an empty list is
        returned. If flag MATCH_UNINSTALLED_PACKAGES is set, the package
        information is retrieved from the list of uninstalled applications
        (which includes installed applications as well as applications with
        data directory i.e. applications which had been deleted with
        DONT_DELETE_DATA flag set).
        """
        pass

    def getInstallerPackageName(self, packageName):
        """
        Retrieve the package name of the application that installed a package.
        This identifies which market the package came from.
        :param packageName: String: The name of the package to query
        :return String:
        :raises: IllegalArgumentExceptionif the given package name is not
        installed
        """
        pass

    def getInstantAppCookie(self):
        """
        Gets the instant application cookie for this app. Non instant apps and
        apps that were instant but were upgraded to normal apps can still
        access this API. For instant apps this cookie is cached for some time
        after uninstall while for normal apps the cookie is deleted after the
        app is uninstalled. The cookie is always present while the app is
        installed.
        :return byte[]: The cookie.This value will never be null.
        See also:
        isInstantApp()
        isInstantApp(String)
        updateInstantAppCookie(byte[])
        getInstantAppCookieMaxBytes()
        clearInstantAppCookie()
        """
        pass

    def getInstantAppCookieMaxBytes(self):
        """
        Gets the maximum size in bytes of the cookie data an instant app can
        store on the device.
        :return int: The max cookie size in bytes.
        See also:
        isInstantApp()
        isInstantApp(String)
        updateInstantAppCookie(byte[])
        getInstantAppCookie()
        clearInstantAppCookie()
        """
        pass

    def getInstrumentationInfo(self, className, flags):
        """
        Retrieve all of the information we know about a particular
        instrumentation class.
        :param className: ComponentName: The full name (i.e.
        com.google.apps.contacts.InstrumentList) of an Instrumentation class.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return InstrumentationInfo: An InstrumentationInfo object containing
        information about the instrumentation.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getLaunchIntentForPackage(self, packageName):
        """
        Returns a "good" intent to launch a front-door activity in a package.
        This is used, for example, to implement an "open" button when browsing
        through packages.  The current implementation looks first for a main
        activity in the category Intent.CATEGORY_INFO, and next for a main
        activity in the category Intent.CATEGORY_LAUNCHER. Returns null if
        neither are found.
        :param packageName: String: The name of the package to inspect.This
        value must never be null.
        :return Intent: A fully-qualified Intent that can be used to launch
        the main activity in the package. Returns null if the package does not
        contain such an activity, or if packageName is not recognized.
        """
        pass

    def getLeanbackLaunchIntentForPackage(self, packageName):
        """
        Return a "good" intent to launch a front-door Leanback activity in a
        package, for use for example to implement an "open" button when
        browsing through packages. The current implementation will look for a
        main activity in the category Intent.CATEGORY_LEANBACK_LAUNCHER, or
        return null if no main leanback activities are found.
        :param packageName: String: The name of the package to inspect.This
        value must never be null.
        :return Intent: Returns either a fully-qualified Intent that can be
        used to launch the main Leanback activity in the package, or null if
        the package does not contain such an activity.
        """
        pass

    def getNameForUid(self, uid):
        """
        Retrieve the official name associated with a uid. This name is
        guaranteed to never change, though it is possible for the underlying
        uid to be changed.  That is, if you are storing information about uids
        in persistent storage, you should use the string returned by this
        function instead of the raw uid.
        :param uid: int: The uid for which you would like to retrieve a name.
        :return String: Returns a unique name for the given uid, or null if
        the uid is not currently assigned.
        """
        pass

    def getPackageArchiveInfo(self, archiveFilePath, flags):
        """
        Retrieve overall information about an application package defined in a
        package archive file
        :param archiveFilePath: String: The path to the archive file
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return PackageInfo: A PackageInfo object containing information
        about the package archive. If the package could not be parsed, returns
        null.
        """
        pass

    @overload('str')
    def getPackageGids(self, packageName):
        """
        Return an array of all of the POSIX secondary group IDs that have been
        assigned to the given package.  Note that the same package may have
        different GIDs under different UserHandle on the same device.
        :param packageName: String: The full name (i.e.
        com.google.apps.contacts) of the desired package.This value must never
        be null.
        :return int[]: Returns an int array of the assigned GIDs, or null if
        there are none.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    @getPackageGids.adddef('str', 'int')
    def getPackageGids(self, packageName, flags):
        """
        Return an array of all of the POSIX secondary group IDs that have been
        assigned to the given package.  Note that the same package may have
        different GIDs under different UserHandle on the same device.
        :param packageName: String: The full name (i.e.
        com.google.apps.contacts) of the desired package.
        :param flags: intValue is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return int[]: Returns an int array of the assigned gids, or null if
        there are none.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    @overload('str', 'int')
    def getPackageInfo(self, packageName, flags):
        """
        Retrieve overall information about an application package that is
        installed on the system.
        :param packageName: String: The full name (i.e.
        com.google.apps.contacts) of the desired package.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return PackageInfo: A PackageInfo object containing information
        about the package. If flag MATCH_UNINSTALLED_PACKAGES is set and if
        the package is not found in the list of installed applications, the
        package information is retrieved from the list of uninstalled
        applications (which includes installed applications as well as
        applications with data directory i.e. applications which had been
        deleted with DONT_DELETE_DATA flag set).
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    @getPackageInfo.adddef('VersionedPackage', 'int')
    def getPackageInfo(self, versionedPackage, flags):
        """
        Retrieve overall information about an application package that is
        installed on the system. This method can be used for retrieving
        information about packages for which multiple versions can be
        installed at the time. Currently only packages hosting static shared
        libraries can have multiple installed versions. The method can also be
        used to get info for a package that has a single version installed by
        passing VERSION_CODE_HIGHEST in the VersionedPackage constructor.
        :param versionedPackage: VersionedPackage: The versioned package for
        which to query.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return PackageInfo: A PackageInfo object containing information
        about the package. If flag MATCH_UNINSTALLED_PACKAGES is set and if
        the package is not found in the list of installed applications, the
        package information is retrieved from the list of uninstalled
        applications (which includes installed applications as well as
        applications with data directory i.e. applications which had been
        deleted with DONT_DELETE_DATA flag set).
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getPackageInstaller(self):
        """
        Return interface that offers the ability to install, upgrade, and
        remove applications on the device.
        :return PackageInstaller: This value will never be null.
        """
        pass

    def getPackageUid(self, packageName, flags):
        """
        Return the UID associated with the given package name.  Note that the
        same package will have different UIDs under different UserHandle on
        the same device.
        :param packageName: String: The full name (i.e.
        com.google.apps.contacts) of the desired package.
        :param flags: intValue is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return int: Returns an integer UID who owns the given package name.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name can not be found on the system.
        """
        pass

    def getPackagesForUid(self, uid):
        """
        Retrieve the names of all packages that are associated with a
        particular user id.  In most cases, this will be a single package
        name, the package that has been assigned that user id.  Where there
        are multiple packages sharing the same user id through the
        "sharedUserId" mechanism, all packages with that id will be returned.
        :param uid: int: The user id for which you would like to retrieve the
        associated packages.
        :return String[]: Returns an array of one or more packages assigned
        to the user id, or null if there are no known packages with the given
        id.
        """
        pass

    def getPackagesHoldingPermissions(self, permissions, flags):
        """
        Return a List of all installed packages that are currently holding any
        of the given permissions.
        :param permissions: String
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return List<PackageInfo>: A List of PackageInfo objects, one for
        each installed package that holds any of the permissions that were
        provided, containing information about the package. If no installed
        packages hold any of the permissions, an empty list is returned. If
        flag MATCH_UNINSTALLED_PACKAGES is set, the package information is
        retrieved from the list of uninstalled applications (which includes
        installed applications as well as applications with data directory
        i.e. applications which had been deleted with DONT_DELETE_DATA flag
        set).
        """
        pass

    def getPermissionGroupInfo(self, name, flags):
        """
        Retrieve all of the information we know about a particular group of
        permissions.
        :param name: String: The fully qualified name (i.e.
        com.google.permission_group.APPS) of the permission you are interested
        in.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return PermissionGroupInfo: Returns a PermissionGroupInfo containing
        information about the permission.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getPermissionInfo(self, name, flags):
        """
        Retrieve all of the information we know about a particular permission.
        :param name: String: The fully qualified name (i.e.
        com.google.permission.LOGIN) of the permission you are interested in.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return PermissionInfo: Returns a PermissionInfo containing
        information about the permission.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getPreferredActivities(self, outFilters, outActivities, packageName):
        """
        Retrieve all preferred activities, previously added with
        addPreferredActivity(IntentFilter, int, ComponentName[],
        ComponentName), that are currently registered with the system.
        :param outFilters: List: A required list in which to place the filters
        of all of the preferred activities.This value must never be null.
        :param outActivities: List: A required list in which to place the
        component names of all of the preferred activities.This value must
        never be null.
        :param packageName: String: An optional package in which you would
        like to limit the list.  If null, all activities will be returned; if
        non-null, only those activities in the given package are returned.
        :return int: Returns the total number of registered preferred
        activities (the number of distinct IntentFilter records, not the
        number of unique activity components) that were found.
        """
        pass

    def getPreferredPackages(self, flags):
        """
        Retrieve the list of all currently configured preferred packages. The
        first package on the list is the most preferred, the last is the least
        preferred.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_ACTIVITIES,
        GET_CONFIGURATIONS, GET_GIDS, GET_INSTRUMENTATION, GET_INTENT_FILTERS,
        GET_META_DATA, GET_PERMISSIONS, GET_PROVIDERS, GET_RECEIVERS,
        GET_SERVICES, GET_SHARED_LIBRARY_FILES, GET_SIGNATURES,
        GET_SIGNING_CERTIFICATES, GET_URI_PERMISSION_PATTERNS,
        MATCH_UNINSTALLED_PACKAGES, MATCH_DISABLED_COMPONENTS,
        MATCH_DISABLED_UNTIL_USED_COMPONENTS or MATCH_SYSTEM_ONLY.
        :return List<PackageInfo>: A List of PackageInfo objects, one for
        each preferred application, in order of preference.
        """
        pass

    def getProviderInfo(self, component, flags):
        """
        Retrieve all of the information we know about a particular content
        provider class.
        :param component: ComponentName: The full component name (i.e.
        com.google.providers.media/com.google.providers.media. MediaProvider)
        of a ContentProvider class.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return ProviderInfo: A ProviderInfo object containing information
        about the provider.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getReceiverInfo(self, component, flags):
        """
        Retrieve all of the information we know about a particular receiver
        class.
        :param component: ComponentName: The full component name (i.e.
        com.google.apps.calendar/com.google.apps.calendar. CalendarAlarm) of a
        Receiver class.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return ActivityInfo: An ActivityInfo containing information about
        the receiver.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getResourcesForActivity(self, activityName):
        """
        Retrieve the resources associated with an activity.  Given the full
        name of an activity, retrieves the information about it and calls
        getResources() to return its application's resources.  If the activity
        cannot be found, NameNotFoundException is thrown.
        :param activityName: ComponentName: Name of the activity whose
        resources are to be retrieved.
        :return Resources: Returns the application's Resources.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded.
        See also:
        getResourcesForApplication(ApplicationInfo)
        """
        pass

    @overload('ApplicationInfo')
    def getResourcesForApplication(self, app):
        """
        Retrieve the resources for an application.  Throws
        NameNotFoundException if the package is no longer installed.
        :param app: ApplicationInfo: Information about the desired application.
        :return Resources: Returns the application's Resources.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded (most likely because it
        was uninstalled).
        """
        pass

    @getResourcesForApplication.adddef('str')
    def getResourcesForApplication(self, appPackageName):
        """
        Retrieve the resources associated with an application.  Given the full
        package name of an application, retrieves the information about it and
        calls getResources() to return its application's resources.  If the
        appPackageName cannot be found, NameNotFoundException is thrown.
        :param appPackageName: String: Package name of the application whose
        resources are to be retrieved.
        :return Resources: Returns the application's Resources.
        :raises: PackageManager.NameNotFoundExceptionThrown if the resources
        for the given application could not be loaded.
        See also:
        getResourcesForApplication(ApplicationInfo)
        """
        pass

    def getServiceInfo(self, component, flags):
        """
        Retrieve all of the information we know about a particular service
        class.
        :param component: ComponentName: The full component name (i.e.
        com.google.apps.media/com.google.apps.media. BackgroundPlayback) of a
        Service class.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return ServiceInfo: A ServiceInfo object containing information
        about the service.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def getSharedLibraries(self, flags):
        """
        Get a list of shared libraries on the device.
        :param flags: int: To filter the libraries to return.Value is either 0
        or combination of INSTALL_REASON_POLICY, INSTALL_REASON_DEVICE_RESTORE
        or INSTALL_REASON_USER.
        :return List<SharedLibraryInfo>: The shared library list.This value
        will never be null.
        See also:
        MATCH_UNINSTALLED_PACKAGES
        """
        pass

    def getSuspendedPackageAppExtras(self):
        """
        Returns a Bundle of extras that was meant to be sent to the calling
        app when it was suspended. An app with the permission
        android.permission.SUSPEND_APPS can supply this to the system at the
        time of suspending an app.  This is the same Bundle that is sent along
        with the broadcast Intent.ACTION_MY_PACKAGE_SUSPENDED, whenever the
        app is suspended. The contents of this Bundle are a contract between
        the suspended app and the suspending app.  Note: These extras are
        optional, so if no extras were supplied to the system, this method
        will return null, even when the calling app has been suspended.
        :return Bundle: A Bundle containing the extras for the app, or null
        if the package is not currently suspended.
        See also:
        isPackageSuspended()
        Intent.ACTION_MY_PACKAGE_UNSUSPENDED
        Intent.ACTION_MY_PACKAGE_SUSPENDED
        Intent.EXTRA_SUSPENDED_PACKAGE_EXTRAS
        """
        pass

    def getSystemAvailableFeatures(self):
        """
        Get a list of features that are available on the system.
        :return FeatureInfo[]: An array of FeatureInfo classes describing the
        features that are available on the system, or null if there are
        none(!!).
        """
        pass

    def getSystemSharedLibraryNames(self):
        """
        Get a list of shared libraries that are available on the system.
        :return String[]: An array of shared library names that are available
        on the system, or null if none are installed.
        """
        pass

    def getText(self, packageName, resid, appInfo):
        """
        Retrieve text from a package.  This is a low-level API used by the
        various package manager info structures (such as ComponentInfo to
        implement retrieval of their associated labels and other text.
        :param packageName: String: The name of the package that this text is
        coming from. Cannot be null.
        :param resid: int: The resource identifier of the desired text.
        Cannot be 0.
        :param appInfo: ApplicationInfo: Overall information about
        packageName.  This may be null, in which case the application
        information will be retrieved for you if needed; if you already have
        this information around, it can be much more efficient to supply it
        here.
        :return CharSequence: Returns a CharSequence holding the requested
        text.  Returns null if the text could not be found for any reason.
        """
        pass

    def getUserBadgedDrawableForDensity(self, drawable, user, badgeLocation, badgeDensity):
        """
        If the target user is a managed profile of the calling user or the
        caller is itself a managed profile, then this returns a badged copy of
        the given drawable allowing the user to distinguish it from the
        original drawable. The caller can specify the location in the bounds
        of the drawable to be badged where the badge should be applied as well
        as the density of the badge to be used.  If the original drawable is a
        BitmapDrawable and the backing bitmap is mutable as per
        Bitmap.isMutable(), the badging is performed in place and the original
        drawable is returned.
        :param drawable: Drawable: The drawable to badge.
        :param user: UserHandle: The target user.
        :param badgeLocation: Rect: Where in the bounds of the badged drawable
        to place the badge. If it's null, the badge is applied on top of the
        entire drawable being badged.
        :param badgeDensity: int: The optional desired density for the badge
        as per DisplayMetrics.densityDpi. If it's not positive, the density of
        the display is used.
        :return Drawable: A drawable that combines the original drawable and
        a badge as determined by the system.
        """
        pass

    def getUserBadgedIcon(self, icon, user):
        """
        If the target user is a managed profile, then this returns a badged
        copy of the given icon to be able to distinguish it from the original
        icon. For badging an arbitrary drawable use
        getUserBadgedDrawableForDensity(android.graphics.drawable.Drawable,
        UserHandle, android.graphics.Rect, int).  If the original drawable is
        a BitmapDrawable and the backing bitmap is mutable as per
        Bitmap.isMutable(), the badging is performed in place and the original
        drawable is returned.
        :param icon: Drawable: The icon to badge.
        :param user: UserHandle: The target user.
        :return Drawable: A drawable that combines the original icon and a
        badge as determined by the system.
        """
        pass

    def getUserBadgedLabel(self, label, user):
        """
        If the target user is a managed profile of the calling user or the
        caller is itself a managed profile, then this returns a copy of the
        label with badging for accessibility services like talkback. E.g.
        passing in "Email" and it might return "Work Email" for Email in the
        work profile.
        :param label: CharSequence: The label to change.
        :param user: UserHandle: The target user.
        :return CharSequence: A label that combines the original label and a
        badge as determined by the system.
        """
        pass

    def getXml(self, packageName, resid, appInfo):
        """
        Retrieve an XML file from a package.  This is a low-level API used to
        retrieve XML meta data.
        :param packageName: String: The name of the package that this xml is
        coming from. Cannot be null.
        :param resid: int: The resource identifier of the desired xml.  Cannot
        be 0.
        :param appInfo: ApplicationInfo: Overall information about
        packageName.  This may be null, in which case the application
        information will be retrieved for you if needed; if you already have
        this information around, it can be much more efficient to supply it
        here.
        :return XmlResourceParser: Returns an XmlPullParser allowing you to
        parse out the XML data.  Returns null if the xml resource could not be
        found for any reason.
        """
        pass

    @overload('int', 'byte[]', 'int')
    def hasSigningCertificate(self, uid, certificate, type):
        """
        Searches the set of signing certificates by which the package(s) for
        the given uid has proven to have been signed.  For multiple packages
        sharing the same uid, this will return the signing certificates found
        in the signing history of the "newest" package, where "newest"
        indicates the package with the newest signing certificate in the
        shared uid group.  This method should be used instead of
        getPackageInfo with GET_SIGNATURES since it takes into account the
        possibility of signing certificate rotation, except in the case of
        packages that are signed by multiple certificates, for which signing
        certificate rotation is not supported. This method is analogous to
        using getPackagesForUid followed by getPackageInfo with
        GET_SIGNING_CERTIFICATES, selecting the PackageInfo of the
        newest-signed bpackage , and finally searching through the resulting
        signingInfo field to see if the desired certificate is there.
        :param uid: int: uid whose signing
        :param certificate: s to checkcertificatebyte: signing certificate for
        which to search
        :param type: int: representation of the certificateValue is
        CERT_INPUT_RAW_X509 or CERT_INPUT_SHA256.
        :return boolean: true if this package was or is signed by exactly the
        certificate certificate
        """
        pass

    @hasSigningCertificate.adddef('str', 'byte[]', 'int')
    def hasSigningCertificate(self, packageName, certificate, type):
        """
        Searches the set of signing certificates by which the given package
        has proven to have been signed.  This should be used instead of
        getPackageInfo with GET_SIGNATURES since it takes into account the
        possibility of signing certificate rotation, except in the case of
        packages that are signed by multiple certificates, for which signing
        certificate rotation is not supported.  This method is analogous to
        using getPackageInfo with GET_SIGNING_CERTIFICATES and then searching
        through the resulting signingInfo field to see if the desired
        certificate is present.
        :param packageName: String: package whose signing
        :param certificate: s to checkcertificatebyte: signing certificate for
        which to search
        :param type: int: representation of the certificateValue is
        CERT_INPUT_RAW_X509 or CERT_INPUT_SHA256.
        :return boolean: true if this package was or is signed by exactly the
        certificate certificate
        """
        pass

    @overload('str')
    def hasSystemFeature(self, name):
        """
        Check whether the given feature name is one of the available features
        as returned by getSystemAvailableFeatures(). This tests for the
        presence of any version of the given feature name; use
        hasSystemFeature(String, int) to check for a minimum version.
        :param name: String
        :return boolean: Returns true if the devices supports the feature,
        else false.
        """
        pass

    @hasSystemFeature.adddef('str', 'int')
    def hasSystemFeature(self, name, version):
        """
        Check whether the given feature name and version is one of the
        available features as returned by getSystemAvailableFeatures(). Since
        features are defined to always be backwards compatible, this returns
        true if the available feature version is greater than or equal to the
        requested version.
        :param name: String
        :param version: int
        :return boolean: Returns true if the devices supports the feature,
        else false.
        """
        pass

    @overload
    def isInstantApp(self):
        """
        Gets whether this application is an instant app.
        :return boolean: Whether caller is an instant app.
        See also:
        isInstantApp(String)
        updateInstantAppCookie(byte[])
        getInstantAppCookie()
        getInstantAppCookieMaxBytes()
        """
        pass

    @isInstantApp.adddef('str')
    def isInstantApp(self, packageName):
        """
        Gets whether the given package is an instant app.
        :param packageName: String: The package to check
        :return boolean: Whether the given package is an instant app.
        See also:
        isInstantApp()
        updateInstantAppCookie(byte[])
        getInstantAppCookie()
        getInstantAppCookieMaxBytes()
        clearInstantAppCookie()
        """
        pass

    def isPackageSuspended(self):
        """
        Apps can query this to know if they have been suspended. A system app
        with the permission android.permission.SUSPEND_APPS can put any app on
        the device into a suspended state.  While in this state, the
        application's notifications will be hidden, any of its started
        activities will be stopped and it will not be able to show toasts or
        dialogs or ring the device. When the user tries to launch a suspended
        app, the system will, instead, show a dialog to the user informing
        them that they cannot use this app while it is suspended.  When an app
        is put into this state, the broadcast action
        Intent.ACTION_MY_PACKAGE_SUSPENDED will be delivered to any of its
        broadcast receivers that included this action in their intent-filters,
        including manifest receivers. Similarly, a broadcast action
        Intent.ACTION_MY_PACKAGE_UNSUSPENDED is delivered when a previously
        suspended app is taken out of this state.
        :return boolean: true if the calling package has been suspended,
        false otherwise.
        See also:
        getSuspendedPackageAppExtras()
        Intent.ACTION_MY_PACKAGE_SUSPENDED
        Intent.ACTION_MY_PACKAGE_UNSUSPENDED
        """
        pass

    def isPermissionRevokedByPolicy(self, permName, pkgName):
        """
        Checks whether a particular permissions has been revoked for a package
        by policy. Typically the device owner or the profile owner may apply
        such a policy. The user cannot grant policy revoked permissions, hence
        the only way for an app to get such a permission is by a policy change.
        :param permName: String: The name of the permission you are checking
        for.This value must never be null.
        :param pkgName: String: The name of the package you are checking
        against.This value must never be null.
        :return boolean: Whether the permission is restricted by policy.
        """
        pass

    def isSafeMode(self):
        """
        Return whether the device has been booted into safe mode.
        :return boolean:
        """
        pass

    def queryBroadcastReceivers(self, intent, flags):
        """
        Retrieve all receivers that can handle a broadcast of the given intent.
        :param intent: Intent: The desired intent as per resolveActivity().
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return List<ResolveInfo>: Returns a List of ResolveInfo objects
        containing one entry for each matching receiver, ordered from best to
        worst. If there are no matching receivers, an empty list or null is
        returned.
        """
        pass

    def queryContentProviders(self, processName, uid, flags):
        """
        Retrieve content provider information. Note: unlike most other
        methods, an empty result set is indicated by a null return instead of
        an empty list.
        :param processName: String: If non-null, limits the returned providers
        to only those that are hosted by the given process. If null, all
        content providers are returned.
        :param uid: int: If processName is non-null, this is the required uid
        owning the requested content providers.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return List<ProviderInfo>: A list of ProviderInfo objects containing
        one entry for each provider either matching processName or, if
        processName is null, all known content providers. If there are no
        matching providers, null is returned.
        """
        pass

    def queryInstrumentation(self, targetPackage, flags):
        """
        Retrieve information about available instrumentation code. May be used
        to retrieve either all instrumentation code, or only the code
        targeting a particular package.
        :param targetPackage: String: If null, all instrumentation is
        returned; only the instrumentation targeting this package name is
        returned.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return List<InstrumentationInfo>: A list of InstrumentationInfo
        objects containing one entry for each matching instrumentation. If
        there are no instrumentation available, returns an empty list.
        """
        pass

    def queryIntentActivities(self, intent, flags):
        """
        Retrieve all activities that can be performed for the given intent.
        :param intent: Intent: The desired intent as per resolveActivity().
        :param flags: int: Additional option flags to modify the data
        returned. The most important is MATCH_DEFAULT_ONLY, to limit the
        resolution to only those activities that support the
        Intent.CATEGORY_DEFAULT. Or, set MATCH_ALL to prevent any filtering of
        the results.Value is either 0 or combination of GET_META_DATA,
        GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: List<ResolveInfo>. Returns a List of ResolveInfo objects
        containing one entry for each matching activity, ordered from best to
        worst. In other words, the first item is what would be returned by
        resolveActivity(Intent, int). If there are no matching activities, an
        empty list is returned.
        """
        pass

    def queryIntentActivityOptions(self, caller, specifics, intent, flags):
        """
        Retrieve a set of activities that should be presented to the user as
        similar options. This is like queryIntentActivities(Intent, int),
        except it also allows you to supply a list of more explicit Intents
        that you would like to resolve to particular options, and takes care
        of returning the final ResolveInfo list in a reasonable order, with no
        duplicates, based on those inputs.
        :param caller: ComponentName: The class name of the activity that is
        making the request. This activity will never appear in the output
        list. Can be null.
        :param specifics: Intent: An array of Intents that should be resolved
        to the first specific results. Can be null.
        :param intent: Intent: The desired intent as per resolveActivity().
        :param flags: int: Additional option flags to modify the data
        returned. The most important is MATCH_DEFAULT_ONLY, to limit the
        resolution to only those activities that support the
        Intent.CATEGORY_DEFAULT.Value is either 0 or combination of
        GET_META_DATA, GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: List<ResolveInfo>. Returns a List of ResolveInfo objects
        containing one entry for each matching activity. The list is ordered
        first by all of the intents resolved in specifics and then any
        additional activities that can handle intent but did not get included
        by one of the specifics intents. If there are no matching activities,
        an empty list is returned.
        """
        pass

    def queryIntentContentProviders(self, intent, flags):
        """
        Retrieve all providers that can match the given intent.
        :param intent: Intent: An intent containing all of the desired
        specification (action, data, type, category, and/or component).
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: List<ResolveInfo>. Returns a List of ResolveInfo objects
        containing one entry for each matching provider, ordered from best to
        worst. If there are no matching services, an empty list or null is
        returned.
        """
        pass

    def queryIntentServices(self, intent, flags):
        """
        Retrieve all services that can match the given intent.
        :param intent: Intent: The desired intent as per resolveService().
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: List<ResolveInfo>. Returns a List of ResolveInfo objects
        containing one entry for each matching service, ordered from best to
        worst. In other words, the first item is what would be returned by
        resolveService(Intent, int). If there are no matching services, an
        empty list or null is returned.
        """
        pass

    def queryPermissionsByGroup(self, group, flags):
        """
        Query for all of the permissions associated with a particular group.
        :param group: String: The fully qualified name (i.e.
        com.google.permission.LOGIN) of the permission group you are
        interested in. Use null to find all of the permissions not associated
        with a group.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or GET_META_DATA.
        :return: List<PermissionInfo>. Returns a list of PermissionInfo
        containing information about all of the permissions in the given group.
        :raises: PackageManager.NameNotFoundExceptionif a package with the
        given name cannot be found on the system.
        """
        pass

    def removePackageFromPreferred(self, packageName):
        """
        This method was deprecated in API level 7. This function no longer
        does anything; it was an old approach to managing preferred
        activities, which has been superseded by (and conflicts with) the
        modern activity-based preferences.
        :param packageName: String
        """
        pass

    def removePermission(self, name):
        """
        Removes a permission that was previously added with
        addPermission(PermissionInfo).  The same ownership rules apply -- you
        are only allowed to remove permissions that you are allowed to add.
        :param name: String: The name of the permission to remove.
        :raises: SecurityExceptionif you are not allowed to remove the given
        permission name.
        See also:
        addPermission(PermissionInfo)
        """
        pass

    def resolveActivity(self, intent, flags):
        """
        Determine the best action to perform for a given Intent. This is how
        Intent.resolveActivity(PackageManager) finds an activity if a class
        has not been explicitly specified. Note: if using an implicit Intent
        (without an explicit ComponentName specified), be sure to consider
        whether to set the MATCH_DEFAULT_ONLY only flag. You need to do so to
        resolve the activity in the same way that
        Context.startActivity(Intent) and
        Intent.resolveActivity(PackageManager) do.
        :param intent: Intent: An intent containing all of the desired
        specification (action, data, type, category, and/or component).
        :param flags: int: Additional option flags to modify the data
        returned. The most important is MATCH_DEFAULT_ONLY, to limit the
        resolution to only those activities that support the
        Intent.CATEGORY_DEFAULT.
        Value is either 0 or combination of
        GET_META_DATA, GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: ResolveInfo. Returns a ResolveInfo object containing the
        final activity intent that was determined to be the best action.
        Returns null if no matching activity was found. If multiple matching
        activities are found and there is no default set, returns a
        ResolveInfo object containing something else, such as the activity
        resolver.
        """
        pass

    def resolveContentProvider(self, name, flags):
        """
        Find a single content provider by its base path name.
        :param name: String: The name of the provider to find.
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SHARED_LIBRARY_FILES, MATCH_ALL, MATCH_DEFAULT_ONLY,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DIRECT_BOOT_AWARE, MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY
        or MATCH_UNINSTALLED_PACKAGES.
        :return: ProviderInfo. A ProviderInfo object containing information
        about the provider. If a provider was not found, returns null.
        """
        pass

    def resolveService(self, intent, flags):
        """
        Determine the best service to handle for a given Intent.
        :param intent: Intent: An intent containing all of the desired
        specification (action, data, type, category, and/or component).
        :param flags: int: Additional option flags to modify the data
        returned.Value is either 0 or combination of GET_META_DATA,
        GET_SIGNATURES, GET_SHARED_LIBRARY_FILES, MATCH_ALL,
        MATCH_DISABLED_COMPONENTS, MATCH_DISABLED_UNTIL_USED_COMPONENTS,
        MATCH_DEFAULT_ONLY, MATCH_DIRECT_BOOT_AWARE,
        MATCH_DIRECT_BOOT_UNAWARE, MATCH_SYSTEM_ONLY or
        MATCH_UNINSTALLED_PACKAGES.
        :return: ResolveInfo. Returns a ResolveInfo object containing the
        final service intent that was determined to be the best action.
        Returns null if no matching service was found.
        """
        pass

    def setApplicationCategoryHint(self, packageName, categoryHint):
        """
        Provide a hint of what the ApplicationInfo.category value should be
        for the given package.  This hint can only be set by the app which
        installed this package, as determined by
        getInstallerPackageName(String).
        :param packageName: String: the package to change the category hint
        for.This value must never be null.
        :param categoryHint: int: the category hint to set. Value is
        CATEGORY_UNDEFINED, CATEGORY_GAME, CATEGORY_AUDIO, CATEGORY_VIDEO,
        CATEGORY_IMAGE, CATEGORY_SOCIAL, CATEGORY_NEWS, CATEGORY_MAPS or
        CATEGORY_PRODUCTIVITY.
        """
        pass

    def setApplicationEnabledSetting(self, packageName, newState, flags):
        """
        Set the enabled setting for an application This setting will override
        any enabled state which may have been set by the application in its
        manifest.  It also overrides the enabled state set in the manifest for
        any of the application's components.  It does not override any enabled
        state set by setComponentEnabledSetting(ComponentName, int, int) for
        any of the application's components.
        :param packageName: String: The package name of the application to
        enable
        :param newState: int: The new enabled state for the application.Value
        is COMPONENT_ENABLED_STATE_DEFAULT, COMPONENT_ENABLED_STATE_ENABLED,
        COMPONENT_ENABLED_STATE_DISABLED,
        COMPONENT_ENABLED_STATE_DISABLED_USER or
        COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED.
        :param flags: int: Optional behavior flags. Value is either 0 or
        DONT_KILL_APP.
        """
        pass

    def setComponentEnabledSetting(self, componentName, newState, flags):
        """
        Set the enabled setting for a package component (activity, receiver,
        service, provider). This setting will override any enabled state which
        may have been set by the component in its manifest.
        :param componentName: ComponentName: The component to enable
        :param newState: int: The new enabled state for the component.Value is
        COMPONENT_ENABLED_STATE_DEFAULT, COMPONENT_ENABLED_STATE_ENABLED,
        COMPONENT_ENABLED_STATE_DISABLED,
        COMPONENT_ENABLED_STATE_DISABLED_USER or
        COMPONENT_ENABLED_STATE_DISABLED_UNTIL_USED.
        :param flags: int: Optional behavior flags. Value is either 0 or
        DONT_KILL_APP.
        """
        pass

    def setInstallerPackageName(self, targetPackage, installerPackageName):
        """
        Change the installer associated with a given package.  There are
        limitations on how the installer package can be changed; in
        particular: A SecurityException will be thrown if installerPackageName
        is not signed with the same certificate as the calling application. A
        SecurityException will be thrown if targetPackage already has an
        installer package, and that installer package is not signed with the
        same certificate as the calling application.
        :param targetPackage: String: The installed package whose installer
        will be changed.
        :param installerPackageName: String: The package name of the new
        installer.  May be null to clear the association.
        """
        pass

    def updateInstantAppCookie(self, cookie):
        """
        Updates the instant application cookie for the calling app. Non
        instant apps and apps that were instant but were upgraded to normal
        apps can still access this API. For instant apps this cookie is cached
        for some time after uninstall while for normal apps the cookie is
        deleted after the app is uninstalled. The cookie is always present
        while the app is installed. The cookie size is limited by
        getInstantAppCookieMaxBytes(). Passing null or an empty array clears
        the cookie.
        :param cookie: byte: The cookie data.This value may be null.
        :raises: IllegalArgumentExceptionif the array exceeds max cookie size.
        See also:
        isInstantApp()
        isInstantApp(String)
        getInstantAppCookieMaxBytes()
        getInstantAppCookie()
        clearInstantAppCookie()
        """
        pass

    def verifyPendingInstall(self, id, verificationCode):
        """
        Allows a package listening to the package verification broadcast to
        respond to the package manager. The response must include the
        verificationCode which is one of VERIFICATION_ALLOW or
        VERIFICATION_REJECT.
        :param id: int: pending package identifier as passed via the
        EXTRA_VERIFICATION_ID Intent extra.
        :param verificationCode: int: either VERIFICATION_ALLOW or
        VERIFICATION_REJECT.
        :raises: SecurityExceptionif the caller does not have the
        PACKAGE_VERIFICATION_AGENT permission.
        """
        pass
