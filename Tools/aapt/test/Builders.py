# -*- coding: utf-8 -*-
#
# ported from:
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/test/Builders.h
#
from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.Resource import ResourceId, ResourceName, ResourceType
from Tools.aapt.ResourcesTypes import ResTable_map
from Tools.aapt.test.Common import parseNameOrDie
from Tools.aapt.ResourcesValues import Attribute, Reference, String, FileReference, Id, Styleable, Style


class ResourceTableBuilder(object):

    def __init__(self):
        super(ResourceTableBuilder, self).__init__()
        self.mDiagnostics = ResourceUtils.Diagnostics()
        self.mTable = ResourceTable()
    
    def setPackageId(self, packageName, id):
        package = self.mTable.createPackage(packageName, id)
        assert package
        return self

    def addSimple(self, name, id=None):
        id = id or ResourceId()
        return self.addValue(name, id, Id())
    
    def addReference(self, *args):
        id = None
        if len(args) == 2:
            name, ref = args
        else:
            name, id, ref = args
        return self.addValue(name, id, Reference(parseNameOrDie(ref)))
    
    def addString(self, *args):
        id = None
        if len(args) == 2:
            name, astr = args
        else:
            name, id, astr = args
        return self.addValue(name, id, String(self.mTable.stringPool.makeRef(astr)))
    
    def addFileReference(self, *args):
        id = None
        if len(args) == 2:
            name, path = args
        else:
            name, id, path = args
        return self.addValue(name, id, FileReference(self.mTable.stringPool.makeRef(path)))
    
    def addValue(self, *args):
        id = config = None
        if len(args) == 2:
            name, value = args
        elif len(args) == 3:
            name, id, value = args
        elif len(args) == 4:
            name, id, config, value = args
        result = self.mTable.addResource(
            parseNameOrDie(name), config, '', value, id, self.mDiagnostics
        )
        assert result
        return self
    
    def build(self):
        return self.mTable
    

def buildReference(ref, id=None):
    reference = Reference(parseNameOrDie(ref))
    reference.id = id or ResourceId()
    return reference


class AttributeBuilder(object):

    def __init__(self, weak=False):
        super(AttributeBuilder, self).__init__()
        self.mAttr = Attribute(weak)
        self.mAttr.typeMask = ResTable_map.TYPE_ANY
    
    def setTypeMask(self, typeMask):
        self.mAttr.typeMask = typeMask
        return self
    
    def addItem(self, name, value):
        self.mAttr.symbols.append(
            Attribute.Symbol(
                Reference(
                    ResourceName(None, ResourceType.kId, name),
                    value
                )
            )
        )
        return self
    
    def build(self):
        return self.mAttr
    

class StyleBuilder(object):

    def __init__(self):
        super(StyleBuilder, self).__init__()
        self.mStyle = Style()

    def setParent(self, astr):
        self.mStyle.parent = Reference(parseNameOrDie(astr))
        return self
    
    def addItem(self, astr, value, id=None):
        self.mStyle.entries.append(
            Style.Entry(Reference(parseNameOrDie(astr)), value)
        )
        self.mStyle.entries[-1].key.id = id
        return self
    
    def build(self):
        return self.mStyle
    

class StyleableBuilder(object):

    def __init__(self):
        super(StyleableBuilder, self).__init__()
        self.mStyleable = Styleable()

    def addItem(self, astr, id):
        self.mStyleable.entries.append(Reference(parseNameOrDie(astr)))
        self.mStyleable.entries[-1].id = id
        return self
    
    def build(self):
        return self.mStyleable
    

def buildXmlDom(astr):
    strin = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    strin += astr
    # XmlResource(doc = xml::inflate(&in, &diag, {)
    doc = strin
    assert doc
    return doc
