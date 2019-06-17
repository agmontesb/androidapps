# -*- coding: utf-8 -*-
import re
import collections

from Tools.aapt.Resource import ResourceNameRef, ResourceType
from Tools.aapt.ResourcesValues import Reference, BinaryPrimitive
from Tools.aapt import ResourcesTypes

def normStr(aStr, state):
    #
    # ported from:
    # https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/util/Util.cpp
    # line 192
    #
    if state['mError']:
        return state
    end = len(aStr)
    start = 0
    current = start
    while current != end:
        if state['mLastCharWasEscape']:
            case = aStr[current]
            if case == 't':
                state['mStr'] += '\t'
            elif case == 'n':
                state['mStr'] += '\n'
            elif case in '#@?"\'\\u':
                state['mStr'] += case
            else:
                pass
            state['mLastCharWasEscape'] = False
            start = current + 1
        elif aStr[current] == '"':
            if not state['mQuote'] and state['mTrailingSpace']:
                #  We found an opening quote, and we have
                #  trailing space, so we should append that
                #  space now.
                if state['mTrailingSpace']:
                    #  We had trailing whitespace, so
                    #  replace with a single space.
                    if state['mStr']:
                        state['mStr'] += ' '
                    state['mTrailingSpace'] = False
            state['mQuote'] = not state['mQuote']
            state['mStr'] += aStr[start: current]
            start = current + 1
        elif aStr[current] == '\'' and not state['mQuote']:
            #  This should be escaped.
            state['mError'] = "unescaped apostrophe"
            return state
        elif aStr[current] == '\\':
            #  This is an escape sequence, convert to the real value.
            if not state['mQuote'] and state['mTrailingSpace']:
                #  We had trailing whitespace, so
                #  replace with a single space.
                if state['mStr']:
                    state['mStr'] += ' '
                state['mTrailingSpace'] = False
            state['mStr'] += aStr[start: current]
            start = current + 1
            state['mLastCharWasEscape'] = True
        elif not state['mQuote']:
            #  This is not quoted text, so look for whitespace.
            if aStr[current] == ' ':
                #  We found whitespace, see if we have seen some
                #  before.
                if not state['mTrailingSpace']:
                    #  We didn't see a previous adjacent space,
                    #  so mark that we did.
                    state['mTrailingSpace'] = True
                    state['mStr'] += aStr[start: current]
                #  Keep skipping whitespace.
                start = current + 1
            elif state['mTrailingSpace']:
                #  We saw trailing space before, so replace all
                #  that trailing space with one space.
                if state['mStr']:
                    state['mStr'] += ' '
                state['mTrailingSpace'] = False
        current += 1
    state['mStr'] += aStr[start: end]
    return state


class Diagnostics(object):

    def __init__(self):
        super(Diagnostics, self).__init__()
        self.error = ''
        self.warn = ''
        self.note = ''


class ObjRef(object):

    def __init__(self, value=None):
        super(ObjRef, self).__init__()
        self.setTo(value)

    def __getattr__(self, item):
        return getattr(self._value, item)

    def setTo(self, value):
        self._value = value


def extractResourceName(resStr):
    package, resStr = resStr.split(':') if ':' in resStr else (None, resStr)
    atype, entry = resStr.split('/') if '/' in resStr else ('', resStr)
    return package, atype, entry


def tryParseReferenceB(aStr, outResNameRef, outCreate=None, outPriv=None):
    aStr = aStr.strip('\n\r\t ')
    if not aStr: return False
    create = False
    priv = False
    if not aStr.startswith('@'): return False
    aStr = aStr[1:]
    create = aStr.startswith('+')
    priv = aStr.startswith('*')
    if create or priv:
        aStr = aStr[1:]
    nPckg, nType, nEntry = extractResourceName(aStr)
    parsedType = ResourceType.parseResourceType(nType)
    if not parsedType: return False
    if create and parsedType != ResourceType.kId: return False
    outResNameRef.package = nPckg
    outResNameRef.type = parsedType
    outResNameRef.entry = nEntry
    if outCreate: outCreate.setTo(create)
    if outPriv: outPriv.setTo(priv)
    return True


