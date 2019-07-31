# -*- coding: utf-8 -*-
from Tools.aapt.StringPool import StringPool
from Tools.aapt.flatten.ChunkWriter import ChunkWriter
from Tools.aapt.ResourceTypeExtensions import RES_FILE_EXPORT_TYPE, FileExport_header, ExportedSymbol

class Source(object):
    def __init__(self, path='', line=None):
        super(Source, self).__init__()
        self.path = path
        self.line = line

    def withLine(self, line):
        return self.__class__(self.path, line)


def wrapBufferWithFileExportHeader(buffer, res):
    fileExportWriter = ChunkWriter(buffer)
    fileExport = fileExportWriter.startChunk(RES_FILE_EXPORT_TYPE, FileExport_header)
    symbolRefs = None
    if res.exportedSymbols:
        symbolRefs = fileExportWriter.nextBlock(
            ExportedSymbol,
            len(res.exportedSymbols)
        )
    fileExport.exportedSymbolCount = len(res.exportedSymbols)
    symbolExportPool = StringPool()
    fileExport.magic = "AAPT"
    fileExport.config = res.config
    # fileExport.config.swapHtoD()
    fileExport.name.index = symbolExportPool.makeRef(res.name.toString()).getIndex()
    fileExport.source.index = symbolExportPool.makeRef(res.source.path).getIndex()
    for k, name in enumerate(res.exportedSymbols):
        symbolRefs[k].name.index = symbolExportPool.makeRef(name.name.toString()).getIndex()
        symbolRefs[k].line = name.line
    StringPool.flattenUtf16(symbolExportPool, fileExportWriter.getBuffer())
    return fileExportWriter