# -*- coding: utf-8 -*-
from ctypes import *
import collections

from Tools.aapt.Compile.ResourceUtils import ObjRef
from Tools.aapt.SdkConstants import findAttributeSdkLevel
from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.Compile.XmlIdCollector import XmlIdCollector, IdCollector
from Tools.aapt.Resource import ResourceId
from Tools.aapt.ResourcesTypes import ResStringPool_ref, \
    ResXMLTree_namespaceExt, Res_value, ResXMLTree_node, \
    ResXMLTree_cdataExt, ResXMLTree_attrExt, ResXMLTree_attribute, \
    ResXMLTree_endElementExt, ResXMLTree_header
from Tools.aapt.StringPool import StringPool
from Tools.aapt.flatten.ChunkWriter import ChunkWriter
from Tools.aapt.ResourcesTypes import ResChunk_header
from Tools.aapt.flatten.FileExportWriter import wrapBufferWithFileExportHeader


XmlFlattenerOptions = collections.namedtuple('XmlFlattenerOptions', 'keepRawValues maxSdkLevel')
XmlFlattenerOptions.__new__.func_defaults = (False, None)

kLowPriority = 0xffffffff


class XmlFlattenerVisitor(object):

    START_NAMESPACE = 0x110
    END_NAMESPACE = 0x111

    StringFlattenDest = collections.namedtuple('StringFlattenDest', 'ref dest')

    def __init__(self, buffer, options, idcollector):
        super(XmlFlattenerVisitor, self).__init__()
        self.mBuffer = buffer
        self.mOptions = options
        self.idcollector = idcollector
        self.mPool = StringPool()
        self.mPackagePools = {}
        self.mStringRefs = []
        # Scratch vector to filter attributes. We avoid allocations
        # making this a member.
        self.mFilteredAttrs = []
        self.nsStack = []
        self.eventBuffer = collections.deque()

    def addString(self, aStr, priority, dest):
        if aStr:
            strFlatttenDest = XmlFlattenerVisitor.StringFlattenDest(
                self.mPool.makeRef(aStr, StringPool.Context(priority)),
                dest
            )
            self.mStringRefs.append(strFlatttenDest)
        else:
            # The device doesn't think a string of size 0 is the same as null.
            dest.index = -1

    def addStringRef(self, ref, dest):
        self.mStringRefs.append(XmlFlattenerVisitor.StringFlattenDest(ref, dest))

    def writeNamespace(self, node, atype):
        writer = ChunkWriter(self.mBuffer)
        flatNode = writer.startChunk(atype, ResXMLTree_node)
        flatNode.lineNumber = node.lineNumber
        flatNode.comment.index = -1
        flatNs = writer.nextBlock(ResXMLTree_namespaceExt)
        self.addString(node.namespacePrefix, kLowPriority, flatNs.prefix)
        self.addString(node.namespaceUri, kLowPriority, flatNs.uri)
        writer.finish()
    
    def visitStartNamespace(self, parser):
        for ns in self.namespace(parser):
            self.writeNamespace(ns, ResChunk_header.RES_XML_START_NAMESPACE_TYPE)

    def visitEndNamespace(self, parser):
        for ns in self.namespace(parser):
            self.writeNamespace(ns, ResChunk_header.RES_XML_END_NAMESPACE_TYPE)

    def visitText(self, parser):
        if parser.isWhitespace():
            # Skip whitespace only text nodes.
            return
        writer = ChunkWriter(self.mBuffer)
        flatNode = writer.startChunk(ResChunk_header.RES_XML_CDATA_TYPE, ResXMLTree_node)
        flatNode.lineNumber = parser.getLineNumber()
        flatNode.comment.index = -1
        flatText = writer.nextBlock(ResXMLTree_cdataExt)
        self.addString(parser.getText(), kLowPriority, flatText.data)
        writer.finish()

    def visitStartElement(self, parser):
        startWriter= ChunkWriter(self.mBuffer)
        flatNode = startWriter.startChunk(
            ResChunk_header.RES_XML_START_ELEMENT_TYPE,
            ResXMLTree_node
        )
        flatNode.lineNumber = parser.getLineNumber()
        flatNode.comment.index = -1
        flatElem = startWriter.nextBlock(ResXMLTree_attrExt)
        self.addString(parser.getNamespace(), kLowPriority, flatElem.ns)
        self.addString(parser.getName(), kLowPriority, flatElem.name)
        flatElem.attributeStart = sizeof(flatElem)
        flatElem.attributeSize = sizeof(ResXMLTree_attribute)
        self.writeAttributes(parser, flatElem, startWriter)
        startWriter.finish()

    def visitEndElement(self, parser):
        endWriter = ChunkWriter(self.mBuffer)
        flatEndNode = endWriter.startChunk(
            ResChunk_header.RES_XML_END_ELEMENT_TYPE,
            ResXMLTree_node
        )
        flatEndNode.lineNumber = parser.getLineNumber()
        flatEndNode.comment.index = -1
        flatEndElem = endWriter.nextBlock(ResXMLTree_endElementExt)
        self.addString(parser.getNamespace(), kLowPriority, flatEndElem.ns)
        self.addString(parser.getName(), kLowPriority, flatEndElem.name)
        endWriter.finish()

    def cmpXmlAttributeById(self, attra, attrb):
        if attra.compiledAttribute:
            if attrb.compiledAttribute:
                return cmp(attra.compiledAttribute.id, attrb.compiledAttribute.id)
            return -1
        elif not attrb.compiledAttribute:
            diff = cmp(attra.namespaceUri, attrb.namespaceUri)
            if diff:
                return diff
            return cmp(attra.name, attrb.name)
        return 1

    def writeAttributes(self, parser, flatElem, writer):
        self.mFilteredAttrs = []
        # Filter the attributes.
        for attr in self.attributes(parser):
            if self.mOptions.maxSdkLevel and attr.compiledAttribute:
                sdkLevel = findAttributeSdkLevel(attr.compiledAttribute.id)
                if sdkLevel > self.mOptions.maxSdkLevel:
                    continue
            self.mFilteredAttrs.append(attr)
        if not self.mFilteredAttrs:
            return
        kIdAttr = ResourceId(0x010100d0)
        self.mFilteredAttrs.sort(cmp=self.cmpXmlAttributeById)
        flatElem.attributeCount = len(self.mFilteredAttrs)
        it = iter(writer.nextBlock(ResXMLTree_attribute, flatElem.attributeCount))
        for attributeIndex, xmlAttr in enumerate(self.mFilteredAttrs):
            flatAttr = it.next()
            # Assign the indices for specific attributes.
            if xmlAttr.compiledAttribute and xmlAttr.compiledAttribute.id == kIdAttr:
                flatElem.idIndex = attributeIndex
            elif not xmlAttr.namespaceUri:
                if xmlAttr.name == u"class":
                    flatElem.classIndex = attributeIndex
                elif xmlAttr.name == u"style":
                    flatElem.styleIndex = attributeIndex
            # Add the namespaceUri to the list of StringRefs to encode.
            self.addString(xmlAttr.namespaceUri, kLowPriority, flatAttr.ns)
            flatAttr.rawValue.index = -1
            if not xmlAttr.compiledAttribute:
                # The attribute has no associated ResourceID, so the string order doesn't matter.
                self.addString(xmlAttr.name, kLowPriority, flatAttr.name)
            else:
                # Attribute names are stored without packages, but we use
                # their StringPool index to lookup their resource IDs.
                # This will cause collisions, so we can't dedupe
                # attribute names from different packages. We use separate
                # pools that we later combine.
                #
                # Lookup the StringPool for this package and make the reference there.
                aaptAttr = xmlAttr.compiledAttribute
                nameRef = self.mPackagePools[aaptAttr.id.packageId()].makeRef(
                        xmlAttr.name, StringPool.Context(aaptAttr.id.id )
                )
                # Add it to the list of strings to flatten.
                self.addStringRef(nameRef, flatAttr.name)
                if self.mOptions.keepRawValues:
                    # Keep raw values (this is for static libraries).
                    # TODO(with a smarter inflater for binary XML, we can do without this).
                    self.addString(xmlAttr.value, kLowPriority, flatAttr.rawValue)
            if xmlAttr.compiledValue:
                result = xmlAttr.compiledValue.flatten(flatAttr.typedValue)
                assert result
            else:
                # Flatten as a regular string type.
                flatAttr.typedValue.dataType = Res_value.TYPE_STRING
                self.addString(xmlAttr.value, kLowPriority, flatAttr.rawValue)
                self.addString(xmlAttr.value, kLowPriority, flatAttr.typedValue)
            flatAttr.typedValue.size = sizeof(flatAttr.typedValue)

    def parse(self, parser):
        error = False
        comment = ''
        startDepth = parser.getDepth()
        wparser = self._parserWrapper(parser)
        while True:
            case = wparser.next()
            bFlag = parser.getDepth() >= startDepth and case != parser.END_DOCUMENT
            if not bFlag: break
            if case == self.START_NAMESPACE:
                self.visitStartNamespace(parser)
            elif case == parser.START_TAG:
                self.visitStartElement(parser)
            elif case == parser.END_TAG:
                self.visitEndElement(parser)
            elif case == self.END_NAMESPACE:
                self.visitEndNamespace(parser)
            elif case == parser.TEXT:
                self.visitText(parser)
        return True

    def attributes(self, parser):
        AttrNode = collections.namedtuple('AttrNode', 'namespaceUri '
                                                      'name '
                                                      'value '
                                                      'lineNumber '
                                                      'columnNumber '
                                                      'comment '
                                                      'compiledAttribute '
                                                      'compiledValue')
        for k in xrange(parser.getAttributeCount()):
            an = AttrNode(parser.getAttributeNamespace(k),
                          parser.getAttributeName(k),
                          parser.getAttributeValue(k),
                          parser.getLineNumber(),
                          parser.getColumnNumber(),
                          '',
                          None,
                          None)
            self.idcollector.visit(an)
            yield an

    def namespace(self, parser):
        NamespaceNode = collections.namedtuple('NamespaceNode', 'namespacePrefix '
                                                                'namespaceUri '
                                                                'lineNumber '
                                                                'columnNumber '
                                                                'comment')
        if parser.getEventType() == parser.START_TAG:
            nsStart = parser.getNamespaceCount(parser.getDepth()-1)
            nsEnd = parser.getNamespaceCount(parser.getDepth())
        else:
            assert parser.getEventType() == parser.END_TAG
            nsStart = parser.getNamespaceCount(parser.getDepth())
            nsEnd = parser.getNamespaceCount(parser.getDepth()+1)
        for k in xrange(nsStart, nsEnd):
            nsn = NamespaceNode(parser.getNamespacePrefix(k),
                                parser.getNamespaceUri(k),
                                parser.getLineNumber(),
                                parser.getColumnNumber(),
                                '')
            yield nsn


    def _parserWrapper(self, parser):
        while True:
            try:
                eventType = parser.next()
            except:
                break
            if eventType == parser.START_TAG:
                depth = parser.getDepth()
                if parser.getNamespaceCount(depth - 1) < parser.getNamespaceCount(depth):
                    yield self.START_NAMESPACE
            yield eventType
            if eventType == parser.END_TAG:
                depth = parser.getDepth()
                if parser.getNamespaceCount(depth) < parser.getNamespaceCount(depth + 1):
                    yield self.END_NAMESPACE