def tryParseAttributeReference(aStr, outRef):
    aStr = aStr.strip('\n\r\t ')
    if not aStr: return False
    if not aStr.startswith('?'): return False
    nPckg, nType, nEntry = extractResourceName(aStr[1:])
    if nType and nType != 'attr': return False
    outRef.package = nPckg
    outRef.type = ResourceType.kAttr
    outRef.entry = nEntry
    return True


def parseStyleParentReference(aStr, errStr):
    if not aStr: return None
    errStr.setTo('')
    name = aStr
    hasLeadingIdentifiers = name[0] in '@?'
    privateRef = False
    if hasLeadingIdentifiers:
        name = name[1:]
        if name[0] == '*':
            privateRef = True
            name = name[1:]
    ref = ResourceNameRef()
    ref.type = ResourceType.kStyle
    ref.package, typeStr, ref.entry = extractResourceName(name)
    if typeStr:
        parsedType = ResourceType.parseResourceType(typeStr)
        if not parsedType or parsedType != ResourceType.kStyle:
            errStr.setTo('invalid resource type "%s" for parent of stye' % typeStr)
            return None
    else:
        if hasLeadingIdentifiers:
            errMessage = 'invalid parent reference "%s"' % aStr
            return None, errMessage
    if not hasLeadingIdentifiers and not ref.package and typeStr:
        errStr.setTo('invalid parent reference "%s"' % aStr)
        return None
    result = Reference(ref)
    result.privateReference = privateRef
    return result


def tryParseReferenceR(aStr, outCreate):
    ref = ResourceNameRef()
    privateRef = ObjRef(False)
    value = None
    if tryParseReferenceB(aStr, ref, outCreate, privateRef):
        value = Reference(ref)
        value.privateReference = privateRef._value
    elif tryParseAttributeReference(aStr, ref):
        outCreate.setTo(False)
        value = Reference(ref, Reference.Type.kAttribute)
    return value


def tryParseNullOrEmpty(aStr):
    aStr = aStr.strip('\n\r\t ')
    value = ResourcesTypes.Res_value()
    if aStr == '@null':
        value.dataType = ResourcesTypes.Res_value.TYPE_REFERENCE
    elif aStr == '@empty':
        value.dataType = ResourcesTypes.Res_value.TYPE_NULL
        value.data = ResourcesTypes.Res_value.DATA_NULL_EMPTY
    else:
        return None
    return BinaryPrimitive(value)


def tryParseColor(aStr):
    aStr = aStr.strip('\n\r\t ')
    if not aStr or aStr[0] != '#': return None
    try:
        aValue = int(aStr, 16)
    except:
        return BinaryPrimitive()
    value = ResourcesTypes.Res_value()
    value.data = 0xff000000 | aValue
    case = len(aStr)
    if case == 4:
        value.dataType = ResourcesTypes.Res_value.TYPE_INT_COLOR_RGB4
    elif case == 5:
        value.dataType = ResourcesTypes.Res_value.TYPE_INT_COLOR_ARGB4
    elif case == 7:
        value.dataType = ResourcesTypes.Res_value.TYPE_INT_COLOR_RGB8
    elif case == 9:
        value.dataType = ResourcesTypes.Res_value.TYPE_INT_COLOR_ARGB8
    else:
        return None
    return BinaryPrimitive(value)


def tryParseBool(aStr):
    aStr = aStr.strip('\n\r\t ').lower()
    data = 0
    if aStr == 'true':
        data = 0xffffffff
    elif aStr != 'false':
        return None
    value = ResourcesTypes.Res_value()
    value.dataType =  ResourcesTypes.Res_value.TYPE_INT_BOOLEAN
    value.data = data
    return BinaryPrimitive(value)


def tryParseInt(aStr):
    value = ResourcesTypes.Res_value()
    if not ResourcesTypes.u16stringToInt(aStr, value): return None
    return BinaryPrimitive(value)


def tryParseFloat(aStr):
    value = ResourcesTypes.Res_value()
    if not ResourcesTypes.stringToFloat(aStr, value): return None
    return BinaryPrimitive(value)

