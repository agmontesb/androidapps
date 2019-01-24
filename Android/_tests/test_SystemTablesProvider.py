# -*- coding: utf-8 -*-
import pytest
import os

import Android as android
from Android.content import Intent
from Android.content.ComponentName import ComponentName
from Android.interface.IPackageManager import IPackageManager as PckMng
from SystemManager import SystemTablesContract
from SystemManager.SystemTablesDbHelper import SystemTablesDbHelper
from SystemManager.SystemTablesProvider import SystemTablesProvider
from SystemManager.SystemTablesDbHelper import \
    PACKAGE_TABLE, \
    COMPONENTS_TABLE
from Android.content.IntentFilter import \
    MATCH_ADJUSTMENT_NORMAL, \
    MATCH_CATEGORY_EMPTY

PACKAGE_TABLE_URI = PACKAGE_TABLE.CONTENT_URI
COMPONENTS_TABLE_URI = COMPONENTS_TABLE.CONTENT_URI


class testSystemTablesDbHelper(SystemTablesDbHelper):
    DATABASE_NAME = ":memory:"
    DATABASE_VERSION = 1


class testSystemTablesProvider(SystemTablesProvider):
    def onCreate(self):
        self.mOpenHelper = mOpenHelper = testSystemTablesDbHelper(self.getContext())
        return mOpenHelper is not None

    def getContext(self):
        return dict(android=android.R)

uri_package = SystemTablesContract.InstalledPackages.CONTENT_URI
uri_str = SystemTablesContract.SystemComponents.CONTENT_URI


@pytest.fixture(scope='module')
def provider():
    provider = testSystemTablesProvider()
    path = os.path.abspath('/media/amontesb/HITACHI/AndroidApps/Android/_tests/data')
    provider.mOpenHelper.processAndroidManifest(path)
    return provider


def test_SQLiteOpenHelper():
    provider = testSystemTablesProvider()
    mOpenHelper = provider.mOpenHelper
    assert mOpenHelper.getDatabaseName() == ":memory:", \
        'SQLiteOpenHelper.getDatabaseName: Not the name expected'

    db1 = mOpenHelper.getWritableDatabase()
    assert not db1.isReadOnly(), \
        'SQLiteOpenHelper.getWritableDatabase: Not a writable Database'

    db2 = mOpenHelper.getReadableDatabase()

    assert db1 == db2, \
        'SQLiteOpenHelper: readeable and writeable not the same db'


