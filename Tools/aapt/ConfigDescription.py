# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ConfigDescription.cpp
#
import re
import ctypes
from functools import wraps

import AconfigurationConst
from ResourcesTypes import ResTable_config

SDK_CUPCAKE = 3
SDK_DONUT = 4
SDK_ECLAIR = 5
SDK_ECLAIR_0_1 = 6
SDK_ECLAIR_MR1 = 7
SDK_FROYO = 8
SDK_GINGERBREAD = 9
SDK_GINGERBREAD_MR1 = 10
SDK_HONEYCOMB = 11
SDK_HONEYCOMB_MR1 = 12
SDK_HONEYCOMB_MR2 = 13
SDK_ICE_CREAM_SANDWICH = 14
SDK_ICE_CREAM_SANDWICH_MR1 = 15
SDK_JELLY_BEAN = 16
SDK_JELLY_BEAN_MR1 = 17
SDK_JELLY_BEAN_MR2 = 18
SDK_KITKAT = 19
SDK_KITKAT_WATCH = 20
SDK_LOLLIPOP = 21
SDK_LOLLIPOP_MR1 = 22

wildcardName = "any"

def anyDecorator(func):
    @wraps(func)
    def wrapper(strIn, config):
        try:
            parseStr, outStr = strIn.split('-', 1)
        except:
            parseStr, outStr = strIn, ''
        if func(parseStr, config):
            return outStr
        return strIn
    return wrapper

@anyDecorator
def parseMcc(parseStr, config):
    if parseStr == wildcardName:
        config.mcc = 0
        return True
    if not parseStr.startswith('mcc') or len(parseStr) != 6:
        return False
    try:
        config.mcc = int(parseStr[3:])
        return True
    except:
        return False

@anyDecorator
def parseMnc(parseStr, config):
    if parseStr == wildcardName:
        config.mcc = 0
        return True
    if not parseStr.startswith('mnc') or len(parseStr) == 3 or len(parseStr) > 6:
        return False
    try:
        ival = int(parseStr[3:])
        config.mnc = ival or AconfigurationConst.ACONFIGURATION_MNC_ZERO
        return True
    except:
        return False

def parseLocale(parseStr, config):
    try:
        locStr, outStr = parseStr.split('-', 1)
    except:
        locStr, outStr = parseStr, ''
    if locStr[0] == 'b' and locStr[1] == '+':
        #  This is a "modified" BCP-47 language tag. Same semantics as BCP-47 tags,
        #  except that the separator is "+" and not "-".
        subtags = locStr.split('+')[1:]
        nlen = len(subtags)
        if nlen >= 1:
            config.language = subtags[0].lower()
        if nlen == 2:
            case = len(subtags[1])
            if case in [2,3]:
                config.country = subtags[1].upper()
            elif case == 4:
                config.localeScript = subtags[1].title()
            elif case in [5, 6, 7, 8]:
                config.localeVariant = subtags[1]
            else:
                return parseStr
        elif nlen == 3:
            if len(subtags[1]) == 4:
                config.localeScript = subtags[1].title()
            elif len(subtags[1]) in [2, 3]:
                config.country = subtags[1]
            else:
                return parseStr

            if len(subtags[2]) > 4:
                config.localeVariant = subtags[2]
            elif len(subtags[1]) in [2, 3]:
                config.country = subtags[2].upper()
        elif nlen == 4:
            config.language = subtags[0].lower()
            config.localeScript = subtags[1].title()
            config.country = subtags[2].upper()
            config.localeVariant = subtags[3]
        else:
            return parseStr
        return outStr
    else:
        if len(locStr) in [2, 3] and locStr.isalpha() and locStr != 'car':
            config.language = locStr.lower()
            try:
                locStr, outStr = outStr.split('-', 1)
            except:
                locStr, outStr = outStr, ''
            if locStr and locStr[0] == 'r' and len(locStr) == 3:
                config.country = locStr[1:].upper()
                return outStr
            else:
                return locStr
    return parseStr


