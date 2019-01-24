# -*- coding: utf-8 -*-
import os
import importlib
import inspect
import xml.etree.ElementTree as ET

import Android as android
from Android.content.res.Resources import Resources
from Android.Os.Parcel import Parcel


class AndroidManifest(android.Object):
    def __init__(self, context):
        self._resources = Resources(context)

    @staticmethod
    def get_manifest_attrib_name(tag_name):
        equiv = {
            'compatible-screens': 'compatible-screens-screen',
            'manifest': '',
            'uses-permission-sdk-23': 'uses-permission'
        }
        tag_name = equiv.get(tag_name, tag_name)
        attrname = 'AndroidManifest' + tag_name.title().replace('-', '')
        assert hasattr(android.R.styleable, attrname), 'No tag description'
        return attrname

    def get_manifest_tag_attribs(self, attrname):
        res = self._resources
        styleable_id = getattr(android.R.styleable, attrname)
        styleable_id = filter(lambda x: bool(x), styleable_id)
        array = map(lambda x: res._unpack_pointer(x).attrib, styleable_id)
        return [(x['name'], x.get('format', 'String')) for x in array]

    @staticmethod
    def clasifyFields(fields, aninst):
        def fromFlagToField(x):
            w = x.split('_')[1:]
            return reduce(lambda x, y: x + y.title(), w[1:], w[0].lower())

        flagnames = filter(lambda x: x.startswith('FLAG_'), dir(inspect.getmodule(aninst)))
        flags = map(fromFlagToField, flagnames)
        fieldsFlags = set(fields).intersection(flags)
        attribs = sorted(vars(aninst).keys())
        fieldsAttribs = set(fields).intersection(attribs)
        unclassFields = set(fields).difference(fieldsFlags.union(fieldsAttribs))
        return fieldsFlags, fieldsAttribs, unclassFields

    def parse_component(self, etelement):
        try:
            etelement.attrib.pop('xmlns:map')
        except:
            pass
        # Se limpian los prefijos de los items
        attribitems = etelement.attrib.items()
        keys, values = zip(*attribitems)
        keys = [x.split('}')[-1] for x in keys]
        attribset = dict(zip(keys, values))

        manifest_attr_name = self.get_manifest_attrib_name(etelement.tag)
        styleable_id = getattr(android.R.styleable, manifest_attr_name)
        fieldvalues = self._resources.obtainAtributes(attribset, styleable_id)
        fieldnames, fieldtypes = zip(*self.get_manifest_tag_attribs(manifest_attr_name))
        answ = [x for x in zip(fieldnames, fieldvalues) if x[0] in attribset]
        attribset.update(answ)
        return attribset

    @staticmethod
    def parse_nsmap(file):
        NS_MAP = "xmlns:map"
        events = "start", "start-ns", "end-ns"
        root = None
        ns_map = []
        for event, elem in ET.iterparse(file, events):
            if event == "start-ns":
                ns_map.append(elem)
            elif event == "end-ns":
                ns_map.pop()
            elif event == "start":
                if root is None:
                    root = elem
                elem.set(NS_MAP, dict(ns_map))
        return ET.ElementTree(root)

    def processAndroidManifest(self, manifest_path, dbase, package_table_name, components_table_name):
        manifest_file = os.path.join(manifest_path, 'AndroidManifest.xml')

        stack = []

        manifest = self.parse_nsmap(manifest_file).getroot()
        package = manifest.attrib['package']

        valueMap = dict(name=package, path=manifest_path)
        package_uri = dbase.insert(package_table_name, None, valueMap)
        try:
            package_id = int(package_uri.getLastPathSegment())
        except:
            package_id = package_uri

        stack.append((-1, manifest))
        while stack:
            parent_id, element = stack.pop()
            component = self.componentFactory(element.tag)
            if component:
                if element.tag == 'intent-filter':
                    component.readFromXml(element)
                    parcel = Parcel()
                    parcel.writeTypedObject(component, 0)
                    valuemap = str(parcel.marshall()).encode('base64')
                    children = []
                else:
                    valuemap = self.parse_component(element)
                    self.setFlagsValue(valuemap, component)
                    self.setUnclassifiedFields(valuemap, component)
                    parcel = Parcel()
                    parcel.writeMap(valuemap)
                    valuemap = str(parcel.marshall()).encode('base64')
                    children = reversed(element)
                valueMap = dict(package_id=package_id, parent=parent_id,
                                tag_type=element.tag, content=valuemap.decode('utf-8'))
                taguri = dbase.insert(components_table_name, None, valueMap)
                try:
                    tagid = int(taguri.getLastPathSegment())
                except:
                    tagid = taguri
                stack.extend([(tagid, item) for item in children])

    @staticmethod
    def setFlagsValue(itemmap, aninst):
        def fromFlagToField(x):
            w = x.split('_')[1:]
            return reduce(lambda x, y: x + y.title(), w[1:], w[0].lower())

        module = inspect.getmodule(aninst)
        flagnames = filter(lambda x: x.startswith('FLAG_'), dir(module))
        flagnames = filter(lambda x: itemmap.get(fromFlagToField(x), False), flagnames)
        if flagnames:
            flags = reduce(lambda x, y: x | getattr(module, y), flagnames, 0)
            map(lambda x: itemmap.pop(x), flags)
            itemmap['flags'] = flags

    @staticmethod
    def getClassifyAttribs(itemmap, aninst):
        attribs = vars(aninst).keys()
        fieldsAttribs = set(attribs).intersection(itemmap)
        return list(fieldsAttribs)

    @staticmethod
    def setUnclassifiedFields(itemmap, aninst):
        classifiedFields = AndroidManifest.getClassifyAttribs(itemmap, aninst)
        ufields = set(itemmap).difference(classifiedFields)
        ufieldsMap = {key: itemmap.pop(key) for key in ufields}
        # parcel = Parcel()
        # parcel.writeMap(ufieldsMap)
        if ufieldsMap:
            itemmap['_unclassifiedFields'] = ufieldsMap

    @staticmethod
    def componentFactory(elemtag):
        equiv = {
            'manifest': '.pm.PackageInfo',
            'application': '.pm.ApplicationInfo',
            'activity': '.pm.ActivityInfo',
            'provider': '.pm.ProviderInfo',
            'intent-filter': '.IntentFilter'
        }
        classname = equiv.get(elemtag, None)
        if classname:
            modulename = importlib.import_module(classname, 'Android.content')
            cls = getattr(modulename, classname.rsplit('.', 1)[-1])
            return cls()
