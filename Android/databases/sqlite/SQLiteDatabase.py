# -*- coding: utf-8 -*-

# Implementado con sqlite3, se puede implementar mejor con apsw (https://github.com/rogerbinns/apsw)

import os
import sys
import sqlite3
import itertools
import threading
from SQliteCursor import SQLiteCursor

CONFLICT_NONE = 0x00000000
CONFLICT_ROLLBACK = 0x00000001
CONFLICT_ABORT = 0x00000002
CONFLICT_FAIL = 0x00000003
CONFLICT_IGNORE = 0x00000004
CONFLICT_REPLACE = 0x00000005
CREATE_IF_NECESSARY = 0x10000000
ENABLE_WRITE_AHEAD_LOGGING = 0x20000000
MAX_SQL_CACHE_SIZE = 0x00000064
NO_LOCALIZED_COLLATORS = 0x00000010
OPEN_READONLY = 0x00000001
OPEN_READWRITE = 0x00000000
SQLITE_MAX_LIKE_PATTERN_LENGTH = 0x0000c350


class SQLiteDatabase(object):
    def __init__(self):
        self._conn = None
        self._isReadOnly = False
        self._errorHandler = None
        self._transactionListener = None
        self._nonSuccesfulTransactions = 0

    def beginTransaction(self):
        """Begins a transaction in EXCLUSIVE mode."""
        self._beginTransaction('EXCLUSIVE')

    def beginTransactionNonExclusive(self):
        """Begins a transaction in IMMEDIATE mode."""
        self._beginTransaction('IMMEDIATE')

    def beginTransactionWithListener(self, transactionListener):
        """Begins a transaction in EXCLUSIVE mode."""
        self._beginTransaction('EXCLUSIVE', transactionListener=transactionListener)
        pass

    def beginTransactionWithListenerNonExclusive(self, transactionListener):
        """Begins a transaction in IMMEDIATE mode."""
        self._beginTransaction('IMMEDIATE', transactionListener=transactionListener)
        pass

    def compileStatement(self, sql):
        """Compiles an SQL statement into a reusable pre-compiled statement object."""
        pass

    @classmethod
    def create(cls, factory=None):
        """Create a memory backed SQLite database."""
        openParams = dict(factory=factory)
        return cls.createInMemory(openParams)

    @classmethod
    def createInMemory(cls, openParams):
        """Create a memory backed SQLite database."""
        return cls.openOrCreateDatabase(':memory:', openParams=openParams)

    def delete(self, table, whereClause=None, whereArgs=None):
        """Convenience method for deleting rows in the database."""
        sqlStatement = 'DELETE FROM ' + table
        if whereClause is not None and whereClause != '1':
            sqlStatement += ' WHERE ' + whereClause + ';'
        else:
            sqlStatement += ';'
        cursor = self._execSQL(sqlStatement, whereArgs)
        return cursor.rowcount if whereClause else 0

    @staticmethod
    def deleteDatabase(file):
        """Deletes a database including its journal file and other auxiliary files that may have been created by the database engine."""
        try:
            os.remove(file)
            return True
        except:
            return False

    def disableWriteAheadLogging(self):
        """This method disables the features enabled by enableWriteAheadLogging()."""
        self._execPragma('journal_mode', 'delete')

    def enableWriteAheadLogging(self):
        """This method enables parallel execution of queries from multiple threads on the same database."""
        self._execPragma('journal_mode', 'wal')

    def endTransaction(self):
        """End a transaction."""
        try:
            if self._nonSuccesfulTransactions:
                self._transactionListener.onRollback()
            else:
                self._transactionListener.onCommit()
        except:
            pass
        finally:
            if self._nonSuccesfulTransactions:
                self._conn.rollback()
            else:
                self._conn.commit()
            self._conn.isolation_level = None
            self._transactionListener = None

    def execSQL(self, sql, bindArgs=None):
        """Execute a single SQL statement that is NOT a SELECT/INSERT/UPDATE/DELETE."""
        self._execSQL(sql, bindArgs)

    def findEditTable(self, tables):
        """Finds the name of the first table, which is editable."""
        pass

    def getAttachedDbs(self):
        """Returns list of full pathnames of all attached databases including
        the main database by executing 'pragma database_list' on the database."""
        lista = self._execPragma('database_list', fetchAll=True)
        lista = filter(lambda x: bool(x[2]), lista)
        return map(lambda x: (x[1], x[2]), lista)

    def getMaximumSize(self):
        """Returns the maximum size the database may grow to."""
        pass

    def getPageSize(self):
        """Returns the current database page size, in bytes."""
        return self._execPragma('page_size')

    def getPath(self):
        """Gets the path to the database file."""
        lista = self.getAttachedDbs()
        lista = itertools.dropwhile(lambda x: x[0] != u'main', lista)
        return lista.next()[2]

    def getSyncedTables(self):
        """This method was deprecated in API level 11.
        This method no longer serves any useful purpose and has been deprecated.
        """
        pass

    def getVersion(self):
        """Gets the database version."""
        return self._execPragma('user_version')

    def inTransaction(self):
        """Returns true if the current thread has a transaction pending."""
        pass

    def insert(self, table, nullColumnHack=None, values=None):
        """Convenience method for inserting a row into the database."""
        return self.insertWithOnConflict(table, nullColumnHack, values, CONFLICT_NONE)

    def insertOrThrow(self, table, nullColumnHack=None, values=None):
        """Convenience method for inserting a row into the database."""
        answ = self.insert(table, nullColumnHack, values)
        if answ == -1: raise Exception('SQLException')
        return answ

    def insertWithOnConflict(self, table, nullColumnHack, initialValues, conflictAlgorithm):
        """General method for inserting a row into the database."""
        conflictValues = ['', 'rollback', 'abort', 'fail', 'ignore', 'replace']
        conflictAlgorithm = max(CONFLICT_NONE, min(CONFLICT_REPLACE, conflictAlgorithm))
        conflictAlgorithm = conflictAlgorithm or CONFLICT_ABORT
        conflict = conflictValues[conflictAlgorithm]

        sqlStatement = 'INSERT OR %s INTO %s (%s) VALUES (%s);'
        if initialValues is None:
            columns = nullColumnHack + ','
            values = (None,)
        else:
            items = initialValues.items()
            columns, values = zip(*items)
            columns = ','.join(columns)
        svalues = ','.join(len(values)* '?')
        sqlStatement = sqlStatement % (conflict.upper(), table, columns, svalues)
        try:
            cursor = self._execSQL(sqlStatement, values)
            return cursor.lastrowid if conflictAlgorithm != CONFLICT_IGNORE else -1
        except:
            return -1

    def isDatabaseIntegrityOk(self):
        """Runs 'pragma integrity_check' on the given database
        (and all the attached databases) and returns true if the given database
        (and all its attached databases) pass integrity_check, false otherwise."""
        return self._execPragma('integrity_check') == u'ok'

    def isDbLockedByCurrentThread(self):
        """Returns true if the current thread is holding an active connection
        to the database."""
        pass

    def isDbLockedByOtherThreads(self):
        """This method was deprecated in API level 16. Always returns false.
        Do not use this method.                                                                                    boolean                      isOpen()                    Returns true if the database is currently open."""
        pass

    def isReadOnly(self):
        """Returns true if the database is opened as read only."""
        return self._isReadOnly

    def isWriteAheadLoggingEnabled(self):
        """Returns true if write-ahead logging has been enabled for this database."""
        jmode = self._execPragma('journal_mode')
        return jmode == u'wal'

    def markTableSyncable(self, table, foreignKey, updateTable):
        """This method was deprecated in API level 11. This method no longer
        serves any useful purpose and has been deprecated.
        """
        pass

    def needUpgrade(self, newVersion):
        """Returns true if the new version code is greater than the current
        database version."""
        return newVersion > self.getVersion()[0]

    @classmethod
    def openDatabase(cls, path, factory=None, flags=0, errorHandler=None, openParams=None):
        """Open the database according to the flags OPEN_READWRITE OPEN_READONLY
        CREATE_IF_NECESSARY and/or NO_LOCALIZED_COLLATORS."""
        openParams = openParams or dict(factory=factory, flags=flags, errorHandler=errorHandler)
        flags = openParams.get('flags', 0)
        if flags & CREATE_IF_NECESSARY == 0 and not os.path.exists(path):
            raise Exception('SQLException: %s, no such a file exits' % path)
        kwargs = {}
        factory = openParams.get('factory')
        if not factory:
            cursor = lambda x: sqlite3.Connection.cursor(x, SQLiteCursor)
            factory = type('_SQLiteDatabaseFactory', (sqlite3.Connection,), dict(cursor=cursor))
        kwargs['factory'] = factory
        timeout = openParams.get('idleConnectionTimeout')
        if timeout: kwargs['timeout'] = timeout
        db = cls()
        errorHandler = openParams.get('errorHandler')
        if errorHandler:
            setattr(db, '_errorHandler', errorHandler)

        try:
            sq3db = sqlite3.connect(path, **kwargs)
        except sqlite3.Error as error:
            db._sqliteError(error)

        setattr(db, '_conn', sq3db)
        is_read_only = flags & OPEN_READONLY
        if is_read_only:
            setattr(db, '_isReadOnly', True)
        return db

    @classmethod
    def openOrCreateDatabase(cls, path, factory=None, errorHandler=None):
        """Equivalent to openDatabase(path, factory, CREATE_IF_NECESSARY, errorHandler)."""
        return cls.openDatabase(path, factory, CREATE_IF_NECESSARY, errorHandler)

    def query(self, distinct=False, table='', columns=None, selection='', selectionArgs=None, groupBy='', having='', orderBy='', limit='', cancellationSignal=None):
        """Query the given URL, returning a Cursor over the result set."""
        return self.queryWithFactory(distinct=distinct, table=table, columns=columns,
                                     selection=selection, selectionArgs=selectionArgs,
                                     groupBy=groupBy, having=having, orderBy=orderBy,
                                     limit=limit, cancellationSignal=cancellationSignal)

    def queryWithFactory(self, cursorFactory=None, distinct=False, table='', columns=None, selection='', selectionArgs=None, groupBy='', having='', orderBy='', limit='', cancellationSignal=None):
        """Query the given URL, returning a Cursor over the result set."""
        sqlStatement = self._queryStatement(distinct, table, columns, selection, groupBy, having, orderBy, limit)
        return self.rawQueryWithFactory(cursorFactory=cursorFactory, sql=sqlStatement, selectionArgs=selectionArgs, cancellationSignal=cancellationSignal)

    def rawQuery(self, sql, selectionArgs=None, cancellationSignal=None):
        """Runs the provided SQL and returns a Cursor over the result set."""
        return self.rawQueryWithFactory(sql=sql, selectionArgs=selectionArgs, cancellationSignal=cancellationSignal)

    def rawQueryWithFactory(self, cursorFactory=None, sql='', selectionArgs=None, editTable=None, cancellationSignal=None):
        """Runs the provided SQL and returns a cursor over the result set."""
        return self._execSQL(sql, selectionArgs, cursorFactory, cancellationSignal)

    def releaseMemory(self):
        """Attempts to release memory that SQLite holds but does not require to operate properly."""
        pass

    def replace(self, table, nullColumnHack, initialValues):
        """Convenience method for replacing a row in the database."""
        return self.insertWithOnConflict(table=table, nullColumnHack=nullColumnHack,
                                         initialValues=initialValues,
                                         conflictAlgorithm=CONFLICT_REPLACE)

    def replaceOrThrow(self, table, nullColumnHack, initialValues):
        """Convenience method for replacing a row in the database."""
        answ = self.replace(table=table, nullColumnHack=nullColumnHack,
                            initialValues=initialValues)
        if answ == -1: raise Exception('SQLException')
        return answ

    def setForeignKeyConstraintsEnabled(self, enable):
        """Sets whether foreign key constraints are enabled for the database."""
        pass

    def setLocale(self, locale):
        """Sets the locale for this database."""
        pass

    def setLockingEnabled(self, lockingEnabled):
        """
        This method was deprecated in API level 16. This method now does nothing.
        Do not use."""
        pass

    def setMaxSqlCacheSize(self, cacheSize):
        """
        Sets the maximum size of the prepared-statement cache for this database.
        """
        pass

    def setMaximumSize(self, numBytes):
        """Sets the maximum size the database will grow to."""
        pass

    def setPageSize(self, numBytes):
        """Sets the database page size."""
        self._execPragma('page_size', numBytes)

    def setTransactionSuccessful(self):
        """Marks the current transaction as successful."""
        self._nonSuccesfulTransactions = max(0, self._nonSuccesfulTransactions - 1)
        pass

    def setVersion(self, version):
        """Sets the database version."""
        self._execPragma('user_version', version)

    def toString(self):
        """Returns a string representation of the object."""
        pass

    def update(self, table, values, whereClause, whereArgs):
        """Convenience method for updating rows in the database."""
        return self.updateWithOnConflict(table=table, values=values,
                                         whereClause=whereClause, whereArgs=whereArgs,
                                         conflictAlgorithm=CONFLICT_ABORT)

    def updateWithOnConflict(self, table, values, whereClause, whereArgs, conflictAlgorithm=CONFLICT_NONE):
        """Convenience method for updating rows in the database."""
        conflictValues = ['', 'rollback', 'abort', 'fail', 'ignore', 'replace']
        conflictAlgorithm = max(CONFLICT_NONE, min(CONFLICT_REPLACE, conflictAlgorithm))
        conflictAlgorithm = conflictAlgorithm or CONFLICT_ABORT
        conflict = conflictValues[conflictAlgorithm]

        sqlStatement = 'UPDATE OR %s %s SET %s'
        if values is None:
            values = 'NULL'
        else:
            items = values.items()
            values = ', '.join(map(lambda x: '%s = %s' % x, items))
        args = (conflict.upper(), table, values)
        if whereClause:
            sqlStatement += ' WHERE %s'
            args += (whereClause,)
        sqlStatement += ';'
        sqlStatement = sqlStatement % args
        try:
            cursor = self._execSQL(sqlStatement, whereArgs)
            return cursor.lastrowid if conflictAlgorithm != CONFLICT_IGNORE else -1
        except:
            return -1

    def validateSql(self, sql, cancellationSignal):
        """Verifies that a SQL SELECT statement is valid by compiling it."""
        pass

    def yieldIfContended(self):
        """
        This method was deprecated in API level 3. if the db is locked more than
        once (becuase of nested transactions) then the lock will not be yielded.
        Use yieldIfContendedSafely instead."""
        pass

    def yieldIfContendedSafely(self, sleepAfterYieldDelay=None):
        """Temporarily end the transaction to let other threads run."""
        pass

    def _execPragma(self, strPragma, strValue='', fetchAll=False):
        if strValue:
            sqlStatement = 'PRAGMA %s = %s;' % (strPragma, strValue)
        else:
            sqlStatement = 'PRAGMA %s;' % strPragma
        cursor = self._execSQL(sqlStatement, None)
        answ = None
        if not strValue:
            if fetchAll:
                answ = cursor.fetchall()
            else:
                answ = cursor.fetchone()
        cursor.close()
        return answ

    def _execSQL(self, sql, bindArgs, cursorFactory=None, cancellationSignal=None):
        """Execute a single SQL statement that is NOT a SELECT/INSERT/UPDATE/DELETE."""
        args = [sql, bindArgs]
        if bindArgs and isinstance(bindArgs[0], (tuple, list)):
            fcn = 'executemany'
        else:
            fcn = 'execute'
            if bindArgs is None:
                args = args[:1]

        obj = self._conn
        if cursorFactory:
            obj = obj.cursor(cursorClass=cursorFactory)
        fcn = getattr(obj, fcn)
        try:
            if cancellationSignal:
                cancellationSignal.acquire()
                self._cancellationSignal(cancellationSignal)
            cursor = fcn(*args)
            return cursor
        except sqlite3.Error as error:
            self._sqliteError(error)

    def _sqliteError(self, error):
        if not self._errorHandler:
            raise error
        self._errorHandler(self._conn)

    def _cancellationSignal(self, cancelallationSignal):
        def kill_it(connection, kill_event):
            kill_event.acquire()
            connection.interrupt()
        kill_thread = threading.Thread(target=kill_it, args=(self._conn, cancelallationSignal))
        kill_thread.daemon = True
        kill_thread.start()
        
    def _beginTransaction(self, isolation_level, transactionListener=None):
        """Begins a transaction in EXCLUSIVE mode."""
        if transactionListener:
            self._transactionListener = transactionListener
            transactionListener.begin()
        self._nonSuccesfulTransactions += 1
        self._conn.isolation_level = isolation_level

    def _queryStatement(self, distinct=False, table='', columns=None, selection='', groupBy='', having='', orderBy='', limit=''):
        """Query the given URL, returning a Cursor over the result set."""
        sqlStatement = 'SELECT '
        if distinct:
            sqlStatement += ' DISTINCT '
        columns = columns or ('*', )
        sqlStatement += ', '.join(columns)
        sqlStatement += ' FROM ' + table
        if selection:
            sqlStatement += ' WHERE ' + selection
        if groupBy:
            sqlStatement += ' GROUP BY ' + groupBy
        if having:
            sqlStatement += ' HAVING ' + having
        if orderBy:
            sqlStatement += ' ORDER BY ' + orderBy
        if limit:
            sqlStatement += ' LIMIT ' + str(limit)
        sqlStatement += ';'
        return sqlStatement