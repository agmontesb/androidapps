# -*- coding: utf-8 -*-
import abc
import os

from Android.databases.sqlite.SQLiteDatabase import SQLiteDatabase
from Android.databases.sqlite.SQLiteDatabase import CREATE_IF_NECESSARY, OPEN_READONLY

class  ISQLiteOpenHelper(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, version, context=None, factory=None, errorHandler=None, openParams=None):
        self._name = name
        self._version = version
        self._context = context
        self._factory = factory
        self._errorHandler = errorHandler
        self.setOpenParams(openParams)
        self._writeAheadLoggingEnabled = False
        self._db = None
        self._db_directory = ''

    def close(self):
        """Close any open database object."""
        try:
            self._db.close()
        except:
            pass

    def getDatabaseName(self):
        """Return the name of the SQLite database being opened, as given to the constructor."""
        return self._name

    def getReadableDatabase(self):
        """Create and/or open a database."""
        db_open_params = self._openParams
        db_open_params['flags'] = db_open_params.get('flags', 0) | CREATE_IF_NECESSARY
        db_open_params['flags'] = db_open_params.get('flags', 0) | OPEN_READONLY
        return self._getLazyDB(db_open_params)

    def getWritableDatabase(self):
        """Create and/or open a database that will be used for reading
        and writing."""
        db_open_params = self._getOpenParams()
        db_open_params['flags'] = db_open_params.get('flags', 0) | CREATE_IF_NECESSARY
        return self._getLazyDB(db_open_params)

    def onConfigure(self, db):
        """Called when the database connection is being configured, to enable
        features such as write-ahead logging or foreign key support."""
        if self._writeAheadLoggingEnabled:
            db.enableWriteAheadLogging()
        else:
            db.disableWriteAheadLogging()

    @abc.abstractmethod
    def onCreate(self, db):
        """Called when the database is created for the first time."""
        pass

    def onDowngrade(self, db, oldVersion, newVersion):
        """Called when the database needs to be downgraded."""
        pass

    def onOpen(self, db):
        """Called when the database has been opened."""
        pass

    @abc.abstractmethod
    def onUpgrade(self, db, oldVersion, newVersion):
        """Called when the database needs to be upgraded."""
        pass

    def setIdleConnectionTimeout(self, idleConnectionTimeoutMs):
        """Sets the maximum number of milliseconds that SQLite connection is
        allowed to be idle before it is closed and removed from the pool."""
        self._idleConnectionTimeout = idleConnectionTimeoutMs

    def setLookasideConfig(self, slotSize, slotCount):
        """Configures lookaside memory allocator This method should be called
        from the constructor of the subclass, before opening the database,
        since lookaside memory configuration can only be changed when no
        connection is using it SQLite default settings will be used, if this method
        isn't called."""
        pass

    def setOpenParams(self, openParams):
        """Sets configuration parameters that are used for opening SQLiteDatabase."""
        self._openParams = openParams or {}

    def setWriteAheadLoggingEnabled(self, enabled):
        """Enables or disables the use of write-ahead logging for the database."""
        self._writeAheadLoggingEnabled = enabled
        pass

    def _getOpenParams(self):
        db_open_params = self._openParams
        if not db_open_params:
            db_factory, db_error_handler = self._factory, self._errorHandler
            db_open_params['factory'] = db_factory
            db_open_params['errorHandler'] = db_error_handler
        return db_open_params

    def _getLazyDB(self, db_open_params):
        db = self._db
        if db is None:
            db_name = db_filepath = self.getDatabaseName()
            if db_name != ':memory:':
                db_path = self._db_directory
                db_filepath = os.path.join(db_path, db_name)
            bflag = not os.path.exists(db_filepath)
            db = SQLiteDatabase.openDatabase(db_filepath, openParams=db_open_params)
            journalMode = db_open_params.get('journalMode', 'wal')
            bDummy = journalMode == 'wal' and not db.isReadOnly()
            self.setWriteAheadLoggingEnabled(bDummy)
            self.onConfigure(db)
            if bflag:
                self.onCreate(db)
                db.setVersion(self._version)
        newVersion, oldVersion = self._version, db.getVersion()[0]
        if newVersion != oldVersion:
            if db.needUpgrade(newVersion):
                self.onUpgrade(db, oldVersion, newVersion)
            else:
                self.onDowngrade(db, oldVersion, newVersion)
            db.setVersion(newVersion)
        self.onOpen(db)
        self._db = db
        return db

