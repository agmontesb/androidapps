# -*- coding: utf-8 -*-
# Ported from:
# https:# github.com/aosp-mirror/platform_frameworks_base/blob/master/libs/androidfw/include/androidfw/ResourceTypes.h

import io
from ctypes import *

from AconfigurationConst import *
from Android import AndroidEnum, Object, overload

def readResHeader(stream, headerClass, offset=None):
    if offset is not None:
        stream.seek(offset)
    x = headerClass()
    stream.readinto(x)
    return x


'''
/**
 * Macros for building/splitting resource identifiers.
 */
'''

Res_VALIDID = lambda resid: resid != 0
Res_CHECKID = lambda resid: (resid&0xFFFF0000) != 0
Res_MAKEID = lambda package, type, entry: (((package+1)<<24) | (((type+1)&0xFF)<<16) | (entry&0xFFFF))
Res_GETPACKAGE = lambda id: ((id>>24)-1)
Res_GETTYPE = lambda id: (((id>>16)&0xFF)-1)
Res_GETENTRY = lambda id: (id&0xFFFF)

Res_INTERNALID = lambda resid: ((resid&0xFFFF0000) != 0 and (resid&0xFF0000) == 0)
Res_MAKEINTERNAL = lambda entry: (0x01000000 | (entry&0xFFFF))
Res_MAKEARRAY = lambda entry: (0x02000000 | (entry&0xFFFF))

MAXPACKAGE = 255
Res_MAXTYPE = 255

'''
/** ********************************************************************
 *  Base Types
 *
 *  These are standard types that are shared between multiple specific
 *  resource types.
 *
 *********************************************************************** */
'''

class ResChunk_header(Structure):
    RES_NULL_TYPE               = 0x0000
    RES_STRING_POOL_TYPE        = 0x0001
    RES_TABLE_TYPE              = 0x0002
    RES_XML_TYPE                = 0x0003

    #  Chunk types in RES_XML_TYPE
    RES_XML_FIRST_CHUNK_TYPE    = 0x0100
    RES_XML_START_NAMESPACE_TYPE= 0x0100
    RES_XML_END_NAMESPACE_TYPE  = 0x0101
    RES_XML_START_ELEMENT_TYPE  = 0x0102
    RES_XML_END_ELEMENT_TYPE    = 0x0103
    RES_XML_CDATA_TYPE          = 0x0104
    RES_XML_LAST_CHUNK_TYPE     = 0x017f
    #  This contains a uint32_t array mapping strings in the string
    #  pool back to resource identifiers.  It is optional.
    RES_XML_RESOURCE_MAP_TYPE   = 0x0180

    #  Chunk types in RES_TABLE_TYPE
    RES_TABLE_PACKAGE_TYPE      = 0x0200
    RES_TABLE_TYPE_TYPE         = 0x0201
    RES_TABLE_TYPE_SPEC_TYPE    = 0x0202
    RES_TABLE_LIBRARY_TYPE      = 0x0203
    #
    # Header that appears at the front of every data chunk in a resource.
    #
    _fields_ = [
        #  Type identifier for this chunk.  The meaning of this value depends
        #  on the containing chunk.
        ('type', c_uint16),
        #  Size of the chunk header (in bytes).  Adding this value to
        #  the address of the chunk allows you to find its associated data
        #  (if any).
        ('headerSize', c_uint16),
        #  Total size of this chunk (in bytes).  This is the chunkSize plus
        #  the size of any data associated with the chunk.  Adding this value
        #  to the chunk allows you to completely skip its contents (including
        #  any child chunks).  If this value is the same as chunkSize, there is
        #  no data associated with the chunk.
        ('size', c_uint32)
    ]


'''
/** ********************************************************************
 *  RESOURCE TABLE
 *
 *********************************************************************** */
 '''

class ResTable_header(Structure):
    '''
     * Header for a resource table.  Its data contains a series of
     * additional chunks:
     *   * A ResStringPool_header containing all table values.  This string pool
     *     contains all of the string values in the entire resource table (not
     *     the names of entries or type identifiers however).
     *   * One or more ResTable_package chunks.
     *
     * Specific entries within a resource table can be uniquely identified
     * with a single integer as defined by the ResTable_ref structure.
    '''
    _fields_ = [
        ('header', ResChunk_header),
        # The number of ResTable_package structures.
        ('packageCount', c_uint32)
    ]

class ResTable_package(Structure):
    _fields_ = [
        ('header', ResChunk_header),
        #  If this is a base package, its ID.  Package IDs start
        #  at 1 (corresponding to the value of the package bits in a
        #  resource identifier).  0 means this is not a base package.
        ('id', c_uint32),
        # Actual name of this package, \0-terminated.
        ('name', 128*c_uint16),
        #  Offset to a ResStringPool_header defining the resource
        #  type symbol table.  If zero, this package is inheriting from
        #  another base package (overriding specific values in it).
        ('typeStrings', c_uint32),
        # Last index into typeStrings that is for public use by others.
        ('lastPublicType', c_uint32),
        #  Offset to a ResStringPool_header defining the resource
        #  key symbol table.  If zero, this package is inheriting from
        #  another base package (overriding specific values in it).
        ('keyStrings', c_uint32),
        # Last index into keyStrings that is for public use by others
        ('lastPublicKey', c_uint32),
        ('typeIdOffset', c_uint32),
    ]
    
#  The most specific locale can consist of:
# 
#  - a 3 char language code
#  - a 3 char region code prefixed by a 'r'
#  - a 4 char script code prefixed by a 's'
#  - a 8 char variant code prefixed by a 'v'
# 
#  each separated by a single char separator, which sums up to a total of 24
#  chars, (25 include the string terminator). Numbering system specificator,
#  if present, can add up to 14 bytes (-u-nu-xxxxxxxx), giving 39 bytes,
#  or 40 bytes to make it 4 bytes aligned.
RESTABLE_MAX_LOCALE_LEN = 40
 

