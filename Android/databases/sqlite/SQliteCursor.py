# -*- coding: utf-8 -*-
import sqlite3

class SQLiteCursor(sqlite3.Cursor):
    FIELD_TYPE_BLOB = 0x00000004
    FIELD_TYPE_FLOAT = 0x00000002
    FIELD_TYPE_INTEGER = 0x00000001
    FIELD_TYPE_NULL = 0x00000000
    FIELD_TYPE_STRING = 0x00000003

    def __init__(self, *args, **kwargs):
        super(SQLiteCursor, self).__init__(*args, **kwargs)

    def close(self):
        """Closes the Cursor, releasing all of its resources and making it completely invalid."""
        super(SQLiteCursor, self).close()

    def copyStringToBuffer(self, columnIndex, buffer):
        """Retrieves the requested column text and stores it in the buffer provided."""
        pass

    def deactivate(self):
        """This method was deprecated in API level 16. Since requery() is deprecated,
        so too is this."""
        pass

    def getBlob(self, columnIndex):
        """Returns the value of the requested column as a byte array."""
        pass

    def getColumnCount(self):
        """Return total number of columns                                            abstract                                        int                      getColumnIndex(String columnName)                    Returns the zero-based index for the given column name, or -1 if the column doesn't exist."""
        return len(self.description)

    def getColumnIndex(self, columnName):
        """Returns the zero-based index for the given column name,
        or -1 if the column doesn't exist."""
        try:
            return self.getColumnIndexOrThrow(columnName)
        except ValueError:
            return -1

    def getColumnIndexOrThrow(self, columnName):
        """Returns the zero-based index for the given column name, or throws IllegalArgumentException if the column doesn't exist."""
        column_names = self.getColumnNames()
        try:
            return column_names.index(columnName)
        except:
            raise ValueError('IllegalArgumentException')

    def getColumnName(self, columnIndex):
        """Returns the column name at the given zero-based column index."""
        return self.description[columnIndex][0]

    def getColumnNames(self):
        """Returns a string array holding the names of all of the columns in the result set in the order in which they were listed in the result."""
        return map(lambda x: x[0], self.description)

    def getCount(self):
        """Returns the numbers of rows in the cursor."""
        pass

    def getDatabase(self):
        """Get the database that this cursor is associated with."""
        return self.connection

    def getDouble(self, columnIndex):
        """Returns the value of the requested column as a double."""
        pass

    def getExtras(self):
        """Returns a bundle of extra values."""
        pass

    def getFloat(self, columnIndex):
        """Returns the value of the requested column as a float."""
        pass

    def getInt(self, columnIndex):
        """Returns the value of the requested column as an int."""
        pass

    def getLong(self, columnIndex):
        """Returns the value of the requested column as a long."""
        pass

    def getNotificationUri(self):
        """Return the URI at which notifications of changes in this Cursor's
        data will be delivered, as previously set by
        setNotificationUri(ContentResolver, Uri)."""
        pass

    def getPosition(self):
        """Returns the current position of the cursor in the row set."""
        pass

    def getShort(self, columnIndex):
        """Returns the value of the requested column as a short."""
        pass

    def getString(self, columnIndex):
        """Returns the value of the requested column as a String."""
        pass

    def getType(self, columnIndex):
        """Returns data type of the given column's value."""

        pass

    def getWantsAllOnMoveCalls(self):
        """onMove() will only be called across processes if this method returns true."""
        pass

    def isAfterLast(self):
        """Returns whether the cursor is pointing to the position after the last row."""
        pass

    def isBeforeFirst(self):
        """Returns whether the cursor is pointing to the position before the first row."""
        pass

    def isClosed(self):
        """return true if the cursor is closed                                            abstract                                        boolean                      isFirst()                    Returns whether the cursor is pointing to the first row."""
        pass

    def isLast(self):
        """Returns whether the cursor is pointing to the last row."""
        pass

    def isNull(self, columnIndex):
        """Returns true if the value in the indicated column is null."""
        pass

    def move(self, offset):
        """Move the cursor by a relative amount, forward or backward, from the current position."""
        pass

    def moveToFirst(self):
        """Move the cursor to the first row."""
        pass

    def moveToLast(self):
        """Move the cursor to the last row."""
        pass

    def moveToNext(self):
        """Move the cursor to the next row."""
        pass

    def moveToPosition(self, position):
        """Move the cursor to an absolute position."""
        pass

    def moveToPrevious(self):
        """Move the cursor to the previous row."""
        pass

    def onMove(self, oldPosition, newPosition):
        """ This function is called every time the cursor is successfully scrolled
        to a new position, giving the subclass a chance to update any state it
        may have."""
        pass

    def registerContentObserver(self, observer):
        """Register an observer that is called when changes happen to the content backing this cursor."""
        pass

    def registerDataSetObserver(self, observer):
        """Register an observer that is called when changes happen to the contents
        of the this cursors data set, for example, when the data set is changed
        via requery(), deactivate(), or close()."""
        pass

    def requery(self):
        """This method was deprecated in API level 11. Don't use this.
        Just request a new cursor, so you can do this asynchronously and
        update your list view once the new cursor comes back."""
        pass

    def respond(self, extras):
        """This is an out-of-band way for the the user of a cursor to communicate
        with the cursor."""
        pass

    def setExtras(self, extras):
        """Sets a Bundle that will be returned by getExtras()."""
        pass

    def setFillWindowForwardOnly(self, fillWindowForwardOnly):
        """Controls fetching of rows relative to requested position. """
        pass

    def setNotificationUri(self, cr, uri):
        """Register to watch a content URI for changes."""
        pass

    def unregisterContentObserver(self, observer):
        """Unregister an observer that has previously been registered with this cursor via registerContentObserver(ContentObserver)."""
        pass

    def unregisterDataSetObserver(self, observer):
        """Unregister an observer that has previously been registered with this cursor via registerContentObserver(ContentObserver)."""
        pass