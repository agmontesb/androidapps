# -*- coding: utf-8 -*-
#
# Ported from
# https://android.googlesource.com/platform/frameworks/base/+/1ab598f/tools/aapt2/compile/Compile.cpp
#
import os
import collections

from Tools.aapt.Compile.ResourceTable import ResourceTable
from Tools.aapt.ConfigDescription import ConfigDescription

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

    if not os.path.exists():
        raise Exception('"%s" not such path exits' % pathData)