class ResTable_config(Structure):
    '''
       Describes a particular resource configuration.
    '''

    ORIENTATION_ANY  = ACONFIGURATION_ORIENTATION_ANY
    ORIENTATION_PORT = ACONFIGURATION_ORIENTATION_PORT
    ORIENTATION_LAND = ACONFIGURATION_ORIENTATION_LAND
    ORIENTATION_SQUARE = ACONFIGURATION_ORIENTATION_SQUARE

    TOUCHSCREEN_ANY  = ACONFIGURATION_TOUCHSCREEN_ANY
    TOUCHSCREEN_NOTOUCH  = ACONFIGURATION_TOUCHSCREEN_NOTOUCH
    TOUCHSCREEN_STYLUS  = ACONFIGURATION_TOUCHSCREEN_STYLUS
    TOUCHSCREEN_FINGER  = ACONFIGURATION_TOUCHSCREEN_FINGER

    DENSITY_DEFAULT = ACONFIGURATION_DENSITY_DEFAULT
    DENSITY_LOW = ACONFIGURATION_DENSITY_LOW
    DENSITY_MEDIUM = ACONFIGURATION_DENSITY_MEDIUM
    DENSITY_TV = ACONFIGURATION_DENSITY_TV
    DENSITY_HIGH = ACONFIGURATION_DENSITY_HIGH
    DENSITY_XHIGH = ACONFIGURATION_DENSITY_XHIGH
    DENSITY_XXHIGH = ACONFIGURATION_DENSITY_XXHIGH
    DENSITY_XXXHIGH = ACONFIGURATION_DENSITY_XXXHIGH
    DENSITY_ANY = ACONFIGURATION_DENSITY_ANY
    DENSITY_NONE = ACONFIGURATION_DENSITY_NONE

    KEYBOARD_ANY  = ACONFIGURATION_KEYBOARD_ANY
    KEYBOARD_NOKEYS  = ACONFIGURATION_KEYBOARD_NOKEYS
    KEYBOARD_QWERTY  = ACONFIGURATION_KEYBOARD_QWERTY
    KEYBOARD_12KEY  = ACONFIGURATION_KEYBOARD_12KEY

    NAVIGATION_ANY  = ACONFIGURATION_NAVIGATION_ANY
    NAVIGATION_NONAV  = ACONFIGURATION_NAVIGATION_NONAV
    NAVIGATION_DPAD  = ACONFIGURATION_NAVIGATION_DPAD
    NAVIGATION_TRACKBALL  = ACONFIGURATION_NAVIGATION_TRACKBALL
    NAVIGATION_WHEEL  = ACONFIGURATION_NAVIGATION_WHEEL

    MASK_KEYSHIDDEN = 0x0003
    KEYSHIDDEN_ANY = ACONFIGURATION_KEYSHIDDEN_ANY
    KEYSHIDDEN_NO = ACONFIGURATION_KEYSHIDDEN_NO
    KEYSHIDDEN_YES = ACONFIGURATION_KEYSHIDDEN_YES
    KEYSHIDDEN_SOFT = ACONFIGURATION_KEYSHIDDEN_SOFT

    MASK_NAVHIDDEN = 0x000c
    SHIFT_NAVHIDDEN = 2
    NAVHIDDEN_ANY = ACONFIGURATION_NAVHIDDEN_ANY << SHIFT_NAVHIDDEN
    NAVHIDDEN_NO = ACONFIGURATION_NAVHIDDEN_NO << SHIFT_NAVHIDDEN
    NAVHIDDEN_YES = ACONFIGURATION_NAVHIDDEN_YES << SHIFT_NAVHIDDEN

    SCREENWIDTH_ANY = 0
    SCREENHEIGHT_ANY = 0
    SDKVERSION_ANY = 0
    MINORVERSION_ANY = 0

    MASK_SCREENSIZE = 0x0f
    SCREENSIZE_ANY = ACONFIGURATION_SCREENSIZE_ANY
    SCREENSIZE_SMALL = ACONFIGURATION_SCREENSIZE_SMALL
    SCREENSIZE_NORMAL = ACONFIGURATION_SCREENSIZE_NORMAL
    SCREENSIZE_LARGE = ACONFIGURATION_SCREENSIZE_LARGE
    SCREENSIZE_XLARGE = ACONFIGURATION_SCREENSIZE_XLARGE
    
    #  screenLayout bits for wide/long screen variation.
    MASK_SCREENLONG = 0x30
    SHIFT_SCREENLONG = 4
    SCREENLONG_ANY = ACONFIGURATION_SCREENLONG_ANY << SHIFT_SCREENLONG
    SCREENLONG_NO = ACONFIGURATION_SCREENLONG_NO << SHIFT_SCREENLONG
    SCREENLONG_YES = ACONFIGURATION_SCREENLONG_YES << SHIFT_SCREENLONG

    #  screenLayout bits for layout direction.
    MASK_LAYOUTDIR = 0xC0
    SHIFT_LAYOUTDIR = 6
    LAYOUTDIR_ANY = ACONFIGURATION_LAYOUTDIR_ANY << SHIFT_LAYOUTDIR
    LAYOUTDIR_LTR = ACONFIGURATION_LAYOUTDIR_LTR << SHIFT_LAYOUTDIR
    LAYOUTDIR_RTL = ACONFIGURATION_LAYOUTDIR_RTL << SHIFT_LAYOUTDIR
    #  uiMode bits for the mode type.
    MASK_UI_MODE_TYPE = 0x0f
    UI_MODE_TYPE_ANY = ACONFIGURATION_UI_MODE_TYPE_ANY
    UI_MODE_TYPE_NORMAL = ACONFIGURATION_UI_MODE_TYPE_NORMAL
    UI_MODE_TYPE_DESK = ACONFIGURATION_UI_MODE_TYPE_DESK
    UI_MODE_TYPE_CAR = ACONFIGURATION_UI_MODE_TYPE_CAR
    UI_MODE_TYPE_TELEVISION = ACONFIGURATION_UI_MODE_TYPE_TELEVISION
    UI_MODE_TYPE_APPLIANCE = ACONFIGURATION_UI_MODE_TYPE_APPLIANCE
    UI_MODE_TYPE_WATCH = ACONFIGURATION_UI_MODE_TYPE_WATCH
    UI_MODE_TYPE_VR_HEADSET = ACONFIGURATION_UI_MODE_TYPE_VR_HEADSET

    #  uiMode bits for the night switch.
    MASK_UI_MODE_NIGHT = 0x30
    SHIFT_UI_MODE_NIGHT = 4
    UI_MODE_NIGHT_ANY = ACONFIGURATION_UI_MODE_NIGHT_ANY << SHIFT_UI_MODE_NIGHT
    UI_MODE_NIGHT_NO = ACONFIGURATION_UI_MODE_NIGHT_NO << SHIFT_UI_MODE_NIGHT
    UI_MODE_NIGHT_YES = ACONFIGURATION_UI_MODE_NIGHT_YES << SHIFT_UI_MODE_NIGHT
    #  screenLayout2 bits for round/notround.
    MASK_SCREENROUND = 0x03
    SCREENROUND_ANY = ACONFIGURATION_SCREENROUND_ANY
    SCREENROUND_NO = ACONFIGURATION_SCREENROUND_NO
    SCREENROUND_YES = ACONFIGURATION_SCREENROUND_YES
    #  colorMode bits for wide-color gamut/narrow-color gamut.
    MASK_WIDE_COLOR_GAMUT = 0x03
    WIDE_COLOR_GAMUT_ANY = ACONFIGURATION_WIDE_COLOR_GAMUT_ANY
    WIDE_COLOR_GAMUT_NO = ACONFIGURATION_WIDE_COLOR_GAMUT_NO
    WIDE_COLOR_GAMUT_YES = ACONFIGURATION_WIDE_COLOR_GAMUT_YES

    #  colorMode bits for HDR/LDR.
    MASK_HDR = 0x0c
    SHIFT_COLOR_MODE_HDR = 2
    HDR_ANY = ACONFIGURATION_HDR_ANY << SHIFT_COLOR_MODE_HDR
    HDR_NO = ACONFIGURATION_HDR_NO << SHIFT_COLOR_MODE_HDR
    HDR_YES = ACONFIGURATION_HDR_YES << SHIFT_COLOR_MODE_HDR
    
    #  Flags indicating a set of config values.  These flag constants must
    #  match the corresponding ones in android.content.pm.ActivityInfo and
    #  attrs_manifest.xml.
    CONFIG_MCC = ACONFIGURATION_MCC
    CONFIG_MNC = ACONFIGURATION_MNC
    CONFIG_LOCALE = ACONFIGURATION_LOCALE
    CONFIG_TOUCHSCREEN = ACONFIGURATION_TOUCHSCREEN
    CONFIG_KEYBOARD = ACONFIGURATION_KEYBOARD
    CONFIG_KEYBOARD_HIDDEN = ACONFIGURATION_KEYBOARD_HIDDEN
    CONFIG_NAVIGATION = ACONFIGURATION_NAVIGATION
    CONFIG_ORIENTATION = ACONFIGURATION_ORIENTATION
    CONFIG_DENSITY = ACONFIGURATION_DENSITY
    CONFIG_SCREEN_SIZE = ACONFIGURATION_SCREEN_SIZE
    CONFIG_SMALLEST_SCREEN_SIZE = ACONFIGURATION_SMALLEST_SCREEN_SIZE
    CONFIG_VERSION = ACONFIGURATION_VERSION
    CONFIG_SCREEN_LAYOUT = ACONFIGURATION_SCREEN_LAYOUT
    CONFIG_UI_MODE = ACONFIGURATION_UI_MODE
    CONFIG_LAYOUTDIR = ACONFIGURATION_LAYOUTDIR
    CONFIG_SCREEN_ROUND = ACONFIGURATION_SCREEN_ROUND
    CONFIG_COLOR_MODE = ACONFIGURATION_COLOR_MODE

    _fields_ = [
        ('size', c_uint32),
        ('union1', type('Union1', (Union,), {'_fields_':[
            ('field1', type('Imsi', (Structure,), {'_fields_': [
                #  Mobile country code (from SIM).  0 means "any".
                ('mcc', c_uint16),
                #  Mobile network code (from SIM).  0 means "any".
                ('mnc', c_uint16)
            ]})),
            ('imsi', c_uint32)]})),
        ('union2', type('Union2', (Union,), {'_fields_': [
            ('field1', type('Locale', (Structure,), {'_fields_': [
                #  This field can take three different forms:
                #  - \0\0 means "any".
                #
                #  - Two 7 bit ascii values interpreted as ISO-639-1 language
                #    codes ('fr', 'en' etc. etc.). The high bit for both bytes is
                #    zero.
                #
                #  - A single 16 bit little endian packed value representing an
                #    ISO-639-2 3 letter language code. This will be of the form:
                #
                #    {1, t, t, t, t, t, s, s, s, s, s, f, f, f, f, f}
                #
                #    bit[0, 4] = first letter of the language code
                #    bit[5, 9] = second letter of the language code
                #    bit[10, 14] = third letter of the language code.
                #    bit[15] = 1 always
                #
                #  For backwards compatibility, languages that have unambiguous
                #  two letter codes are represented in that format.
                #
                #  The layout is always bigendian irrespective of the runtime
                #  architecture.
                ('language', (2*c_char)),
                #  This field can take three different forms:
                #  - \0\0 means "any".
                #
                #  - Two 7 bit ascii values interpreted as 2 letter region
                #    codes ('US', 'GB' etc.). The high bit for both bytes is zero.
                #
                #  - An UN M.49 3 digit region code. For simplicity, these are packed
                #    in the same manner as the language codes, though we should need
                #    only 10 bits to represent them, instead of the 15.
                #
                #  The layout is always bigendian irrespective of the runtime
                #  architecture.
                ('country', (2*c_char))
            ]})),
            ('locale', c_uint32)]})),
        ('union3', type('Union3', (Union,), {'_fields_': [
            ('field1', type('ScreenType', (Structure,), {'_fields_': [
                ('orientation', c_uint8),
                ('touchscreen', c_uint8),
                ('density', c_uint16),
            ]})),
            ('screenType', c_uint32)]})),
        ('union4', type('Union4', (Union,), {'_fields_': [
            ('field1', type('Input', (Structure,), {'_fields_': [
                ('keyboard', c_uint8),
                ('navigation', c_uint8),
                ('inputFlags', c_uint8),
                ('inputPad0', c_uint8),
            ]})),
            ('input', c_uint32)]})),
        ('union5', type('Union5', (Union,), {'_fields_': [
            ('field1', type('ScreenSize', (Structure,), {'_fields_': [
                ('screenWidth', c_uint16),
                ('screenHeight', c_uint16),
            ]})),
            ('screenSize', c_uint32)]})),
        ('union6', type('Union6', (Union,), {'_fields_': [
            ('field1', type('Version', (Structure,), {'_fields_': [
                ('sdkVersion', c_uint16),
                #  For now minorVersion must always be 0!!!  Its meaning
                #  is currently undefined.
                ('minorVersion', c_uint16),
            ]})),
            ('version', c_uint32)]})),
        ('union7', type('Union7', (Union,), {'_fields_': [
            ('field1', type('ScreenConfig', (Structure,), {'_fields_': [
                ('screenLayout', c_uint8),
                ('uiMode', c_uint8),
                ('smallestScreenWidthDp', c_uint16),
            ]})),
            ('screenConfig', c_uint32)]})),
        ('union8', type('Union8', (Union,), {'_fields_': [
            ('field1', type('ScreenSizeDp', (Structure,), {'_fields_': [
                ('screenWidthDp', c_uint16),
                ('screenHeightDp', c_uint16),
            ]})),
            ('screenSizeDp', c_uint32)]})),
        #  The ISO-15924 short name for the script corresponding to this
        #  configuration. (eg. Hant, Latn, etc.). Interpreted in conjunction with
        #  the locale field.
        ('localeScript', (4*c_char)),
        #  A single BCP-47 variant subtag. Will vary in length between 4 and 8
        #  chars. Interpreted in conjunction with the locale field.
        ('localeVariant', (8*c_char)),
        ('union9', type('Union9', (Union,), {'_fields_': [
            ('field1', type('ScreenConfig2', (Structure,), {'_fields_': [
                ('screenLayout2', c_uint8),     #  Contains round/notround qualifier.
                ('colorMode', c_uint8),         #  Wide-gamut, HDR, etc.
                ('screenConfigPad2', c_uint16), #  Reserved padding.
            ]})),
            ('screenConfig2', c_uint32)]})),
        #  If false and localeScript is set, it means that the script of the locale
        #  was explicitly provided.
        #
        #  If true, it means that localeScript was automatically computed.
        #  localeScript may still not be set in this case, which means that we
        #  tried but could not compute a script.
        ('localeScriptWasComputed', c_bool),
        #  The value of BCP 47 Unicode extension for key 'nu' (numbering system).
        #  Varies in length from 3 to 8 chars. Zero-filled value.
        ('localeNumberingSystem', (8*c_char)),
    ]

    def __getattr__(self, name):
        fieldMap = {
            'mcc': self.union1.field1, 'mnc': self.union1.field1, 'imsi': self.union1,
            'language': self.union2.field1, 'country': self.union2.field1, 'locale': self.union2,
            'orientation': self.union3.field1, 'touchscreen': self.union3.field1, 'density': self.union3.field1, 'screenType': self.union3,
            'keyboard': self.union4.field1, 'navigation': self.union4.field1, 'inputFlags': self.union4.field1, 'inputPad0': self.union4.field1, 'input': self.union4,
            'screenWidth': self.union5.field1, 'screenHeight': self.union5.field1, 'screenSize': self.union5,
            'sdkVersion': self.union6.field1, 'minorVersion': self.union6.field1, 'version': self.union6,
            'screenLayout': self.union7.field1, 'uiMode': self.union7.field1, 'smallestScreenWidthDp': self.union7.field1, 'screenConfig': self.union7,
            'screenWidthDp': self.union8.field1, 'screenHeightDp': self.union8.field1, 'screenSizeDp': self.union8,
            'screenLayout2': self.union9.field1, 'colorMode': self.union9.field1, 'screenConfigPad2': self.union9.field1, 'screenConfig2': self.union9,
        }
        obj = fieldMap.get(name)
        if not obj:
            errMsg = "'%s' object has no attribute '%s'"  % ('ResTable_config', name)
            raise AttributeError(errMsg)
        return getattr(obj, name)


