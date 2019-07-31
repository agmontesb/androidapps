# -*- coding: utf-8 -*-
#
# Ported from
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/compile/Compile.cpp
#
import os
import collections

from Tools.aapt.BigBuffer import BigBuffer
from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.Compile.IdAssigner import IdAssigner
from Tools.aapt.Compile.ResourceParser import ResourceParser
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.flatten.XmlFlattener import XmlFlattenerOptions, XmlFlattener
from Tools.aapt.Compile.XmlIdCollector import XmlIdCollector
from Tools.aapt.ConfigDescription import ConfigDescription
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory
from Tools.aapt.Resource import ResourceType, ResourceName
from Tools.aapt.flatten.FileExportWriter import wrapBufferWithFileExportHeader, Source
from Tools.aapt.flatten.TableFlattener import TableFlattenerOptions, TableFlattener
from Tools.aapt.Flags import Flags
from Tools.aapt.Resource import ResourceFile, ResourceType


ResourcePathData = collections.namedtuple('ResourcePathData', 'source resourceDir name extension configStr config')

'''
/**
 * Resource file paths are expected to look like:
 * [--/res/]type[-config]/name
 */
 '''
def extractResourcePathData(path, errorStr):
    dirStr = os.path.basename(os.path.dirname(path))
    if not dirStr:
        raise NameError("bad resource path")
    try:
        dirStr, configStr = dirStr.split('-', 1)
    except:
        configStr = ''
    config = ConfigDescription()
    if configStr:
        try:
            if not ConfigDescription.parse(configStr, config):
                return None
        except Exception as e:
            raise Exception('invalid configuration "%s"' % configStr)
    basename = os.path.basename(path)
    name, extension = os.path.splitext(basename)
    return ResourcePathData(
        Source(path),
        dirStr,
        name,
        extension[1:],
        configStr,
        config
    )

CompileOptions = collections.namedtuple('CompileOptions', 'outputPath verbose')

def buildIntermediateFilename(outDir, data):
    name = data.resourceDir
    if data.configStr:
        name += '-' + data.configStr
    name += '_' + data.name + '.' + data.extension + '.flat'
    return os.path.join(outDir, name)

def compileTable(context, options, pathData, outputPath):
    table = ResourceTable()
    table.createPackage('', 0x7f)

    if not os.path.exists(pathData.source.path):
        errMessage = '"%s" not such path exits' % pathData.source.path
        print errMessage
        return False

    factory = XmlPullParserFactory.newInstance()
    factory.setNamespaceAware(True)
    assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
    assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    xmlParser = factory.newPullParser()
    try:
        xmlParser.setInput(pathData.source.path, None)
    except:
        return False

    resParser = ResourceParser(context.getDiagnostics(), table, pathData.source.path, pathData.config)
    if not resParser.parse(xmlParser):
        return False

    idAssigner = IdAssigner()
    if not idAssigner.consume(context, table):
        return False

    buffer = BigBuffer(1024)
    tableFlattenerOptions = TableFlattenerOptions()._replace(useExtendedChunks=True)
    flattener = TableFlattener(buffer, tableFlattenerOptions)
    if not flattener.consume(context, table):
        return False
    with open(outputPath, 'wb') as fout:
        try:
            for block in buffer:
                size = block.size
                fout.write(block.buffer[:size])
        except Exception as e:
            print e.message
            return False
    return True


def compileXml(context, options, pathData, outputPath):
    if not os.path.exists(pathData.source.path):
        errMessage = '"%s" not such path exits' % pathData.source.path
        print errMessage
        return False

    factory = XmlPullParserFactory.newInstance()
    factory.setNamespaceAware(True)
    assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
    assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    ResXml = collections.namedtuple('ResXml', 'file parser')
    xmlParser = factory.newPullParser()
    try:
        xmlParser.setInput(pathData.source.path, None)
    except:
        return False

    resXml = ResXml(ResourceFile(), xmlParser)
    resXml.file.name = ResourceName(
        None,
        ResourceType.parseResourceType(pathData.resourceDir),
        pathData.name
    )
    resXml.file.config = pathData.config
    resXml.file.source = pathData.source
    buffer = BigBuffer(1024)
    xmlFlattenerOptions = XmlFlattenerOptions()._replace(keepRawValues=True)
    flattener = XmlFlattener(buffer, xmlFlattenerOptions)
    if not flattener.consume(context, resXml):
        return False

    with open(outputPath, 'wb') as fout:
        try:
            for block in buffer:
                size = block.size
                fout.write(block.buffer[:size])
        except Exception as e:
            print e.message
            return False
    return True


def compilePng(context, options, pathData, outputPath):
    if not os.path.exists(pathData):
        errMessage = '"%s" not such path exits' % pathData.source
        print errMessage
        return False

    buffer = BigBuffer(4096)
    resFile = ResourceFile()
    resFile.name = ResourceName(
        None,
        ResourceType.parseResourceType(pathData.resourceDir),
        pathData.name
    )
    resFile.config = pathData.config
    resFile.source = pathData.source
    fileExportWriter = wrapBufferWithFileExportHeader(buffer, resFile)
    png = Png(context.getDiagnostics())
    with open(pathData.source.path, 'rb') as fin:
        if not png.process(pathData.source, fin, fileExportWriter.getBuffer(), None):
            return False
    fileExportWriter.finish()

    #  Write it to disk.
    with open(outputPath, 'wb') as fout:
        try:
            for block in buffer:
                size = block.size
                fout.write(block.buffer[:size])
        except Exception as e:
            print e.message
            return False
    return True

    if not os.path.exists(pathData):
        errMessage = '"%s" not such path exits' % pathData.source
        print errMessage
        return False

    buffer = BigBuffer(4096)
    resFile = ResourceFile()
    resFile.name = ResourceName(
        None,
        ResourceType.parseResourceType(pathData.resourceDir),
        pathData.name
    )
    resFile.config = pathData.config
    resFile.source = pathData.source
    fileExportWriter = wrapBufferWithFileExportHeader(buffer, resFile)
    png = Png(context.getDiagnostics())
    with open(pathData.source.path, 'rb') as fin:
        if not png.process(pathData.source, fin, fileExportWriter.getBuffer(), None):
            return False
    fileExportWriter.finish()

    #  Write it to disk.
    with open(outputPath, 'wb') as fout:
        try:
            for block in buffer:
                size = block.size
                fout.write(block.buffer[:size])
        except Exception as e:
            print e.message
            return False
    return True


