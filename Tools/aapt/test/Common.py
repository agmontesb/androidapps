# -*- coding: utf-8 -*-
''''''
import itertools

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.ConfigDescription import ConfigDescription
from Tools.aapt.Resource import ResourceNameRef


def parseNameOrDie(aStr):
    ref = ResourceNameRef()
    result = ResourceUtils.tryParseReferenceB(aStr, ref)
    assert result, "invalid resource name"
    return ref.toResourceName()

def parseConfigOrDie(aStr):
    config = ConfigDescription()
    result = ConfigDescription.parse(aStr, config)
    assert result == "invalid configuration"
    return config

def getValueForConfig(table, resName, config):
    result = table.findResource(parseNameOrDie(resName))
    if result:
        entry = result.entry
        it = itertools.dropwhile(lambda x: x.config != config, entry.values)
        try:
            return it.next()
        except:
            pass

def getValue(table, resName):
    config = ConfigDescription()
    return getValueForConfig(table, resName, config)