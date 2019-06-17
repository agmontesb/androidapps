# -*- coding: utf-8 -*-
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceParser.h
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/ResourceParser.cpp
#
from Tools.aapt.ResourcesTypes import ResTable_map, Res_value, u16stringToInt
from Tools.aapt.Resource import ResourceNameRef, ResourceType, ResourceId, ResourceName
from Tools.aapt.ResourcesValues import Id, Item, Attribute, Reference, Style, \
    Styleable, Array, Plural, RawString, StyledString, String
from Tools.aapt.Compile import ResourceTable, ResourceUtils
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Tools.aapt.StringPool_test import Span, StyleString
from Tools.aapt.Compile.ResourceUtils import ObjRef
from Tools.aapt.StringPool import StringPool


kAllowRawString = True
kNoRawString = False
sXliffNamespaceUri = "urn:oasis:names:tc:xliff:document:1.2"

class ResourceParser(object):

    def __init__(self, diag, resTable, source, configDesc):
        super(ResourceParser, self).__init__()
        self.mDiag = diag
        self.mTable = resTable
        self.mSource = source
        self.mConfig = configDesc

    def _retDiag(self, errMessage, tMessage='error'):
        setattr(self.mDiag, tMessage, errMessage)

    def parse(self, parser):
        error = False
        parser.nextTag()
        if parser.getNamespace() or parser.getName() != 'resources':
            errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
            errMessage += 'root element must be <resources>'
            self._retDiag(errMessage)
            return False
        error |= not self.parseResources(parser)
        parser.next()
        if parser.getEventType() != parser.END_DOCUMENT:
            errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
            errMessage += "xml parser error"
            self._retDiag(errMessage)
            return False
        return not error

    def flattenXmlSubtree(self, parser, outRawString, outStyleString):
        spanStack = []
        outRawString._value = ''
        styleString = outStyleString._value._replace(spans=[])
        builder = ''
        depth = parser.getDepth()
        while True:
            event = parser.next()
            if parser.getDepth() < depth or event == parser.END_DOCUMENT: break
            if event == XmlPullParser.END_TAG:
                if not parser.getNamespace():
                    continue
                lstSpan = spanStack.pop()
                lstSpan = lstSpan._replace(lastChar=len(builder))
                styleString.spans.append(lstSpan)
            elif event == XmlPullParser.TEXT:
                if parser.isWhitespace(): continue
                if not builder:
                    state = {'mStr': '', 'mTrailingSpace': False, 'mQuote': False,
                             'mLastCharWasEscape': False, 'mError': ''}
                ResourceUtils.normStr(parser.getText(), state)
                builder = state['mStr']
                outRawString._value += parser.getText()
            elif event == XmlPullParser.START_TAG:
                if parser.getNamespace() != sXliffNamespaceUri:
                    self.mDiag.warn = self.mSource + ':%s' % parser.getLineNumber()
                    warnMessage = 'skipping element "%s" with unknown namespace "%s"'
                    self.mDiag.warn += warnMessage % (parser.getName(), parser.getNamespace())
                    continue
                spanName = parser.getName()
                for k in range(parser.getAttributeCount()):
                    spanName += ';%s=%s' % (parser.getAttributeName(k), parser.getAttributeValue(k))
                spanStack.append(Span(spanName, len(builder), None))
            elif event == XmlPullParser.COMMENT or event == XmlPullParser.IGNORABLE_WHITESPACE:
                continue
            else:
                assert False
        assert not spanStack, "spans haven't been fully processed"
        outStyleString.setTo(styleString._replace(str=builder))
        return True

    def parseXml(self, parser, typeMask, allowRawValue):
        beginXmlLine = parser.getLineNumber()
        rawValue = ObjRef('')
        styleString = ObjRef(StyleString('', []))
        if not self.flattenXmlSubtree(parser, rawValue, styleString):
            return Item()
        if styleString.spans:
            ref = self.mTable.stringPool.makeRef(styleString._value, StringPool.Context(1, self.mConfig))
            return StyledString(ref)
        onCreateReference = lambda name: self.mTable.addResource(name, None, self.mSource + ':%s' % beginXmlLine,
                                                                 Id(), diag=self.mDiag)
        processedItem = ResourceUtils.parseItemForAttributeM(rawValue._value, typeMask, onCreateReference)
        if processedItem:
            ref = Reference(processedItem)
            if ref:
                transformedName = self.transformPackage(parser, ref.name, "")
                if transformedName:
                    ref.name = transformedName
            return processedItem
        if typeMask & ResTable_map.TYPE_STRING:
            ref = self.mTable.stringPool.makeRef(styleString.str, StringPool.Context(1, self.mConfig))
            return String(ref)
        if allowRawValue:
            ref = self.mTable.stringPool.makeRef(rawValue._value, StringPool.Context(1, self.mConfig))
            return RawString(ref)

    def parseResources(self, parser):
        error = False
        comment = ''
        startDepth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() >= startDepth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if event not in (parser.COMMENT, parser.TEXT, parser.START_TAG):
                continue
            if event == parser.COMMENT:
                comment = parser.getText().strip()
                continue
            if event == parser.TEXT:
                if not parser.isWhitespace():
                    errMessage = 'ERROR %s:%s ' % (self.mSource, parser.getLineNumber())
                    errMessage += 'plain text not allowed here'
                    self._retDiag(errMessage)
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
                self._retDiag(errMessage % (self.mSource, parser.getLineNumber(), elementName))
                error = True
                continue
            name = maybeName
            if elementName == 'item':
                maybeType = parser.getAttributeValue('', 'type')
                if maybeName:
                    elementName = maybeType
                else:
                    errMessage = 'ERROR %s:%s <item>  tag must have a "type" attribute'
                    self._retDiag(errMessage % (self.mSource, parser.getLineNumber()))
                    error = True
                    continue
            if elementName == 'id':
                resName = ResourceNameRef('', ResourceType.kId, name)
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                error |= not self.mTable.addResource(resName, None, source, ResourceId())
            elif elementName == 'string':
                resName = ResourceNameRef('', ResourceType.kString, name)
                error |= not self.parseString(parser, resName)
            elif elementName == 'color':
                resName = ResourceNameRef('', ResourceType.kColor, name)
                error |= not self.parseColor(parser, resName)
            elif elementName == 'drawable':
                resName = ResourceNameRef('', ResourceType.kDrawable, name)
                error |= not self.parseColor(parser, resName)
            elif elementName == 'bool':
                resName = ResourceNameRef('', ResourceType.kBool, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'integer':
                resName = ResourceNameRef('', ResourceType.kInteger, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'dimen':
                resName = ResourceNameRef('', ResourceType.kDimen, name)
                error |= not self.parsePrimitive(parser, resName)
            elif elementName == 'style':
                resName = ResourceNameRef('', ResourceType.kStyle, name)
                error |= not self.parseStyle(parser, resName)
            elif elementName == 'plurals':
                resName = ResourceNameRef('', ResourceType.kPlurals, name)
                error |= not self.parsePlural(parser, resName)
            elif elementName == 'array':
                resName = ResourceNameRef('', ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_ANY)
            elif elementName == 'string-array':
                resName = ResourceNameRef('', ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_STRING)
            elif elementName == 'integer-array':
                resName = ResourceNameRef('', ResourceType.kArray, name)
                error |= not self.parseArray(parser, resName, ResTable_map.TYPE_INTEGER)
            elif elementName == 'public':
                error |= not self.parsePublic(parser, name)
            elif elementName == 'declare-styleable':
                resName = ResourceNameRef('', ResourceType.kStyleable, name)
                error |= not self.parseDeclareStyleable(parser, resName)
            elif elementName == 'attr':
                resName = ResourceNameRef('', ResourceType.kAttr, name)
                error |= not self.parseAttr(parser, resName)
            else:
                errMessage = 'WARNING %s:%s unknown resource type "%s"'
                self._retDiag(errMessage % (self.mSource, parser.getLineNumber(), elementName))
            if not error and comment:
                srchResult = self.mTable.findResource(resName)
                entry = srchResult.entry
                pos = self.mTable._getValueForConfig(entry, self.mConfig)
                if pos != -1:
                    if elementName != 'public':
                        entry.values[pos] = entry.values[pos]._replace(comment=comment)
                    else:
                        ps = entry.values[pos].publicStatus._replace(comment=comment)
                        entry.values[pos] = entry.values[pos]._replace(publicStatus=ps)
                comment = ''
        return not error

    def parseColor(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeProduct = parser.getAttributeValue('', 'product')
        if maybeProduct and maybeProduct not in ('default', 'phone'):
            return True
        processedItem = self.parseXml(parser, ResTable_map.TYPE_COLOR, kNoRawString)
        if not processedItem:
            errMessage = 'invalid color'
            self._retDiag('ERROR ' + source + errMessage)
            return False
        return self.mTable.addResource(resourceName, self.mConfig, source, processedItem)

    def parseString(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        processedItem = self.parseXml(parser, ResTable_map.TYPE_STRING, kNoRawString)
        if not processedItem:
            errMessage = 'not a valid string'
            self._retDiag('ERROR ' + source + errMessage)
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
            self._retDiag('ERROR ' + source + errMessage)
            return False
        return self.mTable.addResource(resourceName, self.mConfig, source, item)

    def parsePublic(self, parser, name):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeType = parser.getAttributeValue('', 'type')
        if not maybeType:
            errMessage = '<public> must have a "type" attribute'
            self._retDiag('ERROR ' + source + errMessage)
            return False
        parsedType = ResourceType.parseResourceType(maybeType)
        if not parsedType:
            errMessage = 'invalid resource type "%s" in <public>' % maybeType
            self._retDiag('ERROR ' + source + errMessage)
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
                self._retDiag('ERROR ' + source + errMessage)
                return False
        if parsedType == ResourceType.kId:
            self.mTable.addResource(resourceName, None, source, Id())
        return self.mTable.markPublic(resourceName, resourceId, source, self.mDiag)

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
            typeMask = reduce(trnFcn, maybeFormat.split('|'), 0)
            if not typeMask:
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                source += 'invalid attribute format "%s"' % maybeFormat
                self._retDiag('ERROR ' + source)
                return None
        if weak and not maybeFormat:
            suffix = resourceName.entry
            package, suffix = suffix.split(':') if ':' in suffix else ('', suffix)
            atype, suffix = suffix.split('/') if '/' in suffix else ('', suffix)
            name = suffix
            if not atype and package:
                resourceName.package = package
                resourceName.entry = name
        items = []
        error = False
        depth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() >= depth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if not elementNamespace and elementName in ['flag', 'enum']:
                if elementName == 'enum':
                    if typeMask & ResTable_map.TYPE_FLAGS:
                        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                        source += 'can not define an <enum>; already defined a <flag>'
                        self._retDiag('ERROR ' + source)
                        error = True
                        continue
                    typeMask |= ResTable_map.TYPE_ENUM
                elif elementName == 'flag':
                    if typeMask & ResTable_map.TYPE_ENUM:
                        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                        source += 'can not define an <flag>; already defined a <enum>'
                        self._retDiag('ERROR ' + source)
                        error = True
                        continue
                    typeMask |= ResTable_map.TYPE_FLAGS
                s = self.parseEnumOrFlagItem(parser, elementName)
                if s and self.mTable.addResource(s.symbol.name, self.mConfig, '%s:%s ' % (self.mSource, parser.getLineNumber()), Id()):
                    items.append(s)
                else:
                    error = True
            elif elementName in ('skip', 'eat-comment'):
                continue
            else:
                source = '%s:%s ' % (self.mSource, parser.getLineNumber())
                source += '<%s>' % elementName
                self._retDiag('ERROR ' + source)
                error = True
        if error: return None
        attr = Attribute(weak)
        attr.symbols = items
        attr.typeMask = typeMask if typeMask else ResTable_map.TYPE_ANY
        return attr

    def parseEnumOrFlagItem(self, parser, tag):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeName = parser.getAttributeValue('', 'name')
        if not maybeName:
            source += 'no attribute "name" found for tag <%s>' % tag
            self._retDiag('ERROR ' + source)
            return None
        maybeValue = parser.getAttributeValue('', 'value')
        if not maybeValue:
            source += 'no attribute "value" found for tag <%s>' % tag
            self._retDiag('ERROR ' + source)
            return None

        val = Res_value()
        if not u16stringToInt(maybeValue, val): # ResourcesTypes.u16stringToInt
            source += 'invalid value "%s" for tag <%s>; must be integer' % (maybeValue, tag)
            self._retDiag('ERROR ' + source)
            return None

        resName = ResourceNameRef('', ResourceType.kId, maybeName)
        ref = Reference(resName)
        return Attribute.Symbol(ref, val.data)

    def parseStyle(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        style = Style()
        maybeParent = parser.getAttributeValue('', 'parent')
        if maybeParent is not None:
            if maybeParent:
                errStr = ObjRef('')
                style.parent = ResourceUtils.parseStyleParentReference(maybeParent, errStr)
                if not style.parent:
                    source += errStr._value
                    self._retDiag('ERROR ' + source)
                    return False
                resName = style.parent.name
                transformedName = self.transformPackage(parser, resName, '')
                if transformedName: style.parent.name = transformedName
        else:
            styleName = resourceName.entry
            pos = styleName.rfind('.')
            if pos != -1:
                style.parentInferred = True
                style.parent = Reference(ResourceNameRef('', ResourceType.kStyle, styleName[:pos]))
        error = False
        depth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() >= depth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                error |= not self.parseStyleItem(parser, style)
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                pass
            else:
                errMessage = '%s:%s ' % (self.mSource, parser.getLineNumber())
                errMessage += ':%s>' % elementName
                self._retDiag('ERROR ' + errMessage)
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, style)

    def parseStyleItem(self, parser, style):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        maybeName = parser.getAttributeValue('', 'name')
        if not maybeName:
            source += '<item> must have a "name" attribute'
            self._retDiag('ERROR ' + source)
            return False
        maybeKey = self.parseXmlAttributeName(maybeName)
        if not maybeKey:
            source += 'invalid attribute name "%s"' % maybeName
            self._retDiag('ERROR ' + source)
            return False
        transformedName = self.transformPackage(parser, maybeKey, u"")
        if transformedName: maybeKey = transformedName
        value = self.parseXml(parser, 0, kAllowRawString)
        if not  value:
            source += 'could not parse style item'
            self._retDiag('ERROR ' + source)
            return False
        maybeKey = ResourceNameRef(maybeKey)
        style.entries.append(Style.Entry(Reference(maybeKey), value))
        return True


    @staticmethod
    def parseXmlAttributeName(aStr):
        package, name = aStr.strip().split(':') if ':' in aStr else ('', aStr)
        return ResourceName(package, ResourceType.kAttr, name)

    @staticmethod
    def transformPackage(parser, resName, package):
        if resName:
            if not resName.package:
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
        depth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() > depth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'attr':
                maybeName = parser.getAttributeValue('', 'name')
                if not maybeName:
                    source += '<attr> tag must have a "name" attribute'
                    self._retDiag('ERROR ' + source)
                    error = True
                    continue
                attrResourceName = ResourceName('', ResourceType.kAttr, maybeName)
                attr = self.parseAttrImpl(parser, attrResourceName, True)
                if not attr:
                    error = True
                    continue
                styleable.entries.append(Reference(ResourceNameRef(attrResourceName)))
                error |= not self.mTable.addResource(attrResourceName, self.mConfig, source, attr)
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                pass
            else:
                source += 'unknown tag <%s>' % elementName
                self._retDiag('ERROR ' + source)
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, styleable)

    def parseArray(self, parser, resourceName, typeMask):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        array = Array()
        error = False
        depth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() > depth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if parser.getEventType() != parser.START_TAG: continue
            itemSource = '%s:%s ' % (self.mSource, parser.getLineNumber())
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                item = self.parseXml(parser,typeMask, kNoRawString)
                if not item:
                    itemSource += 'could not parse array item'
                    self._retDiag('ERROR ' + source)
                    error = True
                    continue
                array.items.append(item)
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                pass
            else:
                source += 'unknown tag <%s>' % elementName
                self._retDiag('ERROR ' + source)
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, array)

    def parsePlural(self, parser, resourceName):
        source = '%s:%s ' % (self.mSource, parser.getLineNumber())
        plural = Plural()
        error = False
        depth = parser.getDepth()
        while True:
            event = parser.next()
            bFlag = (event != parser.END_TAG or parser.getDepth() > depth)
            bFlag = bFlag and event != parser.END_DOCUMENT
            if  not bFlag: break
            if parser.getEventType() != parser.START_TAG: continue
            elementNamespace = parser.getNamespace()
            elementName = parser.getName()
            if elementNamespace == '' and elementName == 'item':
                maybeQuantity = parser.getAttributeValue('', 'quantity')
                if not maybeQuantity:
                    source += '<item> in <plurals> requires attribute "quantity"'
                    self._retDiag('ERROR ' + source)
                    error = True
                    continue
                trimmedQuantity = maybeQuantity.strip()
                if hasattr(Plural, trimmedQuantity.title()):
                    index = getattr(Plural, trimmedQuantity.title())
                else:
                    errMessage = '<item> in <plural> has invalid value "%s"  for attribute "quantity"'
                    self._retDiag('ERROR ' + source + errMessage % trimmedQuantity)
                    error = True
                    continue
                if plural.values.has_key(index):
                    errMessage = 'duplicate quantity "%s"'
                    self._retDiag('ERROR ' + source + errMessage % trimmedQuantity)
                    error = True
                    continue
                plural.values[index] = val = self.parseXml(parser, ResTable_map.TYPE_STRING, kNoRawString)
                if not val:
                    error = True
            elif elementNamespace == '' and elementName in ('skip', 'eat-comment'):
                pass
            else:
                errMessage = 'unknown tag <%s>' % elementName
                self._retDiag('ERROR ' + source + errMessage)
                error = True
        if error: return False
        return self.mTable.addResource(resourceName, self.mConfig, source, plural)
