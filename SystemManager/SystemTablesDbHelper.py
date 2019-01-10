# -*- coding: utf-8 -*-
import os
import collections
import xml.etree.ElementTree as ET

from Android.AndroidManifest import AndroidManifest
from Android.interface.ISQLiteOpenHelper import ISQLiteOpenHelper
from Android.ClossureTable import ClossureTable

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
    DATABASE_VERSION = 6

    def __init__(self, context):
        super(SystemTablesDbHelper, self).__init__(self.DATABASE_NAME, self.DATABASE_VERSION, context)
        self._db_directory = '/media/amontesb/HITACHI/BASURA/databases'
        self._sqlite_db = None

    @property
    def _db(self):
        return self._sqlite_db

    @_db.setter
    def _db(self, db):
        self._sqlite_db = db
        if db:
            self._clossure = ClossureTable(
                db,
                COMPONENTS_TABLE.TABLE_NAME,
                COMPONENTS_TABLE._ID,
                COMPONENTS_TABLE.COLUMN_PARENT
            )

    def __getattr__(self, name):
        try:
            clossure = self._clossure
            return getattr(clossure, name)
        except:
            raise AttributeError()
        pass

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

        '''
        The ClossureTable class, creates and maintains a clossure table for
        the tree of the AndroidManifiest file 
        '''
        ClossureTable.onCreate(db)
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
        db.execSQL("DROP TABLE IF EXISTS clossure")
        self.onCreate(db)
        map(self.processAndroidManifest, manifest_paths)

    def processAndroidManifest(self, manifest_path):
        context = self._context
        db = self.getWritableDatabase()
        am = AndroidManifest(context)
        PACKAGE_TABLE_NAME = PACKAGE_TABLE.TABLE_NAME
        COMPONENTS_TABLE_NAME = COMPONENTS_TABLE.TABLE_NAME
        am.processAndroidManifest(
            manifest_path,
            db,
            PACKAGE_TABLE_NAME,
            COMPONENTS_TABLE_NAME
        )

