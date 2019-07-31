# -*- coding: utf-8 -*-
import itertools

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Resource import ResourceType, ResourceNameRef, SourcedResourceName


class IdCollector(object):

    def __init__(self, outSymbols):
        super(IdCollector, self).__init__()
        self.mOutSymbols = outSymbols

    def visit(self, arg):
        if isinstance(arg, tuple):
            attributes = [(arg.value, arg.lineNumber)]
        else:
            attributes = [
                (arg.getAttributeValue(k), arg.getLineNumber())
                for k in xrange(arg.getAttributeCount())
            ]
        for attrValue, attrLinenumber in attributes:
            name = ResourceNameRef()
            create = ResourceUtils.ObjRef(False)
            if ResourceUtils.tryParseReferenceB(attrValue, name, create, None):
                if create._value and name.type == ResourceType.kId:
                    npos = len(self.mOutSymbols)
                    it = itertools.dropwhile(
                        lambda x, name=name: self.mOutSymbols[x].name < name,
                        xrange(npos)
                    )
                    try:
                        pos = it.next()
                        if self.mOutSymbols[pos].name == name:
                            return
                    except:
                        pos = npos
                    self.mOutSymbols.insert(
                        pos,
                        SourcedResourceName(
                            name.toResourceName(),
                            attrLinenumber
                        )
                    )


class XmlIdCollector(object):

    def consume(self, context, xmlRes):
        xmlRes.file.exportedSymbols = []
        collector = IdCollector(xmlRes.file.exportedSymbols)
        parser = xmlRes.parser
        while True:
            try:
                etype = parser.nextTag()
                if etype == parser.START_TAG:
                    collector.visit(parser)
            except:
                break
        return True