class ResTable_typeSpec(Structure):
    '''
     * A specification of the resources defined by a particular type.
     *
     * There should be one of these chunks for each resource type.
     *
     * This structure is followed by an array of integers providing the set of
     * configuration change flags (ResTable_config::CONFIG_*) that have multiple
     * resources for that configuration.  In addition, the high bit is set if that
     * resource has been made public.
    '''
    
    # Additional flag indicating an entry is public.
    SPEC_PUBLIC = c_uint32(0x40000000)
    # Additional flag indicating an entry is overlayable at runtime.
    # Added in Android-P.
    SPEC_OVERLAYABLE = c_uint32(0x80000000)

    _fields_ = [
        ('header', ResChunk_header),
        #  The type identifier this chunk is holding.  Type IDs start
        #  at 1 (corresponding to the value of the type bits in a
        #  resource identifier).  0 is invalid.
        ('id', c_uint8),
        # Must be 0.
        ('res0', c_uint8),
        # Must be 0.
        ('res1', c_uint16),
        # Number of uint32_t entry configuration masks that follow.
        ('entryCount', c_uint32),
    ]

class ResTable_type(Structure):
    '''
     * A collection of resource entries for a particular resource data
     * type.
     *
     * If the flag FLAG_SPARSE is not set in `flags`, then this struct is
     * followed by an array of uint32_t defining the resource
     * values, corresponding to the array of type strings in the
     * ResTable_package::typeStrings string block. Each of these hold an
     * index from entriesStart; a value of NO_ENTRY means that entry is
     * not defined.
     *
     * If the flag FLAG_SPARSE is set in `flags`, then this struct is followed
     * by an array of ResTable_sparseTypeEntry defining only the entries that
     * have values for this type. Each entry is sorted by their entry ID such
     * that a binary search can be performed over the entries. The ID and offset
     * are encoded in a uint32_t. See ResTabe_sparseTypeEntry.
     *
     * There may be multiple of these chunks for a particular resource type,
     * supply different configuration variations for the resource values of
     * that type.
     *
     * It would be nice to have an additional ordered index of entries, so
     * we can do a binary search if trying to find a resource by string name.
    '''
    NO_ENTRY = 0xFFFFFFFF
    #  If set, the entry is sparse, and encodes both the entry ID and offset into each entry,
    #  and a binary search is used to find the key. Only available on platforms >= O.
    #  Mark any types that use this with a v26 qualifier to prevent runtime issues on older
    #  platforms.
    FLAG_SPARSE = 0x01

    _fields_ = [
        ('header', ResChunk_header),
        #  The type identifier this chunk is holding.  Type IDs start
        #  at 1 (corresponding to the value of the type bits in a
        #  resource identifier).  0 is invalid.
        ('id', c_uint8),
        ('flags', c_uint8),
        #  Must be 0.
        ('reserved', c_uint16),
        #  Number of uint32_t entry indices that follow.
        ('entryCount', c_uint32),
        #  Offset from header where ResTable_entry data starts.
        ('entriesStart', c_uint32),
        #  Configuration this collection of entries is designed for. This must always be last.
        ('config', ResTable_config),
    ]

