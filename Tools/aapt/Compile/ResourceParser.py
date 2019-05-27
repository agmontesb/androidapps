# -*- coding: utf-8 -*-
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceParser.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceParser.cpp
#
from Tools.aapt.ResourcesTypes import ResTable_map, Res_value, u16stringToInt
from Tools.aapt.Resource import ResourceNameRef, ResourceType, ResourceId, ResourceName
from Tools.aapt.ResourcesValues import Attribute, Reference, Style, Styleable, Array, Plural
from Tools.aapt.Compile import ResourceTable, ResourceUtils

kAllowRawString = True
kNoRawString = False

class ResourceParser(object):

    def __init__(self, resTable, source, configDesc):
        super(ResourceParser, self).__init__()
        self.mTable = resTable
        self.mSource = source
        self.mConfig = configDesc

    def parse(self, parser):
        error = False
        parser.nextTag()
        if parser.getNamespace() or parser.getName() != 'resources':
            errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
            errMessage += 'root element must be <resources>'
            print errMessage
            return False
        error |= self.parseResources(parser)
        if parser.getEventType() != parser.END_DOCUMENT:
            errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
            errMessage += "xml parser error"
            print errMessage
            return False
        return not error

    def flattenXmlSubtree(self, parser, outRawString, outStyleString):
        pass

    def parseXml(self, parser, typeMask, allowRawValue):
        pass

    def parseResources(self, parser):
        error = False
        comment = ''
        depth = parser.getDepth()
        while parser.getEventType() != parser.END_DOCUMENT:
            event = parser.next()
            if event == parser.COMMENT:
                comment = parser.getText()
                continue
            if event == parser.TEXT:
                if not parser.isWhitespace():
                    errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
                    errMessage += 'plain text not allowed here'
                    print errMessage
                    error = True
                continue

            assert event == parser.START_TAG

            if parser.getNamespace():
                continue
            elementName = parser.getName()
            if elementName in ('skip', 'eat-comment'):
                comment = ''
                continue
            maybeName = parser.getAttributeValue('', 'name')
            if not maybeName:
                errMessage = 'ERROR %s:%s <%s>  tag must have a "name" attribute'
                print errMessage % (self.mSource, parser.getLineNumber(), elementName)
                error = True
                continue
            name = maybeName
            if elementName == 'item':
                maybeType = parser.getAttributeValue('', 'type')
                if maybeName:
                    elementName = maybeType
                else:
                    errMessage = 'ERROR %s:%s <item>  tag must have a "type" attribute'
                    print errMessage % (self.mSource, parser.getLineNumber())
                    error = True
                    continue
            if elementName == 'id':
                resName = ResourceNameRef(None, ResourceType.kId, name)
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                error |= not self.mTable.addResource(resName, None, source, ResourceId())
            elif elementName == 'string':
                resName = ResourceNameRef(None, ResourceType.kString, name)
                error |= not self.parseString(parser, resName)
            elif elementName == 'color':
                resName = ResourceNameRef(None, ResourceType.kColor, name)
                error |= not self.parseColor(parser, resName)
            elif elementName == 'drawable':
                resName = ResourceNameRef(None, ResourceType.kDrawable, name)
                error |= not self.parseColor(parser, resName)
            elif elementName == 'bool':
                resName = ResourceNameRef(None, ResourceType.kBool, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'integer':
                resName = ResourceNameRef(None, ResourceType.kInteger, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'dimen':
                resName = ResourceNameRef(None, ResourceType.kDimen, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'style':
                resName = ResourceNameRef(None, ResourceType.kStyle, name)
                error |= not self.parseStyle(parser, resName)
            elif elementName == 'plurals':
                resName = ResourceNameRef(None, ResourceType.kPlurals, name)
                error |= not self.parsePlural(parser, resName)
            elif elementName == 'array':
                resName = ResourceNameRef(None, ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_ANY)
            elif elementName == 'string-array':
                resName = ResourceNameRef(None, ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_STRING)
            elif elementName == 'integer-array':
                resName = ResourceNameRef(None, ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_INTEGER)
            elif elementName == 'public':
                error |= not self.parsePublic(parser, name)
            elif elementName == 'declare-styleable':
                resName = ResourceNameRef(None, ResourceType.kStyleable, name)
                error |= not self.parseDeclareStyleable(parser, resName)
            elif elementName == 'attr':
                resName = ResourceNameRef(None, ResourceType.kAttr, name)
                error |= not self.parseAttr(parser, resName)
            else:
                errMessage = 'WARNING %s:%s unknown resource type "%s"'
                print errMessage % (self.mSource, parser.getLineNumber(), elementName)
        return not error

    def parseString(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeProduct = parser.getAttributeValue('', 'product')
        if maybeProduct and maybeProduct not in ('default', 'phone'):
            return True
        processedItem = self.parseXml(parser, ResTable_map.TYPE_COLOR, kNoRawString)
        if not processedItem:
            errMessage = 'invalid color'
            print 'ERROR ' + source + errMessage
            return False
        return self.mTable.addResource(resourceName, self.mConfig, source, processedItem)

    def parseColor(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        processedItem = self.parseXml(parser, ResTable_map.TYPE_STRING, kNoRawString)
        if not processedItem:
            errMessage = 'not a valid string'
            print 'ERROR ' + source +errMessage
            return False
        return self.mTable.addResource(resourceName, self.mConfig, source, processedItem)

    def parsePrimitive(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        typeMask = 0
        case = resourceName.type
        if case == ResourceType.kInteger:
            typeMask |= ResTable_map.TYPE_INTEGER
        elif case == ResourceType.kDimen:
            typeMask |= ResTable_map.TYPE_DIMENSION
            typeMask |= ResTable_map.TYPE_FLOAT
            typeMask |= ResTable_map.TYPE_FRACTION
        elif case == ResourceType.kBool:
            typeMask |= ResTable_map.TYPE_BOOLEAN
        else:
            assert False
        item = self.parseXml(parser, typeMask, kNoRawString)
        if not item:
            errMessage = 'invalid %s' & resourceName.type
            print 'ERROR ' + source + errMessage
            return False
        return self.mTable.addResource(resourceName, self.mConfig, source, item)

    def parsePublic(self, parser, name):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeType = parser.getAttributeValue('', 'type')
        if not maybeType:
            errMessage = '<public> must have a "type" attribute'
            print 'ERROR ' + source + errMessage
            return False
        parsedType = ResourceType.parseResourceType(maybeType)
        if not parsedType:
            errMessage = 'invalid resource type "%s" in <public>' % maybeType
            print 'ERROR ' + source + errMessage
            return False
        resourceName = ResourceNameRef(None, parsedType, name)
        resourceId = ResourceId()
        maybeId = parser.getAttributeValue('', 'id')
        if maybeId:
            val = Res_value()
            result = u16stringToInt(maybeId.value().data(), val) # ResourcesTypes.u16StringToInt
            resourceId.id = val.data
            if not result or not resourceId.isValid():
                errMessage = 'invalid resource ID "%s" in <public>' % maybeId
                print 'ERROR ' + source + errMessage
                return False
        if parsedType == ResourceType.kId:
            self.mTable.addResource(resourceName, None, source, ResourceId())
        return self.mTable.markPublic(resourceName, resourceId, source)

    def parseAttr(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        actualName = resourceName.toResourceName()
        attr = self.parseAttrImpl(parser, actualName, False)
        if not attr:
            return False
        return self.mTable.addResource(actualName, self.mConfig, source, attr)

    def parseAttrImpl(self, parser, resourceName, weak):
        typeMask = 0
        maybeFormat = parser.getAttributeValue('', 'format')
        if maybeFormat:
            fcn = lambda x: (ResTable_map, 'TYPE_%s' % x.strip().upper())
            trnFcn = lambda t, x: t | (getattr(*fcn(x)) if hasattr(*fcn(x)) else 0)
            typeMap = reduce(trnFcn, maybeFormat.split('|'), 0)
            if not typeMask:
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                source += 'invalid attribute format "%s"' % maybeFormat
                print 'ERROR ' + source
                return None
        if weak and not maybeFormat:
            suffix = resourceName.entry.split(':')
            package, suffix = suffix.split(':') if ':' in suffix else ('', suffix)
            atype, suffix = suffix.split('/') if '/' in suffix else ('', suffix)
            name = suffix
            if not atype and package:
                resourceName.package = package
                resourceName.entry = name
        items = []
        comment = ''
        error = False
        depth = parser.getDepth()
        while True:
            parser.next()
            if parser.getDepth() == depth: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace and elementName in ['flag', 'enum']:
                if elementName == 'enum':
                    if typeMask & ResTable_map.TYPE_FLAGS:
                        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                        source += 'can not define an <enum>; already defined a <flag>'
                        print 'ERROR ' + source
                        error = True
                        continue
                    typeMask |= ResTable_map.TYPE_ENUM
                elif elementName == 'flag':
                    if typeMask & ResTable_map.TYPE_ENUM:
                        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                        source += 'can not define an <flag>; already defined a <enum>'
                        print 'ERROR ' + source
                        error = True
                        continue
                    typeMask |= ResTable_map.TYPE_FLAGS
                s = self.parseEnumOrFlagItem(parser, elementName)
                if s and self.mTable.addResource(s.value().symbol.name, self.mConfig, '%s:%s ' % (self.mSource, parser.getLineNumber()), ResourceId()):
                    items.append(s.value())
                else:
                    error = True
            elif elementName in ('skip', 'eat-comment'):
                comment = ''
                continue
            else:
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                source += '<%s>' % elementName
                print 'ERROR ' + source
                error = True
        if error: return None
        attr = Attribute(weak)
        attr.symbols.swap(items)
        attr.typeMask = typeMask if typeMask else ResTable_map.TYPE_ANY
        return attr

    def parseEnumOrFlagItem(self, parser, tag):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeName = parser.getAttributeValue('', 'name')
        if not maybeName:
            source += 'no attribute "name" found for tag <%s>' % tag
            print 'ERROR ' + source
            return None
        maybeValue = parser.getAttributeValue('', 'value')
        if not maybeValue:
            source += 'no attribute "value" found for tag <%s>' % tag
            print 'ERROR ' + source
            return None

        val = Res_value()
        if not u16stringToInt(maybeValue, val): # ResourcesTypes.u16stringToInt
            source += 'invalid value "%s" for tag <%s>; must be integer' % (maybeValue, tag)
            print 'ERROR ' + source
            return None

        resName = ResourceNameRef(None, ResourceType.kId, maybeValue)
        ref = Reference(resName, val.data)
        return Attribute.Symbol(ref)

    def parseStyle(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        style = Style()
        maybeParent = parser.getAttributeValue('', 'parent')
        if maybeParent is not None:
            if not maybeParent:
                style.parent, errStr = ResourceUtils.parseStyleParentReference(maybeParent)
                if not style.parent:
                    source += errStr
                    print 'ERROR ' + source
                    return False
            resName = style.parent.value().name
            transformedName = self.transformPackage(parser, resName, '')
            if transformedName: style.pareent.value().name = transformedName
        else:
            styleName = resourceName.entry
            pos = styleName.rfind('.')
            if pos != -1:
                style.parentInferred = True
                style.parent = Reference(ResourceName(None, ResourceType.kStyle, styleName[:pos]))
        error = False
        comment = ''
        depth = parser.getDepth()
        while True:
            parser.next()
            if parser.getDepth() == depth: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                error |= self.parseStyleItem(parser, style.get())
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                comment = ''
            else:
                errMessage = '%s:%s ' % (self.mSource, parser.getLineNumber())
                errMessage += ':%s>' % elementName
                print 'ERROR ' + errMessage
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, style)

    def parseStyleItem(self, parser, style):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeName = parser.getAttributeValue('', 'name')
        if not maybeName:
            source += '<item> must have a "name" attribute'
            print 'ERROR ' + source
            return False
        maybeKey = self.parseXmlAttributeName(maybeName.value())
        if not maybeKey:
            source += 'invalid attribute name "%s"' % maybeName.value()
            print 'ERROR ' + source
            return False
        transformedName = self.transformPackage(parser, maybeKey.value(), u"")
        if transformedName: maybeKey = transformedName
        value = self.parseXml(parser, 0, kAllowRawString)
        if not  value:
            source += 'could not parse style item'
            print 'ERROR ' + source
            return False
        style.entries.append(Style.Entry(Reference(maybeKey.value()), value))
        return True


    @staticmethod
    def parseXmlAttributeName(aStr):
        package, name = aStr.strip().split(':') if ':' in aStr else ('', aStr)
        return ResourceName(package, ResourceType.kAttr, name)

    @staticmethod
    def transformPackage(parser, resName, package):
        if resName.package is None:
            return ResourceName(package, resName.type, resName.entry)
        kSchemaPrefix = "http://schemas.android.com/apk/res/"
        kSchemaAuto = "http://schemas.android.com/apk/res-auto"
        nNs = parser.getNamespaceCount(parser.getDepth())
        it = filter(lambda x: parser.getNamespacePrefix(x) == resName.package, range(nNs))
        try:
            uri = parser.getNamespaceUri(it[0])
            if uri.startswith(kSchemaPrefix):
                pckname = uri[len(kSchemaPrefix):]
                return ResourceName(pckname, resName.type, resName.entry)
            elif uri.startswith(kSchemaAuto):
                return ResourceName(package, resName.type, resName.entry)
        except:
            pass
        return None

    def parseDeclareStyleable(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        styleable = Styleable()
        error = False
        comment = ''
        depth = parser.getDepth()
        while True:
            parser.next()
            if parser.getDepth() == depth: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'attr':
                maybeName = parser.getAttributeValue('', 'name')
                if not maybeName:
                    source += '<attr> tag must have a "name" attribute'
                    print 'ERROR ' + source
                    error = True
                    continue
                attrResourceName = ResourceName(None, ResourceType.kAttr, maybeName)
                attr = self.parseAttrImpl(parser, attrResourceName, True)
                if not attr:
                    error = True
                    continue
                styleable.entries.append(attrResourceName)
                error |= not self.mTable.addResource(attrResourceName, self.mConfig, source, attr)
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                comment = ''
            else:
                source += 'unknown tag <%s>' % elementName
                print 'ERROR ' + source
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, styleable)

    def parseArray(self, parser, resourceName, typeMask):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        array = Array()
        error = False
        comment = ''
        depth = parser.getDepth()
        while True:
            parser.next()
            if parser.getDepth() == depth: break
            if parser.getEventType() != parser.START_TAG: continue
            itemSource = '%s:%s ' % (self.mSource, parser.getLineNumber())
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                item = self.parseXml(parser,typeMask, kNoRawString)
                if not item:
                    itemSource += 'could not parse array item'
                    print 'ERROR ' + source
                    error = True
                    continue
                array.items.append(item)
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                comment = ''
            else:
                source += 'unknown tag <%s>' % elementName
                print 'ERROR ' + source
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, array)

    def parsePlural(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        plural = Plural()
        error = False
        comment = ''
        depth = parser.getDepth()
        while True:
            parser.next()
            if parser.getDepth() == depth: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                maybeQuantity = parser.getAttributeValue('', 'quantity')
                if not maybeQuantity:
                    source += '<item> in <plurals> requires attribute "quantity"'
                    print 'ERROR ' + source
                    error = True
                    continue
                trimmedQuantity = maybeQuantity.strip()
                if hasattr(Plural, trimmedQuantity.title()):
                    index = getattr(Plural, trimmedQuantity.title())
                else:
                    errMessage = '<item> in <plural> has invalid value "%s"  for attribute "quantity"'
                    print 'ERROR ' + source + errMessage % trimmedQuantity
                    error = True
                    continue
                if plural.values[index]:
                    errMessage = 'duplicate quantity "%s"'
                    print 'ERROR ' + source + errMessage % trimmedQuantity
                    error = True
                    continue
                plural.values[index] = val = self.parseXml(parser, ResTable_map.TYPE_STRING, kNoRawString)
                if not val:
                    error = True
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                comment = ''
            else:
                errMessage = 'unknown tag <%s>' % elementName
                print 'ERROR ' + source + errMessage
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, plural)
