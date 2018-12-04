# -*- coding: utf-8 -*-
from Android.interface.ISQLiteOpenHelper import ISQLiteOpenHelper
from TodoContract import TodoContract

class TodoDbHelper(ISQLiteOpenHelper):
    '''
    This is the name of our database. Database names should be descriptive and end with the
    .db extension.
    '''
    DATABASE_NAME = "mytodolist.db"
    '''
    If you change the database schema, you must increment the database version or the onUpgrade
    method will not be called.
    '''
    DATABASE_VERSION = 1

    def __init_(self, context):
        super(TodoDbHelper, self).__init__(self.DATABASE_NAME, self.DATABASE_VERSION, context)

    def onCreate(db):
        '''
         This String will contain a simple SQL statement that will create a table that will
         cache our todo data.
        '''
        SQL_CREATE_TODO_TABLE = "CREATE TABLE " + TodoContract.TodoEntry.TABLE_NAME + " ("
        '''
         TodoEntry did not explicitly declare a column called "_ID". However,
         TodoEntry implements the interface, "BaseColumns", which does have a field
         named "_ID". We use that here to designate our table's primary key.
        '''
        SQL_CREATE_TODO_TABLE += TodoContract.TodoEntry._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, "
        SQL_CREATE_TODO_TABLE += TodoContract.TodoEntry.COLUMN_DATE + " INTEGER NOT NULL, "
        SQL_CREATE_TODO_TABLE += TodoContract.TodoEntry.COLUMN_TASK + " TEXT NOT NULL,"
        SQL_CREATE_TODO_TABLE += TodoContract.TodoEntry.COLUMN_STATUS + " INTEGER NOT NULL);"
        '''
         After we've spelled out our SQLite table creation statement above, we actually execute
         that SQL with the execSQL method of our SQLite database object.
        '''
        db.execSQL(SQL_CREATE_TODO_TABLE)

    def onUpgrade(self, db, oldVersion, newVersion):
        db.execSQL("DROP TABLE IF EXISTS " + TodoContract.TodoEntry.TABLE_NAME)
        self.onCreate(db)
    