#  The minimum size required to read any version of ResTable_type.
kResTableTypeMinSize = sizeof(ResTable_type) - sizeof(ResTable_config) + ResTable_config.size.size

#  Assert that the ResTable_config is always the last field. This poses a problem for extending
#  ResTable_type in the future, as ResTable_config is variable (over different releases).
assert sizeof(ResTable_type) == ResTable_type.config.offset + sizeof(ResTable_config), \
              "ResTable_config must be last field in ResTable_type"

class ResTable_sparseTypeEntry(Union):
    '''
     * An entry in a ResTable_type with the flag `FLAG_SPARSE` set.
    '''
    _fields_ = [
        #  Holds the raw uint32_t encoded value. Do not read this.
        ('entry', c_uint32),
        #  The offset from ResTable_type::entriesStart, divided by 4.
        ('field2', type('ScreenConfig2', (Structure,), {'_fields_': [
                ('idx', c_uint16),     #  The index of the entry.
                ('offset', c_uint16),  #  The offset from ResTable_type.entriesStart, divided by 4.
            ]})),
    ]

    def __getattr__(self, name):
        fieldMap = {
            'idx': self.field2, 'offset': self.field2,
        }
        obj = fieldMap.get(name)
        if not obj:
            errMsg = "'%s' object has no attribute '%s'"  % ('ResTable_sparseTypeEntry', name)
            raise AttributeError(errMsg)
        return getattr(obj, name)

