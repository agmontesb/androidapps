# -*- coding: utf-8 -*-
import os
import collections
import xml.etree.ElementTree as ET

from Android.interface.ISQLiteOpenHelper import ISQLiteOpenHelper

import SystemTablesContract
PACKAGE_TABLE = SystemTablesContract.InstalledPackages
COMPONENTS_TABLE = SystemTablesContract.SystemComponents


class SystemTablesDbHelper(ISQLiteOpenHelper):
    '''
    This is the name of our database. Database names should be descriptive and end with the
    .db extension.
    '''
    DATABASE_NAME = "systemtables.db"
    '''
    If you change the database schema, you must increment the database version or the onUpgrade
    method will not be called.
    '''
    DATABASE_VERSION = 4

    def __init__(self, context):
        super(SystemTablesDbHelper, self).__init__(self.DATABASE_NAME, self.DATABASE_VERSION, context)
        self._db_directory = 'E:\BASURA\databases'

    def onCreate(self, db):
        '''
         This String will contain a simple SQL statement that will
         create a table that will cache our data.
        '''
        table_class = PACKAGE_TABLE
        SQL_CREATE_TABLE = "CREATE TABLE " + table_class.TABLE_NAME + " ("
        SQL_CREATE_TABLE += table_class._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
        SQL_CREATE_TABLE += table_class.COLUMN_NAME + " VARCHAR(30) NOT NULL,"
        SQL_CREATE_TABLE += table_class.COLUMN_PATH + " TEXT NOT NULL);"
        '''
         After we've spelled out our SQLite table creation statement above, we actually execute
         that SQL with the execSQL method of our SQLite database object.
        '''
        db.execSQL(SQL_CREATE_TABLE)
        table_class = COMPONENTS_TABLE
        SQL_CREATE_TABLE = "CREATE TABLE " + table_class.TABLE_NAME + " ("
        '''
         SystemComponents did not explicitly declare a column called "_ID". However,
         SystemComponents implements the interface, "BaseColumns", which does have a field
         named "_ID". We use that here to designate our table's primary key.
        '''
        SQL_CREATE_TABLE += table_class._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
        SQL_CREATE_TABLE += table_class.COLUMN_PACKAGE_ID + " INTEGER NOT NULL, "
        SQL_CREATE_TABLE += table_class.COLUMN_PARENT + " INTEGER NOT NULL, "
        SQL_CREATE_TABLE += table_class.COLUMN_TYPE + " VARCHAR(30) NOT NULL,"
        SQL_CREATE_TABLE += table_class.COLUMN_CONTENT + " TEXT NOT NULL);"
        '''
         After we've spelled out our SQLite table creation statement above, we actually execute
         that SQL with the execSQL method of our SQLite database object.
        '''
        db.execSQL(SQL_CREATE_TABLE)
        db.setVersion(self.DATABASE_VERSION)

    def onUpgrade(self, db, oldVersion, newVersion):
        table_classes = [
            COMPONENTS_TABLE,
            PACKAGE_TABLE
        ]
        tbl_class = PACKAGE_TABLE
        cursor = db.query(table=tbl_class.TABLE_NAME, columns=(tbl_class.COLUMN_PATH,))
        manifest_paths = map(lambda x: x[0], cursor.fetchall())
        cursor.close()
        for table_class in table_classes:
            db.execSQL("DROP TABLE IF EXISTS " + table_class.TABLE_NAME)
        self.onCreate(db)

        map(self.processAndroidManifest, manifest_paths)

    def processAndroidManifest(self, manifest_path):
        import pickle
        from Android.IntentFilter import IntentFilter

        manifest_file = os.path.join(manifest_path, 'AndroidManifest.xml')
        db = self.getWritableDatabase()
        insertValueMap = lambda table_class, valueMap: \
            db.insert(table_class.TABLE_NAME, None, valueMap)

        stack = collections.deque()
        root = self.parse_nsmap(manifest_file).getroot()
        package = root.attrib.pop('package')

        valueMap = dict(name=package, path=manifest_path)
        package_id = insertValueMap(PACKAGE_TABLE, valueMap)

        stack.append((-1, root))
        while stack:
            parent_id, element = stack.popleft()
            # items = [(key.split('}')[-1], value) for key, value in element.items()]
            tag, attrib = element.tag, element.attrib
            if tag == 'intent-filter':
                ifilter = IntentFilter()
                ifilter.readFromXml(element)
                content = pickle.dumps(ifilter)
                element = []
            else:
                content = ' '.join(['%s="%s"' % x for x in attrib.items()])
            valueMap = dict(package_id=package_id, parent=parent_id,
                            tag_type=tag, content=content)
            tagid = insertValueMap(COMPONENTS_TABLE, valueMap)
            stack.extend([(tagid, item) for item in element])

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