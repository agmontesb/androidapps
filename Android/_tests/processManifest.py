# -*- coding: utf-8 -*-
import collections

import Android as android
from Android.AndroidManifest import AndroidManifest
from Android.content.IntentFilter import IntentFilter
from Android.Os.Parcel import Parcel
from SystemManager.SystemTablesDbHelper import SystemTablesDbHelper
from SystemManager.SystemTablesDbHelper import PACKAGE_TABLE, COMPONENTS_TABLE
from SystemManager.SystemTablesProvider import SystemTablesProvider

PACKAGE_TABLE_URI = PACKAGE_TABLE.CONTENT_URI
COMPONENTS_TABLE_URI = COMPONENTS_TABLE.CONTENT_URI

class DataBase(object):
    def __init__(self):
        self. counter = 0
        self.indx = []
        self.db = []
        self.clossure = []

    def query(self, queryfmt):
        return filter(lambda x: eval(queryfmt.format(x)), self.db)

    def insert(self, table_class, valueMap):
        table_class = table_class.toString()
        self.counter = nodeid = self.counter + 1
        self.indx.append(nodeid)
        valueMap['indx'] = nodeid
        self.db.append((table_class, valueMap))
        if table_class == 'COMPONENTS_TABLE':
            parent = valueMap['parent']
            self.insertClossureRecords(nodeid, parent)
        return nodeid

    def delete(self, table_class, valueMap):
        if not valueMap.get('indx'):
            return
        node = valueMap['indx']
        todelete = self.deleteClossureRecords(node)
        todelete = sorted(todelete, key=lambda x: -self.getRecord(x))
        return map(lambda x: (self.indx.pop(x), self.db.pop(x)), todelete)

    def getRecord(self, source_node):
        try:
            indx = self.indx.index(source_node)
        except:
            raise Exception('Node not in batabase')
        return self.db[indx]

    def insertClossureRecords(self, node, parent):
        componentStack = self.getAllAncestors(parent)
        maxdepth = len(componentStack)
        trnf = lambda x: self.clossure.append((x[1], node, maxdepth - x[0]))
        map(trnf, enumerate(componentStack))
        self.clossure.append((node, node, 0))

    def deleteClossureRecords(self, node):
        descendants = self.getAllDescendants(node)
        self.clossure = filter(
            lambda x: x[0] not in descendants and x[1] not in descendants,
            self.clossure
        )
        return descendants

    def getAllDescendants(self, source_node, include_node=True):
        answ =  filter(lambda x: x[0] == source_node, self.clossure)
        if not include_node:
            answ = answ[1:]
        return map(lambda x: x[1], sorted(answ, key=lambda x: x[2]))

    def getDirectDescendants(self, source_node):
        answ = filter(lambda x: x[0] == source_node and x[2] == 1, self.clossure)
        return map(lambda x: x[1], answ)

    def getAllSiblings(self, source_node):
        parent = self.getRecord(source_node)[2]['parent']
        return self.getDirectDescendants(parent)

    def getAllAncestors(self, source_node):
        answ = filter(lambda x: x[1] == source_node, self.clossure)
        return map(lambda x: x[0], sorted(answ, key=lambda x: -x[2]))


class DataBaseHelper(SystemTablesDbHelper):
    DATABASE_NAME = ':memory:'
    DATABASE_VERSION = 1


class DataBaseProvider(SystemTablesProvider):
    def onCreate(self):
        self.mOpenHelper = mOpenHelper = DataBaseHelper(self.getContext())
        return mOpenHelper is not None

    def getContext(self):
        return dict(android=android.R)

    def processAndroidManifest(self, manifest_path):
        am = AndroidManifest(self.getContext())
        am.processAndroidManifest(manifest_path, self, PACKAGE_TABLE_URI, COMPONENTS_TABLE_URI)


caso = 3
manifest_path = '/media/amontesb/HITACHI/AndroidApps/TestActivity'  # type: str
if caso == 1:
    dbase = DataBase()    
    context = dict(android=android.R)
    
    am = AndroidManifest(context)
    am.processAndroidManifest(manifest_path, dbase)