assert sizeof(ResTable_sparseTypeEntry) == sizeof(c_uint32), \
       "ResTable_sparseTypeEntry must be 4 bytes in size"

class ResStringPool_ref(Structure):
    # Reference to a string in a string pool.
    _fields_ = [
        # Index into the string pool table (uint32_t-offset from the indices
        # immediately after ResStringPool_header) at which to find the location
        # of the string data in the pool.
        ('index', c_uint32)
    ]


class ResTable_entry(Structure):
    '''
     * This is the beginning of information about an entry in the resource
     * table.  It holds the reference to the name of this entry, and is
     * immediately followed by one of:
     *   * A Res_value structure, if FLAG_COMPLEX is -not- set.
     *   * An array of ResTable_map structures, if FLAG_COMPLEX is set.
     *     These supply a set of name/value mappings of data.
    '''
    # ** Flags **
    #  If set, this is a complex entry, holding a set of name/value
    #  mappings.  It is followed by an array of ResTable_map structures.
    FLAG_COMPLEX = 0x0001
    #  If set, this resource has been declared public, so libraries
    #  are allowed to reference it.
    FLAG_PUBLIC = 0x0002
    #  If set, this is a weak resource and may be overriden by strong
    #  resources of the same name/type. This is only useful during
    #  linking with other resource tables.
    FLAG_WEAK = 0x0004

    _fields_ = [
        ('size', c_uint16),         # Number of bytes in this structure.
        ('flags', c_uint16),        # Flags
        ('key', ResStringPool_ref)  # Reference into ResTable_package.keyStrings
                                    # identifying this entry.
    ]


class ResTable_ref(Structure):
    #
    #  This is a reference to a unique entry (a ResTable_entry structure)
    #  in a resource table.  The value is structured as: 0xpptteeee,
    #  where pp is the package index, tt is the type index in that
    #  package, and eeee is the entry index in that type.  The package
    #  and type values start at 1 for the first item, to help catch cases
    #  where they have not been supplied.
    #
    _fields_ = [
        ('ident', c_uint32)
    ]


class ResTable_map_entry(Structure):
    '''
     * Extended form of a ResTable_entry for map entries, defining a parent map
     * resource from which to inherit values.
    '''
    _fields_ = [
        #  Resource identifier of the parent mapping, or 0 if there is none.
        #  This is always treated as a TYPE_DYNAMIC_REFERENCE.
        ('parent', ResTable_ref),
        #  Number of name/value pairs that follow for FLAG_COMPLEX.
        ('count', c_uint32),
    ]