class XmlFlattener(object):

    def __init__(self, buffer, options):
        super(XmlFlattener, self).__init__()
        self.mBuffer = buffer
        self.mOptions = options

    def consume(self, context, resource, linker=None):
        if not resource or not resource.parser:
            return False
        if not self.flatten(context, resource, linker):
            return False
        return True


    def flatten(self, context, resource, linker):
        collector = IdCollector(resource.file.exportedSymbols)
        parser = resource.parser
        nodeBuffer = BigBuffer(1024)
        visitor = XmlFlattenerVisitor(nodeBuffer, self.mOptions, collector)
        if not visitor.parse(parser):
            return False

        fileExportWriter = wrapBufferWithFileExportHeader(self.mBuffer, resource.file)

        # Merge the package pools into the main pool.
        for packagePoolEntry in visitor.mPackagePools.itervalues():
            visitor.mPool.merge(packagePoolEntry)
        # Sort the string pool so that attribute resource IDs show up first.
        visitor.mPool.sort(lambda x, y: cmp(x.context.priority, y.context.priority))
        # Now we flatten the string pool references into the correct places.
        for refEntry in visitor.mStringRefs:
            if isinstance(refEntry.dest, Res_value):
                refEntry.dest.data = refEntry.ref.getIndex()
            else:
                refEntry.dest.index = refEntry.ref.getIndex()
        # Write the XML header.
        xmlHeaderWriter = ChunkWriter(self.mBuffer)
        xmlHeaderWriter.startChunk(ResChunk_header.RES_XML_TYPE, ResXMLTree_header)
        # Flatten the StringPool.
        StringPool.flattenUtf16(visitor.mPool, self.mBuffer)
        # Write the array of resource IDs, indexed by StringPool order.
        resIdMapWriter = ChunkWriter(self.mBuffer)
        resIdMapWriter.startChunk(
            ResChunk_header.RES_XML_RESOURCE_MAP_TYPE,
            ResChunk_header
        )
        for astr in visitor.mPool:
            id = ResourceId(astr.context.priority)
            if id.id == kLowPriority or not id.isValid():
                # When we see the first non-resource ID,
                # we're done.
                break
            resIdMapWriter.nextBlock(c_uint32).value = id.id;
        resIdMapWriter.finish()
        # Move the nodeBuffer and append it to the out buffer.
        self.mBuffer.appendBuffer(nodeBuffer)
        # Finish the xml header.
        xmlHeaderWriter.finish()
        fileExportWriter.finish()
        return True