def compileFile(context, options, pathData, outputPath):
    if not os.path.exists(pathData.source.path):
        errMessage = '"%s" not such path exits' % pathData.source.path
        print errMessage
        return False

    buffer = BigBuffer(256)
    resFile = ResourceFile()
    resFile.name = ResourceName(
        None,
        ResourceType.parseResourceType(pathData.resourceDir),
        pathData.name
    )
    resFile.config = pathData.config
    resFile.source = pathData.source
    fileExportWriter = wrapBufferWithFileExportHeader(buffer, resFile)
    filesize = os.path.getsize(pathData.source.path)
    # Manually set the size and don't call finish(). This is because we are not copying from
    # the buffer the entire file.
    fileExportWriter.getChunkHeader().size = buffer.size() + filesize

    #  Write it to disk.
    with open(outputPath, 'wb') as fout:
        try:
            for block in buffer:
                size = block.size
                fout.write(block.buffer[:size])
            with open(pathData.source.path, 'rb') as fin:
                fout.write(fin.read())
        except Exception as e:
            print e.message
            return False
    return True


class CompileContext(object):

    def __init__(self):
        super(CompileContext, self).__init__()
        self.mDiagnostics = ResourceUtils.Diagnostics()

    def getExternalSymbols(self):
        pass

    def getDiagnostics(self):
        return self.mDiagnostics

    def getCompilationPackage(self):
        return ''

    def getPackageId(self):
        return 0x7F

    def getNameMangler(self):
        pass


def compile(*args):
    #
    #  Entry point for compilation phase. Parses arguments and dispatches to the correct steps.
    #

    context = CompileContext()
    options = Flags() \
            .requiredFlag("-o", "Output path", 'outputPath') \
            .optionalSwitch("-v", "Enables verbose logging", 'verbose')
    if not options.parse("aapt2 compile", args, context.getDiagnostics()):
        print context.getDiagnostics().error
        return 1

    inputData = []
    #  Collect data from the path for each input file.
    for arg in options.getArgs():
        errorStr = ''
        pathData = extractResourcePathData(arg, errorStr)
        if pathData:
            inputData.append(pathData)
        else:
            context.getDiagnostics().error = errorStr + " (" + str(arg) + ")"
            return 1
    error = False
    for pathData in inputData:
        if options.verbose:
            context.getDiagnostics().note = pathData.source + "processing"
        if pathData.resourceDir == u"values":
            #  Overwrite the extension.
            pathData = pathData._replace(extension="arsc")
            func = compileTable
        else:
            atype = ResourceType.parseResourceType(pathData.resourceDir)
            func = compileFile
            if atype:
                if atype != ResourceType.kRaw:
                    if pathData.extension == "xml":
                        func = compileXml
                    elif pathData.extension == "png" or pathData.extension == "9.png":
                        func = compilePng
            else:
                context.getDiagnostics().error = \
                        "invalid file path '" + pathData.source + "'"
                func = lambda *args: True
        outputFilename = buildIntermediateFilename(options.outputPath, pathData)
        error = error or not func(context, options, pathData, outputFilename)
    return int(error)

if __name__ == '__main__':
    fpath = '/home/amontesb/ROOT_HITACHI/AndroidApps/Android/res/raw-es/loaderror.html'
    fpath = '/home/amontesb/ROOT_HITACHI/AndroidApps/Android/res/layout-round-watch/alert_dialog_title_material.xml'
    fpath = '/home/amontesb/ROOT_HITACHI/AndroidApps/Android/res/values/arrays.xml'
    outpath = '/home/amontesb/ROOT_HITACHI/AppsOutput'
    compile(fpath, '-o', outpath)

    import Tools.aapt.ResourcesLab as rl


    class ExtResChunkHeader(rl.ResChunkHeader):
        typeMap = rl.ResChunkHeader.typeMap
        typeMap.update([
            (0x000c, 'RES_FILE_EXPORT_TYPE'),
            (0x000d, 'RES_TABLE_PUBLIC_TYPE'),
            (0x000e, 'RES_TABLE_SOURCE_POOL_TYPE'),
            (0x000f, 'RES_TABLE_SYMBOL_TABLE_TYPE'),
        ])

        def hasData(self):
            bFlag = super(ExtResChunkHeader, self).hasData()
            return bFlag or self.typeName in [
                # 'RES_FILE_EXPORT_TYPE',
                # 'RES_TABLE_PUBLIC_TYPE',
                # 'RES_TABLE_SOURCE_POOL_TYPE',
                # 'RES_TABLE_SYMBOL_TABLE_TYPE',
            ]


    xmlFile = '/home/amontesb/ROOT_HITACHI/AppsOutput/layout-round-watch_alert_dialog_title_material.xml.flat'
    rl.dumpXmlTree(xmlFile, headerClass=ExtResChunkHeader)