elif caso == 2:
    dbase = DataBaseProvider()
    dbase.processAndroidManifest(manifest_path)

    cur = dbase.query(COMPONENTS_TABLE_URI)
    colnames = cur.getColumnNames()
    colnames[0] = 'id'
    ComponentRecord = collections.namedtuple('ComponentRecord', colnames)
    records = map(lambda x: ComponentRecord(*x), cur.fetchall())

    parcel = Parcel()
    bytestr = bytearray(records[4].content, encoding='utf-8')
    parcel.unmarshall(bytestr, 0, len(bytestr))
    parcel.setDataPosition(0)
    content = parcel.readTypedObject(IntentFilter.CREATOR)

    node = 5
    descendants = dbase.getAllDescendants(node)
    qstr = ', '.join(map(str, descendants))
    whereClauseStr = '(successor IN ({0}) AND NOT (predecessor IN ({0})))'
    whereClauseStr += ' OR (successor=predecessor AND successor IN ({0}))'
    kwargs = dict(
        table='clossure',
        selection=whereClauseStr.format(qstr),
    )
    cursor = dbase.mOpenHelper.getReadableDatabase().query(**kwargs)
    print cursor.fetchall()

    print dbase.getAllDescendants(1, include_node=False)


    kwargs = dict(
        table='clossure',
        columns=None,
        selection='successor>?',
        selectionArgs=(0,),
        orderBy='depth,predecessor, successor ASC'
    )
    cursor = dbase.mOpenHelper.getReadableDatabase().query(**kwargs)
    print cursor.fetchall()

    print dbase.getAllAncestors(5)

    print dbase.getDirectDescendants(2)
elif caso == 3:
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
    dbase = DataBaseProvider()
    for node, parent in treeStruct:
        valueMap = dict(package_id=1, parent=parentMap.get(parent, -1),
                        tag_type='node', content=node.decode('utf-8'))
        taguri = dbase.insert(COMPONENTS_TABLE_URI, valueMap)
        parentMap[node] = int(taguri.getLastPathSegment())

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

    clossure = dbase.mOpenHelper
    getAllAncestors = lambda x: trnfunc(x, func=clossure.getAllAncestors)
    getAllDescendants = lambda x: trnfunc(x, func=clossure.getAllDescendants)
    getDirectDescendants = lambda x: trnfunc(x, func=clossure.getDirectDescendants)
    getAllSiblings = lambda x: trnfunc(x, func=clossure.getAllSiblings)

    def aprint(x, y): 
        print 'assert {0} == {1}, "ERROR: {0}"'.format(x,y)
    aprint('getAllAncestors("jabao")', getAllAncestors('jabao'))
    aprint("getDirectDescendants('colors')", getDirectDescendants('colors'))
    aprint("getAllDescendants('azul')", getAllDescendants('azul'))
    aprint("getAllSiblings('cielo')", getAllSiblings('cielo'))

    aprint("before update -> getDirectDescendants('rojo')=", getDirectDescendants('rojo'))
    aprint("before update -> getDirectDescendants('cielo')=", getDirectDescendants('cielo'))
    aprint("before update -> getAllDescendants('amarillo')=", getAllDescendants('amarillo'))
    update_uri = COMPONENTS_TABLE_URI
    dbase.update(update_uri, {'parent':parentMap['amarillo']}, '_id IN (?, ?)', map(parentMap.get, ['limon', 'pollito']))
    aprint("after update -> getDirectDescendants('rojo')=", getDirectDescendants('rojo'))
    aprint("after update -> getDirectDescendants('cielo')=", getDirectDescendants('cielo'))
    aprint("after update -> getAllDescendants('amarillo')=", getAllDescendants('amarillo'))

    aprint("getAllDescendants('delete')", getAllDescendants('delete'))
    aprint("before update -> getDirectDescendants('sangre')=", getDirectDescendants('sangre'))
    aprint("before update -> getDirectDescendants('colors')=", getDirectDescendants('colors'))
    update_uri = COMPONENTS_TABLE.buildUriWithId(parentMap['delete'])
    dbase.update(update_uri, {'parent':parentMap['colors']}, None, None)
    aprint("after update -> getDirectDescendants('sangre')=", getDirectDescendants('sangre'))
    aprint("after update -> getDirectDescendants('colors')=", getDirectDescendants('colors'))

    aprint("before delete -> getAllDescendants('colors')=", getAllDescendants('colors'))
    delete_uri = COMPONENTS_TABLE.buildUriWithId(parentMap['delete'])
    dbase.delete(delete_uri,selection=None, selectionArgs=None)
    aprint("after delete -> getAllDescendants('colors')=", getAllDescendants('colors'))

    records = dbase.query(COMPONENTS_TABLE_URI).fetchall()
    nidToName = {rec[0]:rec[-1] for rec in records}
    cm_nodes = set()
    for id, pck, parent, t, name in records:
        cm_nodes.add(id)
        print name, nidToName.get(parent)

    db = dbase.mOpenHelper.getWritableDatabase()
    records = db.query(table='clossure', selection='depth >= 0').fetchall()
    cl_nodes = set()
    for rec in records:
        cl_nodes.update(rec[:-1])
    print sorted(cl_nodes)

    print cm_nodes.difference(cl_nodes), cl_nodes.difference(cm_nodes)
pass



