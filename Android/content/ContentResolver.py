# -*- coding: utf-8 -*-
from Android.Uri import Uri
from Android.interface.IContentResolver import IContentResolver
from SystemManager.SystemTablesProvider import SystemTablesProvider


class ContentResolver(IContentResolver):

    def __init__(self, context):
        super(ContentResolver, self).__init()
        self._context = context
        self._authorities = {}
        authority = 'com.androidapps.systemmanager'
        self._authorities[authority] = SystemTablesProvider()
        self._getContentResolver(authority)

    def applyBatch(self, authority, operations):
        """Applies each of the ContentProviderOperation objects and returns
        an array of their results."""
        pass

    def bulkInsert(self, url, values):
        """Inserts multiple rows into a table at the given URL."""
        pass

    def call(self, uri, method, arg, extras):
        """Call a provider-defined method."""
        pass

    def canonicalize(self, url):
        """Transform the given url to a canonical representation of its
        referenced resource, which can be used across devices, persisted,
        backed up and restored, etc."""
        pass

    def delete(self, uri, where, selectionArgs):
        """Deletes row(s) specified by a content URI."""
        pass

    def getStreamTypes(self, url, mimeTypeFilter):
        """Query for the possible MIME types for the representations the given
        content URL can be returned when opened as as stream with
        openTypedAssetFileDescriptor(Uri, String, Bundle)."""
        pass

    def getType(self, url):
        """Return the MIME type of the given content URL."""
        pass

    def insert(self, url, values):
        """Inserts a row into a table at the given URL."""
        pass

    def notifyChange(self, uri, observer, syncToNetwork=None, flags=None):
        """Notify registered observers that a row was updated."""
        pass

    def query(self, uri, projection, selection, selectionArgs, sortOrder=None, cancellationSignal=None):
        """Query the given URI, returning a Cursor over the result set with optional support for cancellation."""
        pass

    def refresh(self, url, args, cancellationSignal):
        """This allows clients to request an explicit refresh of content
        identified by uri."""
        pass

    def registerContentObserver(self, uri, notifyForDescendants, observer):
        """Register an observer class that gets callbacks when data identified
        by a given content URI changes."""
        pass

    def removeStatusChangeListener(self, handle):
        """Remove a previously registered status change listener."""
        pass

    def uncanonicalize(self, url):
        """Given a canonical Uri previously generated by canonicalize(Uri),
        convert it to its local non-canonical form."""
        pass

    def unregisterContentObserver(self, observer):
        """Unregisters a change observer."""
        pass

    def update(self, uri, values, where, selectionArgs):
        """Update row(s) in a content URI."""
        pass

    def _getContentResolver(self, authority):
        if not self._authorities.has_key(authority):
            pass
        return self._authorities.get(authority)