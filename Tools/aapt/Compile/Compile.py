# -*- coding: utf-8 -*-
#
# Ported from
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/compile/Compile.cpp
#
import os
import collections

from Tools.aapt import BigBuffer
from Tools.aapt.Compile.ResourceParser import ResourceParser
from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.ConfigDescription import ConfigDescription
from Android.reference.xmlpull.XmlPullParser import XmlPullParser
from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory

ResourcePathData = collections.namedtuple('ResourcePathData', 'source resourceDir name extension configStr config')

'''
/**
 * Resource file paths are expected to look like:
 * [--/res/]type[-config]/name
 */
 '''
def extractResourcePathData(path):
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
        path,
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

    if not os.path.exists(pathData):
        errMessage = '"%s" not such path exits' % pathData.source
        print errMessage
        return False

    factory = XmlPullParserFactory.newInstance()
    factory.setNamespaceAware(True)
    assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
    assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    xmlParser = factory.newPullParser()
    try:
        xmlParser.setInput(pathData, None)
    except:
        return False

    resParser = ResourceParser(table, pathData.source, pathData.config)
    if not resParser.parse(xmlParser):
        return False

    idAssifner = IdAssigner()
    if not idAssigner(context, table):
        return False

    buffer = BigBuffer.BigBuffer(1024)
    tableFlattenerOptions = TableFlattenerOptions()
    tableFlattenerOptions.useExtendedChunks = True
    flattener = TableFlattener(buffer, tableFlattenerOptions)
    if not flattener.consume(context, table):
        return False
    try:
        with open(outputPath, 'wb') as fout:
            fout.write(buffer)
    except Exception as e:
        print e.message
        return False
    return True