def tryParseEnumSymbol(enumAttr, aStr):
    aStr = aStr.strip('\n\r\t ')
    for symbol in enumAttr.symbols:
        enumSymbolResourceName = symbol.symbol.name
        if aStr == enumSymbolResourceName.entry:
            value = ResourcesTypes.Res_value()
            value.dataType = ResourcesTypes.Res_value.TYPE_INT_DEC
            value.data = symbol.value
            return BinaryPrimitive(value)
    return None

def tryParseFlagSymbol(flagAttr, aStr):
    flags = ResourcesTypes.Res_value()
    flags.dataType = ResourcesTypes.Res_value.TYPE_INT_DEC
    for part in aStr.split('|'):
        part = part.strip('\n\r\t ')
        flagset = False
        for symbol in flagAttr.symbols:
            flagSymbolResourceName = symbol.symbol.name
            if part == flagSymbolResourceName.entry:
                flags.data |= symbol.value
                flagset = True
                break
        if not flagset: return None
    return BinaryPrimitive(flags)

def androidTypeToAttributeTypeMask(aType):
    rvt = ResourcesTypes.Res_value
    rtm = ResourcesTypes.ResTable_map
    if aType in [rvt.TYPE_NULL, rvt.TYPE_REFERENCE, rvt.TYPE_ATTRIBUTE, rvt.TYPE_DYNAMIC_REFERENCE]:
        return rtm.TYPE_REFERENCE
    elif aType == rvt.TYPE_STRING:
        return rtm.TYPE_STRING
    elif aType == rvt.TYPE_FLOAT:
        return rtm.TYPE_FLOAT
    elif aType == rvt.TYPE_DIMENSION:
        return rtm.TYPE_DIMENSION
    elif aType == rvt.TYPE_FRACTION:
        return rtm.TYPE_FRACTION
    elif aType == rvt.TYPE_INT_BOOLEAN:
        return rtm.TYPE_INT_BOOLEAN
    elif aType in [rvt.TYPE_INT_DEC, rvt.TYPE_INT_HEX]:
        return rtm.TYPE_INTEGER | rtm.TYPE_ENUM | rtm.TYPE_FLAGS
    elif aType in [rvt.TYPE_INT_COLOR_ARGB8, rvt.TYPE_INT_COLOR_RGB8, rvt.TYPE_INT_COLOR_ARGB4, rvt.TYPE_INT_COLOR_RGB4]:
        return rtm.TYPE_COLOR
    else:
        return 0


def parseItemForAttributeM(value, typeMask, onCreateReference=None):
    nullOrEmpty = tryParseNullOrEmpty(value)
    if nullOrEmpty: return nullOrEmpty
    create = ObjRef(False)
    reference = tryParseReferenceR(value, create)
    if reference:
        if create._value and onCreateReference: onCreateReference(reference.name)
        return reference
    if typeMask & ResourcesTypes.ResTable_map.TYPE_COLOR:
        color = tryParseColor(value)
        if color: return color
    if typeMask & ResourcesTypes.ResTable_map.TYPE_BOOLEAN:
        boolean = tryParseBool(value)
        if boolean: return boolean
    if typeMask & ResourcesTypes.ResTable_map.TYPE_INTEGER:
        integer = tryParseInt(value)
        if integer: return integer
    rtm = ResourcesTypes.ResTable_map
    floatMask = rtm.TYPE_FLOAT | rtm.TYPE_DIMENSION | rtm.TYPE_FRACTION
    if typeMask & floatMask:
        floatingPoint = tryParseFloat(value)
        if floatingPoint and typeMask & androidTypeToAttributeTypeMask(floatingPoint.value.dataType):
            return floatingPoint
    return None


def parseItemForAttributeA(aStr, attr, onCreateReference=None):
    typeMask = attr.typeMask
    value = parseItemForAttributeM(aStr, typeMask, onCreateReference)
    if value: return value
    if typeMask & ResourcesTypes.ResTable_map.TYPE_ENUM:
        enumValue = tryParseEnumSymbol(attr, aStr)
        if enumValue: return enumValue
    if typeMask & ResourcesTypes.ResTable_map.TYPE_FLAGS:
        flagValue = tryParseFlagSymbol(attr, aStr)
        if flagValue: return flagValue