class Res_value(Structure):
    #  The 'data' is either 0 or 1, specifying this resource is either
    #  undefined or empty respectively.
    TYPE_NULL = 0x00
    #  The 'data' holds a ResTable_ref, a reference to another resource
    #  table entry.
    TYPE_REFERENCE = 0x01
    #  The 'data' holds an attribute resource identifier.
    TYPE_ATTRIBUTE = 0x02
    #  The 'data' holds an index into the containing resource table's
    #  global value string pool.
    TYPE_STRING = 0x03
    #  The 'data' holds a single-precision floating point number.
    TYPE_FLOAT = 0x04
    #  The 'data' holds a complex number encoding a dimension value,
    #  such as "100in".
    TYPE_DIMENSION = 0x05
    #  The 'data' holds a complex number encoding a fraction of a
    #  container.
    TYPE_FRACTION = 0x06
    #  The 'data' holds a dynamic ResTable_ref, which needs to be
    #  resolved before it can be used like a TYPE_REFERENCE.
    TYPE_DYNAMIC_REFERENCE = 0x07
    #  The 'data' holds an attribute resource identifier, which needs to be resolved
    #  before it can be used like a TYPE_ATTRIBUTE.
    TYPE_DYNAMIC_ATTRIBUTE = 0x08

    #  Beginning of integer flavors...
    TYPE_FIRST_INT = 0x10

    #  The 'data' is a raw integer value of the form n..n.
    TYPE_INT_DEC = 0x10
    #  The 'data' is a raw integer value of the form 0xn..n.
    TYPE_INT_HEX = 0x11
    #  The 'data' is either 0 or 1, for input "false" or "true" respectively.
    TYPE_INT_BOOLEAN = 0x12

    #  Beginning of color integer flavors...
    TYPE_FIRST_COLOR_INT = 0x1c

    #  The 'data' is a raw integer value of the form #aarrggbb.
    TYPE_INT_COLOR_ARGB8 = 0x1c
    #  The 'data' is a raw integer value of the form #rrggbb.
    TYPE_INT_COLOR_RGB8 = 0x1d
    #  The 'data' is a raw integer value of the form #argb.
    TYPE_INT_COLOR_ARGB4 = 0x1e
    #  The 'data' is a raw integer value of the form #rgb.
    TYPE_INT_COLOR_RGB4 = 0x1f

    #  ...end of integer flavors.
    TYPE_LAST_COLOR_INT = 0x1f

    #  ...end of integer flavors.
    TYPE_LAST_INT = 0x1f

    #  Structure of complex data values (TYPE_UNIT and TYPE_FRACTION)
    #  Where the unit type information is.  This gives us 16 possible
    #  types, as defined below.
    COMPLEX_UNIT_SHIFT = 0
    COMPLEX_UNIT_MASK = 0xf

    #  TYPE_DIMENSION: Value is raw pixels.
    COMPLEX_UNIT_PX = 0
    #  TYPE_DIMENSION: Value is Device Independent Pixels.
    COMPLEX_UNIT_DIP = 1
    #  TYPE_DIMENSION: Value is a Scaled device independent Pixels.
    COMPLEX_UNIT_SP = 2
    #  TYPE_DIMENSION: Value is in points.
    COMPLEX_UNIT_PT = 3
    #  TYPE_DIMENSION: Value is in inches.
    COMPLEX_UNIT_IN = 4
    #  TYPE_DIMENSION: Value is in millimeters.
    COMPLEX_UNIT_MM = 5

    #  TYPE_FRACTION: A basic fraction of the overall size.
    COMPLEX_UNIT_FRACTION = 0
    #  TYPE_FRACTION: A fraction of the parent size.
    COMPLEX_UNIT_FRACTION_PARENT = 1

    #  Where the radix information is, telling where the decimal place
    #  appears in the mantissa.  This give us 4 possible fixed point
    #  representations as defined below.
    COMPLEX_RADIX_SHIFT = 4
    COMPLEX_RADIX_MASK = 0x3

    #  The mantissa is an integral number -- i.e., 0xnnnnnn.0
    COMPLEX_RADIX_23p0 = 0
    #  The mantissa magnitude is 16 bits -- i.e, 0xnnnn.nn
    COMPLEX_RADIX_16p7 = 1
    #  The mantissa magnitude is 8 bits -- i.e, 0xnn.nnnn
    COMPLEX_RADIX_8p15 = 2
    #  The mantissa magnitude is 0 bits -- i.e, 0x0.nnnnnn
    COMPLEX_RADIX_0p23 = 3

    #  Where the actual value is.  This gives us 23 bits of
    #  precision.  The top bit is the sign.
    COMPLEX_MANTISSA_SHIFT = 8
    COMPLEX_MANTISSA_MASK = 0xffffff

    #  Possible data values for TYPE_NULL.
    #  The value is not defined.
    DATA_NULL_UNDEFINED = 0
    #  The value is explicitly defined as empty.
    DATA_NULL_EMPTY = 1

    _fields_ = [
        # Number of bytes in this structure.
        ('size', c_uint16),
        # Always set to 0.
        ('res0', c_uint8),
        # Type of the data value.
        ('dataType', c_uint8),
        # The data for this item, as interpreted according to dataType.
        ('data', c_uint32)
    ]


class ResTable_map(Structure):
    '''
     * A single name/value mapping that is part of a complex resource
     * entry.
    '''

    #  Special values for 'name' when defining attribute resources.
    #  This entry holds the attribute's type code.
    ATTR_TYPE = Res_MAKEINTERNAL(0)

    #  For integral attributes, this is the minimum value it can hold.
    ATTR_MIN = Res_MAKEINTERNAL(1)

    #  For integral attributes, this is the maximum value it can hold.
    ATTR_MAX = Res_MAKEINTERNAL(2)

    #  Localization of this resource is can be encouraged or required with
    #  an aapt flag if this is set
    ATTR_L10N = Res_MAKEINTERNAL(3)

    #  for plural support, see android.content.res.PluralRules#attrForQuantity(int)
    ATTR_OTHER = Res_MAKEINTERNAL(4)
    ATTR_ZERO = Res_MAKEINTERNAL(5)
    ATTR_ONE = Res_MAKEINTERNAL(6)
    ATTR_TWO = Res_MAKEINTERNAL(7)
    ATTR_FEW = Res_MAKEINTERNAL(8)
    ATTR_MANY = Res_MAKEINTERNAL(9)

    #  Bit mask of allowed types, for use with ATTR_TYPE.
    #  No type has been defined for this attribute, use generic
    #  type handling.  The low 16 bits are for types that can be
    #  handled generically; the upper 16 require additional information
    #  in the bag so can not be handled generically for TYPE_ANY.
    TYPE_ANY = 0x0000FFFF

    #  Attribute holds a references to another resource.
    TYPE_REFERENCE = 1<<0

    #  Attribute holds a generic string.
    TYPE_STRING = 1<<1

    #  Attribute holds an integer value.  ATTR_MIN and ATTR_MIN can
    #  optionally specify a constrained range of possible integer values.
    TYPE_INTEGER = 1<<2

    #  Attribute holds a boolean integer.
    TYPE_BOOLEAN = 1<<3

    #  Attribute holds a color value.
    TYPE_COLOR = 1<<4

    #  Attribute holds a floating point value.
    TYPE_FLOAT = 1<<5

    #  Attribute holds a dimension value, such as "20px".
    TYPE_DIMENSION = 1<<6

    #  Attribute holds a fraction value, such as "20%".
    TYPE_FRACTION = 1<<7

    #  Attribute holds an enumeration.  The enumeration values are
    #  supplied as additional entries in the map.
    TYPE_ENUM = 1<<16

    #  Attribute holds a bitmaks of flags.  The flag bit values are
    #  supplied as additional entries in the map.
    TYPE_FLAGS = 1<<17

    #  Enum of localization modes, for use with ATTR_L10N.
    L10N_NOT_REQUIRED = 0
    L10N_SUGGESTED    = 1

    _fields_ = [
        #  The resource identifier defining this mapping's name.  For attribute
        #  resources, 'name' can be one of the following special resource types
        #  to supply meta-data about the attribute; for all other resource types
        #  it must be an attribute resource.
        ('name', ResTable_ref),
        #  This mapping's value.
        ('value', Res_value),
    ]


