# -*- coding: utf-8 -*-
import pytest

import os
import xml.etree.ElementTree as ET
import collections

from SystemManager import SystemTablesContract
from SystemManager.SystemTablesProvider import SystemTablesProvider
from SystemManager.SystemTablesDbHelper import SystemTablesDbHelper

class testSystemTablesDbHelper(SystemTablesDbHelper):
    DATABASE_NAME = ":memory:"

class testSystemTablesProvider(SystemTablesProvider):
    def onCreate(self):
        self.mOpenHelper = mOpenHelper = testSystemTablesDbHelper(self.getContext())
        return mOpenHelper is not None


uri_package = SystemTablesContract.InstalledPackages.CONTENT_URI
uri_str = SystemTablesContract.SystemComponents.CONTENT_URI

def populateDatabase(insertValueMap):
    stack = collections.deque()
    path = os.path.abspath('./data/testAndroidManifest.xml')
    root = ET.parse(path).getroot()
    package = root.attrib.pop('package')
    stack.append((-1, root))
    while stack:
        parent_id, element = stack.popleft()
        items = [(key.split('}')[-1], value) for key, value in element.items()]
        tag, attrib = element.tag, dict(items)
        content = ' '.join(['%s="%s"' % x for x in attrib.items()])
        valueMap = dict(parent=parent_id, tag_type=tag, content=content)
        tagid = insertValueMap(uri_str, valueMap)
        if valueMap['parent'] == -1:
            valueMap = dict(component_id=tagid, name=package, path=os.path.dirname(path))
            insertValueMap(uri_package, valueMap)
        stack.extend([(tagid, item) for item in element])

@pytest.fixture(scope='module')
def provider():
    provider = testSystemTablesProvider()
    def providerInsert(uri, valueMap):
        item_uri = provider.insert(uri, valueMap)
        return int(item_uri.getLastPathSegment())
    populateDatabase(providerInsert)
    return provider

def test_SQLiteOpenHelper(provider):
    mOpenHelper = provider.mOpenHelper
    assert mOpenHelper.getDatabaseName() == ":memory:", \
        'SQLiteOpenHelper.getDatabaseName: Not the name expected'

    db1 = mOpenHelper.getWritableDatabase()
    assert not db1.isReadOnly(), \
        'SQLiteOpenHelper.getWritableDatabase: Not a writable Database'

    db2 = mOpenHelper.getReadableDatabase()
    # assert db2.isReadOnly(), \
    #     'SQLiteOpenHelper.getReadableDatabase: Not a read only Database'

    assert db1 == db2, \
        'SQLiteOpenHelper: readeable and writeable not the same db'


def test_provider(provider):
    required = "vnd.android.cursor.dir/vnd.de.code_manifest"
    assert provider.getType(uri_str) == required, 'getType: bad type'
    uri_item = SystemTablesContract.SystemComponents.buildUriWithId(134)
    required = "vnd.android.cursor.item/vnd.de.code_manifest"
    assert provider.getType(uri_item) == required, 'getType: bad type'

