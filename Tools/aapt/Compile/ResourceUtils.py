# -*- coding: utf-8 -*-
from Tools.aapt.Resource import ResourceNameRef, ResourceType
from Tools.aapt.ResourcesValues import Reference


def extractResourceName(resStr):
    package, resStr = resStr.split(':') if ':' in resStr else ('', resStr)
    atype, entry = resStr.split('/') if '/' in resStr else ('', resStr)
    return package, atype, entry


def parseStyleParentReference(aStr):
    if not aStr: return None
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
            errMessage = 'invalid resource type "%s" for parent of stye' % typeStr
            return None, errMessage
    else:
        if hasLeadingIdentifiers:
            errMessage = 'invalid parent reference "%s"' % aStr
            return None, errMessage
    if not hasLeadingIdentifiers and ref.package and typeStr:
        errMessage = 'invalid parent reference "%s"' % aStr
        return None, errMessage
    result = Reference(ref)
    result.privateReference = privateRef
    return result, ''

