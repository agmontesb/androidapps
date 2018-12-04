# -*- coding: utf-8 -*-
from Android.UriMatcher import UriMatcher
from Android.interface.IContentProvider import IContentProvider
from Android.interface.IContentResolver import IContentResolver
from TodoContract import TodoContract
from TodoDbHelper import TodoDbHelper

class TodoProvider(IContentProvider):
    '''
    This class serves as the ContentProvider for all of Todo's data. This class allows us to
    bulkInsert data, query data, and delete data.
     '''
    mOpenHelper = None
    '''
    These constant will be used to match URIs with the data we are looking for. We will take
    advantage of the UriMatcher class to make that matching MUCH easier than doing something
    ourselves, such as using regular expressions.
    '''
    CODE_TODO = 100
    CODE_TODO_WITH_ID = 101
    '''
    Creates the UriMatcher that will match each URI to the CODE_TODO and
    CODE_TODO_WITH_ID constants defined above.
    
    UriMatcher does all the hard work for you. You just have to tell it which code to match
    with which URI, and it does the rest automatically.
    
    @return A UriMatcher that correctly matches the constants for CODE_TODO and CODE_TODO_WITH_ID
    '''
    @staticmethod
    def buildUriMatcher(self):
        '''
        All paths added to the UriMatcher have a corresponding code to return when a match is
        found. The code passed into the constructor of UriMatcher here represents the code to
        return for the root URI. It's common to use NO_MATCH as the code for this case.
        '''
        matcher = UriMatcher(UriMatcher.NO_MATCH)
        authority = TodoContract.CONTENT_AUTHORITY
        '''
        For each type of URI you want to add, create a corresponding code. Preferably, these are
        constant fields in your class so that you can use them throughout the class and you no
        they aren't going to change. In Todo, we use CODE_TODO or CODE_TODO_WITH_ID.

        This URI is content://com.example.todo/todo/ 
        '''
        matcher.addURI(authority, TodoContract.TodoEntry.TABLE_NAME, self.CODE_TODO)
        '''
        This URI would look something like content://com.example.todo/todo/1
        The "/#" signifies to the UriMatcher that if TABLE_NAME is followed by ANY number,
        that it should return the CODE_TODO_WITH_ID code
        '''
        matcher.addURI(authority, TodoContract.TodoEntry.TABLE_NAME + "/#", self.CODE_TODO_WITH_ID)

        return matcher
    '''
   The URI Matcher used by this content provider.
    '''
    sUriMatcher = buildUriMatcher()

    '''
    In onCreate, we initialize our content provider on startup. This method is called for all
    registered content providers on the application main thread at application launch time.
    It must not perform lengthy operations, or application startup will be delayed.
    
    @return true if the provider was successfully loaded, false otherwise
    '''
    def onCreate(self):
        self.mOpenHelper = mOpenHelper = TodoDbHelper(self.getContext())
        return mOpenHelper is not None

    def query(self, uri, projection, selection, selectionArgs, sortOrder):
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

        '''
         * Here's the switch statement that, given a URI, will determine what kind of request is
         * being made and query the database accordingly.
        '''
        codeForUri = self.sUriMatcher.match(uri)
        '''
        /*
         * When sUriMatcher's match method is called with a URI that looks something like this
         *
         *      content://com.example.todo/todo/2
         *
         * sUriMatcher's match method will return the code that indicates to us that we need
         * to return the todo for a particular id. The id in this code is encoded in
         * int and is at the very end of the URI (2) and can be accessed
         * programmatically using Uri's getLastPathSegment method.
         *
         * In this case, we want to return a cursor that contains one row of todo data for
         * a particular date.
         */
        '''
        if codeForUri == self.CODE_TODO_WITH_ID:
            '''
            /*
             * In order to determine the id associated with this URI, we look at the last
             * path segment. 
             */
            '''
            _ID = uri.getLastPathSegment()
            '''
            /*
             * The query method accepts a string array of arguments, as there may be more
             * than one "?" in the selection statement. Even though in our case, we only have
             * one "?", we have to create a string array that only contains one element
             * because this method signature accepts a string array.
             */
            '''
            selectionArguments = [_ID]

            cursor = self.mOpenHelper.getReadableDatabase().query(
                # Table we are going to query */
                TodoContract.TodoEntry.TABLE_NAME,
                 # * A projection designates the columns we want returned in our Cursor.
                 # * Passing null will return all columns of data within the Cursor.
                 # * However, if you don't need all the data from the table, it's best
                 # * practice to limit the columns returned in the Cursor with a projection.
                projection,
                # * The URI that matches CODE_TODO_WITH_ID contains a id at the end
                # * of it. We extract that id and use it with these next two lines to
                # * specify the row of todo we want returned in the cursor. We use a
                # * question mark here and then designate selectionArguments as the next
                # * argument for performance reasons. Whatever Strings are contained
                # * within the selectionArguments array will be inserted into the
                # * selection statement by SQLite under the hood.
                TodoContract.TodoEntry._ID + " = ? ",
                selectionArguments,
                None,
                None,
                sortOrder
            )
            # /*
            #  * When sUriMatcher's match method is called with a URI that looks EXACTLY like this
            #  *
            #  *      content://com.example.todo/todo
            #  *
            #  * sUriMatcher's match method will return the code that indicates to us that we need
            #  * to return all of the records in our todo table.
            #  *
            #  * In this case, we want to return a cursor that contains every record
            #  * in our todo table.
            #  */
        elif codeForUri == self.CODE_TODO:
            cursor = self.mOpenHelper.getReadableDatabase().query(
                TodoContract.TodoEntry.TABLE_NAME,
                projection,
                selection,
                selectionArgs,
                None,
                None,
                sortOrder
            )
        else:
            raise Exception('UnsupportedOperationException: Unknown uri: ' + uri)
        cursor.setNotificationUri(self.getContext().getContentResolver(), uri)
        return cursor

    def getType(self, uri):
        codeForUri = self.sUriMatcher.match(uri)
        if codeForUri == self.CODE_TODO_WITH_ID:
          return IContentResolver.ANY_CURSOR_ITEM_TYPE + "/vnd.de.code_todo"
        elif codeForUri == self.CODE_TODO:
          return IContentResolver.CURSOR_DIR_BASE_TYPE + "/vnd.de.code_todo"
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
        codeForUri = self.sUriMatcher.match(uri)
        if codeForUri == self.CODE_TODO:
            _id = db.insert(TodoContract.TodoEntry.TABLE_NAME, None, values)
            '''
            if _id is equal to -1 insertion failed 
            '''
            if _id != -1:
                '''
                This will help to broadcast that database has been changed,
                and will inform entities to perform automatic update.
                '''
                self.getContext().getContentResolver().notifyChange(uri, None)
            return TodoContract.TodoEntry.buildTodoUriWithId(_id)
        else:
            return None

    def delete(self, uri, selection, selectionArgs):
        '''
        Handles request to delete a.
         *
        param uri    The URI of the insertion request. This must not be null.
        param values A set of column_name/value pairs to add to the database. This must not be null
        return       The URI for the newly inserted item.
        '''
        db = self.mOpenHelper.getWritableDatabase()
        codeForUri = self.sUriMatcher.match(uri)
        if codeForUri == self.CODE_TODO_WITH_ID:
            _ID = uri.getLastPathSegment()
            selection = TodoContract.TodoEntry._ID + " = ? "
            selectionArgs = [_ID]
            _id = db.delete(TodoContract.TodoEntry.TABLE_NAME, selection, selectionArgs)
            '''
            if _id is equal to -1 insertion failed 
            '''
            if _id != -1:
                '''
                This will help to broadcast that database has been changed,
                and will inform entities to perform automatic update.
                '''
                self.getContext().getContentResolver().notifyChange(uri, None)
            return TodoContract.TodoEntry.buildTodoUriWithId(_id)
        else:
            return None


    def update(self, uri, values, selection, selectionArgs):
        return 0