class ResTable_lib_header(Structure):
    '''
     * A package-id to package name mapping for any shared libraries used
     * in this resource table. The package-id's encoded in this resource
     * table may be different than the id's assigned at runtime. We must
     * be able to translate the package-id's based on the package name.
     '''
    _fields_ = [
        ('header', ResChunk_header),
        #  The number of shared libraries linked in this resource table.
        ('count', c_uint32),
    ]


class ResTable_lib_entry(Structure):
    '''
     * A shared library package-id to package name entry.
    '''
    _fields_ = [
        #  The package-id this shared library was assigned at build time.
        #  We use a uint32 to keep the structure aligned on a uint32 boundary.
        ('packageId', c_uint32),
        #  The package name of the shared library. \0 terminated.
        ('packageName', (128*c_uint16)),
    ]


'''
/** ********************************************************************
 *  String Pool
 *
 *  A set of strings that can be references by others through a
 *  ResStringPool_ref.
 *
 *********************************************************************** */
/**
 * Definition for a pool of strings.  The data of this chunk is an
 * array of uint32_t providing indices into the pool, relative to
 * stringsStart.  At stringsStart are all of the UTF-16 strings
 * concatenated together; each starts with a uint16_t of the string's
 * length and each ends with a 0x0000 terminator.  If a string is >
 * 32767 characters, the high bit of the length is set meaning to take
 * those 15 bits as a high word and it will be followed by another
 * uint16_t containing the low word.
 *
 * If styleCount is not zero, then immediately following the array of
 * uint32_t indices into the string table is another array of indices
 * into a style table starting at stylesStart.  Each entry in the
 * style table is an array of ResStringPool_span structures.
 */
'''

class ResStringPool_header(Structure):
    #  **Values for field flags**
    #  If set, the string index is sorted by the string values (based
    #  on strcmp16()).
    SORTED_FLAG = 1<<0
    #  String pool is encoded in UTF-8
    UTF8_FLAG = 1<<8

    _fields_ = [
        ('header', ResChunk_header),
        # Number of strings in this pool (number of uint32_t indices that follow
        # in the data).
        ('stringCount', c_uint32),
        # Number of style span arrays in the pool (number of uint32_t indices
        # follow the string indices).
        ('styleCount', c_uint32),
        # Flags.
        ('flags', c_uint32),
        # Index from header of the string data.
        ('stringsStart', c_uint32),
        # Index from header of the style data.
        ('stylesStart', c_uint32)
    ]

    def __str__(self):
        answ = 'ResStringPool_header{'
        answ += 'type=%s, ' % self.header.type
        answ += 'headerSize=%s, ' % self.header.headerSize
        answ += 'size=%s, ' % self.header.size
        answ += 'stringCount=%s, ' % self.stringCount
        answ += 'styleCount=%s, ' % self.styleCount
        answ += 'flags=%s, ' % hex(self.flags)
        answ += 'stringsStart=%s, ' % self.stringsStart
        answ += 'stylesStart=%s' % self.stylesStart
        answ += '}'
        return answ


class ResStringPool_span(Structure):
    # This structure defines a span of style information associated with
    # a string in the pool.
    END = 0xFFFFFFFF
    _fields_ = [
        #  This is the name of the span -- that is, the name of the XML
        #  tag that defined it.  The special value END (0xFFFFFFFF) indicates
        #  the end of an array of spans.
        ('name', ResStringPool_ref),
        # The range of characters in the string that this span applies to.
        ('firstChar', c_uint32),
        ('lastChar', c_uint32),
    ]