@anyDecorator
def parseLayoutDirection(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.LAYOUTDIR_ANY
    elif parseStr == "ldltr":
        layoutattr = ResTable_config.LAYOUTDIR_LTR
    elif parseStr == "ldrtl":
        layoutattr = ResTable_config.LAYOUTDIR_RTL
    else:
        return False
    config.screenLayout = (config.screenLayout & ResTable_config.MASK_LAYOUTDIR) \
                          | layoutattr
    return True

@anyDecorator
def parseScreenLayoutSize(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.SCREENSIZE_ANY
    elif parseStr == "small":
        layoutattr = ResTable_config.SCREENSIZE_SMALL
    elif parseStr == "normal":
        layoutattr = ResTable_config.SCREENSIZE_NORMAL
    elif parseStr == "large":
        layoutattr = ResTable_config.SCREENSIZE_LARGE
    elif parseStr == "xlarge":
        layoutattr = ResTable_config.SCREENSIZE_XLARGE
    else:
        return False
    config.screenLayout = (config.screenLayout & ResTable_config.MASK_SCREENSIZE) \
                          | layoutattr
    return True

@anyDecorator
def parseScreenLayoutLong(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.SCREENLONG_ANY
    elif parseStr == "long":
        layoutattr = ResTable_config.SCREENLONG_YES
    elif parseStr == "notlong":
        layoutattr = ResTable_config.SCREENLONG_NO
    else:
        return False
    config.screenLayout = (config.screenLayout & ResTable_config.MASK_SCREENLONG) \
                          | layoutattr
    return True

@anyDecorator
def parseOrientation(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.ORIENTATION_ANY
    elif parseStr == "port":
        layoutattr = ResTable_config.ORIENTATION_PORT
    elif parseStr == "land":
        layoutattr = ResTable_config.ORIENTATION_LAND
    elif parseStr == "square":
        layoutattr = ResTable_config.ORIENTATION_SQUARE
    else:
        return False
    config.orientation = layoutattr
    return True

@anyDecorator
def parseScreenLayoutRound(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.SCREENROUND_ANY
    elif parseStr == "round":
        layoutattr = ResTable_config.SCREENROUND_YES
    elif parseStr == "notround":
        layoutattr = ResTable_config.SCREENROUND_NO
    else:
        return False
    config.screenLayout = (config.screenLayout & ResTable_config.MASK_SCREENROUND) \
                          | layoutattr
    return True


@anyDecorator
def parseUiModeType(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.UI_MODE_TYPE_ANY
    elif parseStr == "desk":
        layoutattr = ResTable_config.UI_MODE_TYPE_DESK
    elif parseStr == "car":
        layoutattr = ResTable_config.UI_MODE_TYPE_CAR
    elif parseStr == "television":
        layoutattr = ResTable_config.UI_MODE_TYPE_TELEVISION
    elif parseStr == "appliance":
        layoutattr = ResTable_config.UI_MODE_TYPE_APPLIANCE
    elif parseStr == "watch":
        layoutattr = ResTable_config.UI_MODE_TYPE_WATCH
    else:
        return False
    config.uiMode = (config.uiMode & ResTable_config.MASK_UI_MODE_TYPE) \
                    | layoutattr
    return True

@anyDecorator
def parseUiModeNight(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.UI_MODE_NIGHT_ANY
    elif parseStr == "nigth":
        layoutattr = ResTable_config.UI_MODE_NIGHT_YES
    elif parseStr == "nonigth":
        layoutattr = ResTable_config.UI_MODE_NIGHT_NO
    else:
        return False
    config.uiMode = (config.uiMode & ResTable_config.MASK_UI_MODE_TYPE) \
                    | layoutattr
    return True

@anyDecorator
def parseDensity(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.DENSITY_DEFAULT
    elif parseStr == "anydpi":
        layoutattr = ResTable_config.DENSITY_ANY
    elif parseStr == "nodpi":
        layoutattr = ResTable_config.DENSITY_NONE
    elif parseStr == "ldpi":
        layoutattr = ResTable_config.DENSITY_LOW
    elif parseStr == "mdpi":
        layoutattr = ResTable_config.DENSITY_MEDIUM
    elif parseStr == "tvdpi":
        layoutattr = ResTable_config.DENSITY_TV
    elif parseStr == "hdpi":
        layoutattr = ResTable_config.DENSITY_HIGH
    elif parseStr == "xhdpi":
        layoutattr = ResTable_config.DENSITY_XHIGH
    elif parseStr == "xxhdpi":
        layoutattr = ResTable_config.DENSITY_XXHIGH
    elif parseStr == "xxxhdpi":
        layoutattr = ResTable_config.DENSITY_XXXHIGH
    else:
        if not parseStr.upper().endswith('DPI'):
            return False
        try:
            layoutattr = int(parseStr[:-3])
        except:
            return False
    config.density = layoutattr
    return True

@anyDecorator
def parseTouchscreen(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.TOUCHSCREEN_ANY
    elif parseStr == "notouch":
        layoutattr = ResTable_config.TOUCHSCREEN_NOTOUCH
    elif parseStr == "stylus":
        layoutattr = ResTable_config.TOUCHSCREEN_STYLUS
    elif parseStr == "finger":
        layoutattr = ResTable_config.TOUCHSCREEN_FINGER
    else:
        return False
    config.touchscreen = layoutattr
    return True

@anyDecorator
def parseKeysHidden(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.KEYSHIDDEN_ANY
    elif parseStr == "keysexposed":
        layoutattr = ResTable_config.KEYSHIDDEN_NO
    elif parseStr == "keyhidden":
        layoutattr = ResTable_config.KEYSHIDDEN_YES
    elif parseStr == "keysoft":
        layoutattr = ResTable_config.KEYSHIDDEN_SOFT
    else:
        return False
    config.inputFlags = (config.inputFlags & ResTable_config.MASK_KEYSHIDDEN) \
                    | layoutattr
    return True

@anyDecorator
def parseKeyboard(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.KEYBOARD_ANY
    elif parseStr == "nokeys":
        layoutattr = ResTable_config.KEYBOARD_NOKEYS
    elif parseStr == "qwerty":
        layoutattr = ResTable_config.KEYBOARD_QWERTY
    elif parseStr == "12key":
        layoutattr = ResTable_config.KEYBOARD_12KEY
    else:
        return False
    config.keyboard = layoutattr
    return True

@anyDecorator
def parseNavHidden(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.NAVHIDDEN_ANY
    elif parseStr == "navexposed":
        layoutattr = ResTable_config.NAVHIDDEN_NO
    elif parseStr == "navhidden":
        layoutattr = ResTable_config.NAVHIDDEN_YES
    else:
        return False
    config.inputFlags = (config.inputFlags & ResTable_config.MASK_NAVHIDDEN) \
                    | layoutattr
    return True

@anyDecorator
def parseNavigation(parseStr, config):
    if parseStr == wildcardName:
        layoutattr = ResTable_config.NAVIGATION_ANY
    elif parseStr == "nonav":
        layoutattr = ResTable_config.NAVIGATION_NONAV
    elif parseStr == "dpad":
        layoutattr = ResTable_config.NAVIGATION_DPAD
    elif parseStr == "trackball":
        layoutattr = ResTable_config.NAVIGATION_TRACKBALL
    elif parseStr == "wheel":
        layoutattr = ResTable_config.NAVIGATION_WHEEL
    else:
        return False
    config.navigation = layoutattr
    return True

@anyDecorator
def parseScreenSize(parseStr, config):
    if parseStr == wildcardName:
        w = ResTable_config.SCREENWIDTH_ANY
        h = ResTable_config.SCREENHEIGHT_ANY
    else:
        try:
            x, y = parseStr.split('x')
        except:
            return False

        try:
            w = int(x)
            h = int(y)
            if w < h:
                return False
        except:
            return False
    config.screenwidth = w
    config.screenHeight = h
    return True

@anyDecorator
def parseSmallestScreenWidthDp(parseStr, config):
    if parseStr == wildcardName:
        config.smallestScreenWidthDp = ResTable_config.SCREENWIDTH_ANY
        return True
    if not parseStr.startswith('sw') or not parseStr.endswith('dp'):
        return False
    try:
        config.smallestScreenWidthDp = int(parseStr[2:-2])
    except:
        return False
    return True

@anyDecorator
def parseScreenWidthDp(parseStr, config):
    if parseStr == wildcardName:
        config.screenWidthDp = ResTable_config.SCREENWIDTH_ANY
        return True
    if not parseStr.startswith('w') or not parseStr.endswith('dp'):
        return False
    try:
        config.screenWidthDp = int(parseStr[1:-2])
    except:
        return False
    return True

@anyDecorator
def parseScreenHeightDp(parseStr, config):
    if parseStr == wildcardName:
        config.screenHeightDp = ResTable_config.SCREENHEIGHT_ANY
        return True
    if not parseStr.startswith('h') or not parseStr.endswith('dp'):
        return False
    try:
        config.screenHeightDp = int(parseStr[1:-2])
    except:
        return False
    return True

@anyDecorator
def parseVersion(parseStr, config):
    if parseStr == wildcardName:
        config.sdkVersion = ResTable_config.SDKVERSION_ANY
        config.minorVersion = ResTable_config.MINORVERSION_ANY
        return True
    if not parseStr.startswith('v'):
        return False
    try:
        config.screenHeightDp = int(parseStr[1:])
        config.minorVersion = 0
    except:
        return False
    return True


class ConfigDescription(ResTable_config):
    @staticmethod
    def parse(strIn, configDescription):
        '''
        Parse a string of the form 'fr-sw600dp-land' and fill in the
        given ResTable_config with resulting configuration parameters.
        The resulting configuration has the appropriate sdkVersion defined
        for backwards compatibility.
        :param strIn: String: String to parse.
        :param configDescription: ConfigDescription: Parse result.
        :return: boolean: True if no error occur while parsing, else False.
        '''
        pArray = (parseMcc, parseMnc, parseLocale, parseLayoutDirection,
                  parseSmallestScreenWidthDp, parseScreenWidthDp, parseScreenHeightDp,
                  parseScreenLayoutSize, parseScreenLayoutLong, parseScreenLayoutRound,
                  parseOrientation,
                  parseUiModeType, parseUiModeNight, parseDensity, parseTouchscreen,
                  parseKeysHidden, parseKeyboard, parseNavHidden, parseNavigation,
                  parseScreenSize, parseVersion, )
        pMax = len(pArray)
        pPos = 0 if strIn else None
        while strIn and pPos < pMax:
            strIn = pArray[pPos](strIn, configDescription)
            pPos += 1
        if strIn and pPos == pMax:
            return False
        if pPos is not None:
            ConfigDescription.applyVersionForCompatibility(configDescription)
        return True

    @staticmethod
    def applyVersionForCompatibility(config):
        minSdk = 0
        rtc = ResTable_config
        if config.density == rtc.DENSITY_ANY:
            minSdk = SDK_LOLLIPOP
        elif config.smallestScreenWidthDp != rtc.SCREENWIDTH_ANY or \
             config.screenWidthDp != rtc.SCREENWIDTH_ANY or \
             config.screenHeightDp != rtc.SCREENHEIGHT_ANY:
            minSdk = SDK_HONEYCOMB_MR2
        elif (config.uiMode & rtc.MASK_UI_MODE_TYPE) != rtc.UI_MODE_TYPE_ANY or \
              (config.uiMode & rtc.MASK_UI_MODE_NIGHT) != rtc.UI_MODE_NIGHT_ANY:
            minSdk = SDK_FROYO
        elif (config.screenLayout & rtc.MASK_SCREENSIZE) != rtc.SCREENSIZE_ANY or \
                 (config.screenLayout & rtc.MASK_SCREENLONG) != rtc.SCREENLONG_ANY or \
                 config.density != rtc.DENSITY_DEFAULT:
            minSdk = SDK_DONUT
        
        if minSdk > config.sdkVersion:
            config.sdkVersion = minSdk