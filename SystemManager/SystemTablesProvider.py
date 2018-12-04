# -*- coding: utf-8 -*-
from Android.UriMatcher import UriMatcher
from Android.interface.IContentProvider import IContentProvider
from Android.interface.IContentResolver import IContentResolver
import SystemTablesContract
from SystemTablesDbHelper import SystemTablesDbHelper

'''
These constant will be used to match URIs with the data we are looking for. We will take
advantage of the UriMatcher class to make that matching MUCH easier than doing something
ourselves, such as using regular expressions.
'''
CODE_MANIFEST = 100
CODE_MANIFEST_WITH_ID = 101
CODE_PACKAGE = 200
CODE_PACKAGE_WITH_ID = 201

def buildUriMatcher():
    '''
    All paths added to the UriMatcher have a corresponding code to return when a match is
    found. The code passed into the constructor of UriMatcher here represents the code to
    return for the root URI. It's common to use NO_MATCH as the code for this case.
    '''
    matcher = UriMatcher(UriMatcher.NO_MATCH)
    authority = SystemTablesContract.CONTENT_AUTHORITY
    '''
    For each type of URI you want to add, create a corresponding code. Preferably, these are
    constant fields in your class so that you can use them throughout the class and you no
    they aren't going to change.

    This URI is content://com.androidapps.systemmanager/system_components/ 
    '''
    table_class = SystemTablesContract.SystemComponents
    matcher.addURI(authority, table_class.TABLE_NAME, CODE_MANIFEST)
    '''
    This URI would look something like 
    content://com.androidapps.systemmanager/system_components/1
    The "/#" signifies to the UriMatcher that if TABLE_NAME is followed 
    by ANY number, that it should return the CODE_MANIFEST_WITH_ID code
    '''
    matcher.addURI(authority, table_class.TABLE_NAME + "/#", CODE_MANIFEST_WITH_ID)

    table_class = SystemTablesContract.InstalledPackages
    matcher.addURI(authority, table_class.TABLE_NAME, CODE_PACKAGE)
    matcher.addURI(authority, table_class.TABLE_NAME + "/#", CODE_PACKAGE_WITH_ID)

    return matcher


class SystemTablesProvider(IContentProvider):
    '''
    This class serves as the ContentProvider for all of Todo's data. This class allows us to
    bulkInsert data, query data, and delete data.
     '''
    mOpenHelper = None
    '''
   The URI Matcher used by this content provider.
    '''
    sUriMatcher = buildUriMatcher()

    '''
    In onCreate, we initialize our content provider on startup. This method is 
    called for all registered content providers on the application main thread 
    at application launch time. It must not perform lengthy operations, or 
    application startup will be delayed.

    @return true if the provider was successfully loaded, false otherwise
    '''

    def onCreate(self):
        self.mOpenHelper = mOpenHelper = SystemTablesDbHelper(self.getContext())
        return mOpenHelper is not None

    def query(self, uri, projection=None, selection=None, selectionArgs=None, sortOrder=None):
        '''
         * Handles query requests from clients. We will use this method to query for all
         * of our todo data as well as to query for the specific todo record.
         *
         * @param uri           The URI to query
         * @param projection    The list of columns to put into the cursor. If null, all columns are
         *                      included.
         * @param selection     A selection criteria to apply when filtering rows. If null, then all
         *                      rows are included.
         * @param selectionArgs You may include ?s in selection, which will be replaced by
         *                      the values from selectionArgs, in order that they appear in the
         *                      selection.
         * @param sortOrder     How the rows in the cursor should be sorted.
         * @return A Cursor containing the results of the query. In our implementation,
        '''
        cursor = None
        table_class, itemId = self._getTableClass(uri)
        if table_class:
            if itemId:
                _ID = uri.getLastPathSegment()
                selection = table_class._ID + " = ? "
                selectionArgs = [_ID]
            kwargs = dict(
                table=table_class.TABLE_NAME,
                columns=projection,
                selection=selection,
                selectionArgs=selectionArgs,
                orderBy=sortOrder
            )
            cursor = self.mOpenHelper.getReadableDatabase().query(**kwargs)
        else:
            raise Exception('UnsupportedOperationException: Unknown uri: ' + uri)
        # cursor.setNotificationUri(self.getContext().getContentResolver(), uri)
        return cursor

    def getType(self, uri):
        codeForUri = self.sUriMatcher.match(uri)
        if codeForUri == CODE_MANIFEST_WITH_ID:
            return IContentResolver.CURSOR_ITEM_BASE_TYPE + "/vnd.de.code_manifest"
        elif codeForUri == CODE_MANIFEST:
            return IContentResolver.CURSOR_DIR_BASE_TYPE + "/vnd.de.code_manifest"
        elif codeForUri == CODE_PACKAGE_WITH_ID:
            return IContentResolver.CURSOR_ITEM_BASE_TYPE + "/vnd.de.code_package"
        elif codeForUri == CODE_PACKAGE:
            return IContentResolver.CURSOR_DIR_BASE_TYPE + "/vnd.de.code_package"
        else:
            return None

    def insert(self, uri, values):
        '''
        Handles request to insert a new row.
         *
        param uri    The URI of the insertion request. This must not be null.
        param values A set of column_name/value pairs to add to the database. This must not be null
        return       The URI for the newly inserted item.
        '''
        db = self.mOpenHelper.getWritableDatabase()
        table_class, itemId = self._getTableClass(uri)
        if table_class:
            _id = db.insert(table_class.TABLE_NAME, None, values)
            if _id != -1:
                # self.getContext().getContentResolver().notifyChange(uri, None)
                return table_class.buildUriWithId(_id)
        raise Exception('UnsupportedOperationException: Unknown uri: ' + uri)

    def delete(self, uri, selection, selectionArgs):
        '''
        Handles request to delete a.
         *
        param uri    The URI of the insertion request. This must not be null.
        param values A set of column_name/value pairs to add to the database. This must not be null
        return       The URI for the newly inserted item.
        '''
        db = self.mOpenHelper.getWritableDatabase()
        table_class, itemId = self._getTableClass(uri)
        if table_class:
            if itemId:
                selection = table_class._ID + " = ? "
                selectionArgs = [itemId]
            _id = db.delete(table_class.TABLE_NAME, selection, selectionArgs)
            if _id != -1:
                # self.getContext().getContentResolver().notifyChange(uri, None)
                return table_class.buildUriWithId(_id)

    def update(self, uri, values, selection, selectionArgs):
        db = self.mOpenHelper.getWritableDatabase()
        table_class, itemId = self._getTableClass(uri)
        if table_class:
            if itemId:
                selection = table_class._ID + " = ? "
                selectionArgs = [itemId]
            _id = db.update(table_class.TABLE_NAME, values, selection, selectionArgs)
            if _id != -1:
                # self.getContext().getContentResolver().notifyChange(uri, None)
                return table_class.buildUriWithId(_id)

    def _getTableClass(self, uri):
        codeForUri = self.sUriMatcher.match(uri)
        itemId = None
        isItemUri = bool(codeForUri % 10)
        if isItemUri:
            codeForUri -=1
            itemId = uri.getLastPathSegment()
        if codeForUri == CODE_MANIFEST:
            table_class = SystemTablesContract.SystemComponents
        elif codeForUri == CODE_PACKAGE:
            table_class = SystemTablesContract.InstalledPackages
        else:
            table_class = None
        return table_class, itemId

