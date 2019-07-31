# -*- coding: utf-8 -*-
import collections

from Tools.aapt.Compile.XmlIdCollector import XmlIdCollector
from Tools.aapt.Resource import SourcedResourceName
from Tools.aapt.test.Common import parseNameOrDie
from Tools.aapt.test.Context import ContextBuilder
from Tools.aapt.test.Builders import buildXmlDom
from Tools.aapt.Resource import ResourceFile

ResXml = collections.namedtuple('ResXml', 'file parser')

def getXmlPullParser(doc):
    from Android.reference.xmlpull.XmlPullParser import XmlPullParser
    from Android.reference.xmlpull.XmlPullParserFactory import XmlPullParserFactory

    factory = XmlPullParserFactory.newInstance()
    factory.setNamespaceAware(True)
    assert factory.getFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES)
    assert not factory.getFeature(XmlPullParser.FEATURE_VALIDATION)

    xmlParser = factory.newPullParser()
    try:
        xmlParser.setInput(doc, None, None)
        return xmlParser
    except:
        pass


def filterRS(aStr, lineNumber, exportedSymbols):
    sourcedResourceName = SourcedResourceName(parseNameOrDie(aStr), lineNumber)
    return filter(lambda x: x == sourcedResourceName, exportedSymbols)

def test_CollectsIds():
    context = ContextBuilder().build()
    doc = buildXmlDom(
          '\n<View xmlns:android="http://schemas.android.com/apk/res/android" \n'
          ' android:id="@+id/foo" '
          'text="@+id/bar">\n\n'
          '<SubView android:id="@+id/car" '
          'class="@+id/bar"/>\n'
          '</View>'
    )
    resXml = ResXml(ResourceFile(), getXmlPullParser(doc))
    collector = XmlIdCollector()
    assert collector.consume(context, resXml)
    exportedSymbols = resXml.file.exportedSymbols
    assert len(filterRS(u"@id/foo", 3, exportedSymbols)) == 1
    assert len(filterRS(u"@id/bar", 3, exportedSymbols)) == 1
    assert len(filterRS(u"@id/car", 6, exportedSymbols)) == 1
    

def test_DontCollectNonIds():
    context = ContextBuilder().build()
    doc = buildXmlDom("<View foo=\"@+string/foo\"/>")
    resXml = ResXml(ResourceFile(), getXmlPullParser(doc))
    collector = XmlIdCollector()
    assert collector.consume(context, resXml)
    assert not resXml.file.exportedSymbols