def test_clossuretable():
    def trnfunc(x,func):
        xid = dbase.query(
            COMPONENTS_TABLE_URI,
            projection=('_id',),
            selection="content=?",
            selectionArgs=[x]
        ).fetchone()[0]
        cursor = map(
            lambda x: dbase.query(
                COMPONENTS_TABLE_URI,
                projection=('content',),
                selection='_id=?',
                selectionArgs=[x]
            ).fetchone(),
            func(xid)
        )
        try:
            return zip(*cursor)[0]
        except:
            return tuple()

    treeStruct = [
        ('colors', 'root'),
        ('azul', 'colors'),
        ('rojo', 'colors'),
        ('cielo', 'azul'),
        ('turqui', 'azul'),
        ('fuego', 'rojo'),
        ('sangre', 'rojo'),
        ('limon', 'rojo'),
        ('pollito', 'cielo'),
        ('amarillo', 'colors'),
        ('jabao', 'pollito'),
        ('delete', 'sangre'),
        ('uno', 'delete'),
        ('dos', 'delete')
    ]
    parentMap = {}
    dbase = testSystemTablesProvider()
    for node, parent in treeStruct:
        valueMap = dict(package_id=1, parent=parentMap.get(parent, -1),
                        tag_type='node', content=node.decode('utf-8'))
        taguri = dbase.insert(COMPONENTS_TABLE_URI, valueMap)
        parentMap[node] = int(taguri.getLastPathSegment())


    clossure = dbase.mOpenHelper
    getAllAncestors = lambda x: trnfunc(x, func=clossure.getAllAncestors)
    getAllDescendants = lambda x: trnfunc(x, func=clossure.getAllDescendants)
    getDirectDescendants = lambda x: trnfunc(x, func=clossure.getDirectDescendants)
    getAllSiblings = lambda x: trnfunc(x, func=clossure.getAllSiblings)

    assert getAllAncestors("jabao") == (u'colors', u'azul', u'cielo', u'pollito', u'jabao'), \
        "ERROR: getAllAncestors('jabao')"
    assert getDirectDescendants('colors') == (u'azul', u'rojo', u'amarillo'), \
        "ERROR: getDirectDescendants('colors')"
    assert getAllDescendants('azul') == (u'azul', u'cielo', u'turqui', u'pollito', u'jabao'), \
        "ERROR: getAllDescendants('azul')"
    assert getAllSiblings('cielo') == (u'cielo', u'turqui'), \
        "ERROR: getAllSiblings('cielo')"

    bUpRojo = getDirectDescendants('rojo')
    bUpCielo = getDirectDescendants('cielo')
    bUpAmarillo = getAllDescendants('amarillo')
    update_uri = COMPONENTS_TABLE_URI
    dbase.update(update_uri, {'parent':parentMap['amarillo']}, '_id IN (?, ?)', map(parentMap.get, ['limon', 'pollito']))
    aUpRojo = getDirectDescendants('rojo')
    aUpCielo = getDirectDescendants('cielo')
    aUpAmarillo = getAllDescendants('amarillo')
    assert set(bUpRojo).difference(aUpRojo) == set([u'limon']), "ERROR: update"
    assert set(bUpCielo).difference(aUpCielo) == set([u'pollito']), "ERROR: update"
    assert set(aUpAmarillo).difference(bUpAmarillo) == set((u'limon', u'pollito', u'jabao')), "ERROR: update"

    bUpSangre = getDirectDescendants('sangre')
    bUpColors = getDirectDescendants('colors')
    update_uri = COMPONENTS_TABLE.buildUriWithId(parentMap['delete'])
    dbase.update(update_uri, {'parent':parentMap['colors']}, None, None)
    aUpSangre = getDirectDescendants('sangre')
    aUpColors = getDirectDescendants('colors')
    assert set(bUpSangre).difference(aUpSangre) == set([u'delete']), "ERROR: update"
    assert set(aUpColors).difference(bUpColors) == set([u'delete']), "ERROR: update"

    deleteNodes = getAllDescendants('delete')
    assert deleteNodes == (u'delete', u'uno', u'dos'), \
        "ERROR: getAllDescendants('delete')"

    bDeColors = getAllDescendants('colors')
    delete_uri = COMPONENTS_TABLE.buildUriWithId(parentMap['delete'])
    dbase.delete(delete_uri,selection=None, selectionArgs=None)
    aDeColors = getAllDescendants('colors')
    assert set(bDeColors).difference(aDeColors) == set(deleteNodes), \
        "ERROR: Delete"

    records = dbase.query(COMPONENTS_TABLE_URI).fetchall()
    nidToName = {rec[0]:rec[-1] for rec in records}
    cm_nodes = sorted(map(lambda x: x[0], records))

    for id, pck, parent, t, name in records:
        # cm_nodes.add(id)
        print name, nidToName.get(parent)

    db = dbase.mOpenHelper.getWritableDatabase()
    records = db.query(table='clossure', selection='depth >= 0').fetchall()
    cl_nodes = sorted(reduce(lambda t, y: t.union(y[:-1]), records, set()))

    assert  cm_nodes == cl_nodes, \
        "ERROR: COMPONENTS_TABLE and ClossureTable have different nodes"


def test_provider(provider):
    required = "vnd.android.cursor.dir/vnd.de.code_manifest"
    assert provider.getType(uri_str) == required, 'getType: bad type'
    uri_item = SystemTablesContract.SystemComponents.buildUriWithId(134)
    required = "vnd.android.cursor.item/vnd.de.code_manifest"
    assert provider.getType(uri_item) == required, 'getType: bad type'


def test_packageinfo(provider):
    packagename = "com.AdroidApps.TestActivity"
    flags = PckMng.GET_ACTIVITIES | PckMng.GET_PROVIDERS
    packageinfo = provider.getPackageInfo(packagename, flags)
    assert packageinfo, 'getPackageInfo: creation failure'
    assert packageinfo.applicationInfo.name == 'mi aplicacion', \
        'getPackageInfo: applicationInfo'
    activities = packageinfo.activities
    assert len(activities) == 2, 'getPackageInfo: len activities'
    assert activities[0].name == '.TestActivity'
    assert activities[1].name == '.ActivityNumber2'
    pass

def test_getComponentsInfoForIntent(provider):
    intent = Intent.Intent(Intent.ACTION_MAIN)
    intent.addCategory(Intent.CATEGORY_LAUNCHER)
    resolveinfoList = provider.getComponentsInfoForIntent('activity', intent, 0)
    assert resolveinfoList and len(resolveinfoList) == 1
    resolveinfo = resolveinfoList[0]
    assert resolveinfo.match & MATCH_CATEGORY_EMPTY
    assert resolveinfo.match & MATCH_ADJUSTMENT_NORMAL
    assert resolveinfo.activityInfo and not (resolveinfo.serviceInfo or resolveinfo.providerInfo)
    activityinfo = resolveinfo.activityInfo
    assert activityinfo.name == '.TestActivity'
    assert activityinfo.applicationInfo.name == 'mi aplicacion'
    pass

def test_getComponentInfo(provider):
    component = ComponentName.createRelative("com.AdroidApps.TestActivity",
                                             '.TestActivity')
    activityinfo = provider.getComponentInfo(component, 0)
    assert activityinfo.name == '.TestActivity'
    assert activityinfo.applicationInfo.name == 'mi aplicacion'
    pass