class ResStringPool(object):
    #
    # Convenience class for accessing data in a ResStringPool resource.
    #
    def __init__(self, data=None, offset=None):
        headeroffset = offset or data.tell()
        rsph = readResHeader(data, ResStringPool_header, offset=headeroffset)
        assert rsph.header.type == 1
        self.resStringPoolheader = rsph
        self.strData = strData = []
        offsets = ((rsph.stringCount + rsph.styleCount)*c_uint32)()
        assert sizeof(offsets) == data.readinto(offsets)
        cint16 = c_uint16()
        if rsph.stringCount:
            encoding = 'UTF-8' if rsph.flags & rsph.UTF8_FLAG else 'UTF-16'
            stroffset = headeroffset + rsph.stringsStart
            data.seek(stroffset)
            for indx in range(rsph.stringCount):
                data.seek(stroffset + offsets[indx])
                # if indx == 1158:
                #     pass
                if encoding == 'UTF-8':
                    hbyte = readResHeader(data, c_uint8).value
                    strlen = readResHeader(data, c_uint8).value
                    if hbyte & 0x80:
                        hbyte = readResHeader(data, c_uint8).value
                        strlen = readResHeader(data, c_uint8).value
                        strlen = ((hbyte & 0x7f) << 8) | strlen
                    if hbyte < 0x80 and strlen & 0x80:
                        strlen = (strlen & 0x7f) << 8 | readResHeader(data, c_uint8).value
                        # strlen -= 1
                        # lbyte = readResHeader(data, c_uint8).value
                    strlen += 1
                else:
                    strlen = readResHeader(data, c_uint16).value
                    if strlen & 0x8000:
                        strlen = ((strlen & 0x7fff) << 16) | readResHeader(data, c_uint16).value
                    strlen = 2*(strlen + 1)
                char_array = readResHeader(data, (strlen * c_char))
                try:
                    strData.append(char_array.raw.decode(encoding)[:-1])
                except:
                    data.seek(stroffset + offsets[indx])
                    dmy = (4 * c_uint8)()
                    data.readinto(dmy)
                    dmy = (4*'{:0>2x} ').format(*dmy)
                    soff = 'ERROR: 0x{:0>8x} '.format(stroffset + offsets[indx])
                    fmt = soff + dmy + \
                          'len=0x{:0>4x} '.format(offsets[indx+1] - offsets[indx] - 4) + \
                        'strlen=0x{:0>4x} '.format(strlen)
                    strData.append(fmt)
        assert data.tell() <= headeroffset + rsph.header.size
        self.styleSpans = []
        if rsph.styleCount:
            dataSize = rsph.styleCount * sizeof(ResStringPool_span)
            dataReaded = 0
            data.seek(headeroffset + rsph.stylesStart)
            while dataReaded < dataSize:
                x = ResStringPool_span()
                dataReaded += data.readinto(x)
                self.styleSpans.append(x)
        assert data.tell() <= headeroffset + rsph.header.size

    def stringCount(self):
        return self.resStringPoolheader.stringCount

    def stringAt(self, indx):
        if hasattr(indx, 'index'):
            indx = indx.index
        try:
            return self.strData[indx]
        except:
            pass

    def styleCount(self):
        return self.resStringPoolheader.styleCount

    def styleAt(self, indx):
        try:
            return self.styleSpans[indx]
        except:
            pass

    def flags(self):
        return self.resStringPoolheader.flags

    def isSorted(self):
        return self.flags() & ResStringPool_header.SORTED_FLAG

    def isUTF8(self):
        return self.flags() & ResStringPool_header.UTF8_FLAG





'''
/** ********************************************************************
 *  XML Tree
 *
 *  Binary representation of an XML document.  This is designed to
 *  express everything in an XML document, in a form that is much
 *  easier to parse on the device.
 *
 *********************************************************************** */
'''

class ResXMLTree_header(Structure):
    '''
     * XML tree header.  This appears at the front of an XML tree,
     * describing its content.  It is followed by a flat array of
     * ResXMLTree_node structures; the hierarchy of the XML document
     * is described by the occurrance of RES_XML_START_ELEMENT_TYPE
     * and corresponding RES_XML_END_ELEMENT_TYPE nodes in the array.
    '''
    _fields_ = [
        ('header', ResChunk_header),
    ]


class ResXMLTree_node(Structure):
    '''
     * Basic XML tree node.  A single item in the XML document.  Extended info
     * about the node can be found after header.headerSize.
    '''
    _fields_ = [
        ('header', ResChunk_header),
        #  Line number in original source file at which this element appeared.
        ('lineNumber', c_uint32),
        #  Optional XML comment that was associated with this element -1 if none.
        ('comment', ResStringPool_ref),
    ]


class ResXMLTree_cdataExt(Structure):
    '''
     * Extended XML tree node for CDATA tags -- includes the CDATA string.
     * Appears header.headerSize bytes after a ResXMLTree_node.
    '''
    _fields_ = [
        #  The raw CDATA character data.
        ('data', ResStringPool_ref),
        #  The typed value of the character data if this is a CDATA node.
        ('typedData', Res_value),
    ]
    
class ResXMLTree_namespaceExt(Structure):
    '''
     * Extended XML tree node for namespace start/end nodes.
     * Appears header.headerSize bytes after a ResXMLTree_node.
    '''
    _fields_ = [
        #  The prefix of the namespace.
        ('prefix', ResStringPool_ref),  
        #  The URI of the namespace.
        ('uri', ResStringPool_ref)  
    ]
    

class ResXMLTree_endElementExt(Structure):
    '''
     * Extended XML tree node for element start/end nodes.
     * Appears header.headerSize bytes after a ResXMLTree_node.
    '''
    _fields_ = [
        #  String of the full namespace of this element.
        ('ns', ResStringPool_ref),
        #  String name of this node if it is an ELEMENT the raw
        #  character data if this is a CDATA node.
        ('name', ResStringPool_ref),  
    ]

class ResXMLTree_attrExt(Structure):
    '''
     * Extended XML tree node for start tags -- includes attribute
     * information.
     * Appears header.headerSize bytes after a ResXMLTree_node.
    '''
    _fields_ = [
        #  String of the full namespace of this element.
        ('ns', ResStringPool_ref),  
        #  String name of this node if it is an ELEMENT the raw
        #  character data if this is a CDATA node.
        ('name', ResStringPool_ref),  
        #  Byte offset from the start of this structure where the attributes start.
        ('attributeStart', c_uint16),
        #  Size of the ResXMLTree_attribute structures that follow.
        ('attributeSize', c_uint16), 
        #  Number of attributes associated with an ELEMENT.  These are
        #  available as an array of ResXMLTree_attribute structures
        #  immediately following this node.
        ('attributeCount', c_uint16), 
        #  Index (1-based) of the "id" attribute. 0 if none.
        ('idIndex', c_uint16), 
        #  Index (1-based) of the "class" attribute. 0 if none.
        ('classIndex', c_uint16), 
        #  Index (1-based) of the "style" attribute. 0 if none.
        ('styleIndex', c_uint16), 
    ]


class ResXMLTree_attribute(Structure):
    _fields_ = [
        #  Namespace of this attribute.
        ('ns', ResStringPool_ref),
        #  Name of this attribute.
        ('name', ResStringPool_ref),
        #  The original raw string value of this attribute.
        ('rawValue', ResStringPool_ref),
        #  Processesd typed value of this attribute.
        ('typedValue', Res_value),
    ]

