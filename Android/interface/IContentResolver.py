# -*- coding: utf-8 -*-
import abc


class IContentResolver(object):
    __metaclass__ = abc.ABCMeta

    ANY_CURSOR_ITEM_TYPE = "vnd.android.cursor.item/*"
    CURSOR_DIR_BASE_TYPE = "vnd.android.cursor.dir"
    CURSOR_ITEM_BASE_TYPE = "vnd.android.cursor.item"
    EXTRA_HONORED_ARGS = "android.content.extra.HONORED_ARGS"
    EXTRA_REFRESH_SUPPORTED = "android.content.extra.REFRESH_SUPPORTED"
    EXTRA_SIZE = "android.content.extra.SIZE"
    EXTRA_TOTAL_COUNT = "android.content.extra.TOTAL_COUNT"
    NOTIFY_SKIP_NOTIFY_FOR_DESCENDANTS = 0x00000002
    NOTIFY_SYNC_TO_NETWORK = 0x00000001
    QUERY_ARG_LIMIT = "android:query-arg-limit"
    QUERY_ARG_OFFSET = "android:query-arg-offset"
    QUERY_ARG_SORT_COLLATION = "android:query-arg-sort-collation"
    QUERY_ARG_SORT_COLUMNS = "android:query-arg-sort-columns"
    QUERY_ARG_SORT_DIRECTION = "android:query-arg-sort-direction"
    QUERY_ARG_SQL_SELECTION = "android:query-arg-sql-selection"
    QUERY_ARG_SQL_SELECTION_ARGS = "android:query-arg-sql-selection-args"
    QUERY_ARG_SQL_SORT_ORDER = "android:query-arg-sql-sort-order"
    QUERY_SORT_DIRECTION_ASCENDING = 0x00000000
    QUERY_SORT_DIRECTION_DESCENDING = 0x00000001
    SCHEME_ANDROID_RESOURCE = "android.resource"
    SCHEME_CONTENT = "content"
    SCHEME_FILE = "file"
    SYNC_EXTRAS_ACCOUNT = "account"
    SYNC_EXTRAS_DISCARD_LOCAL_DELETIONS = "discard_deletions"
    SYNC_EXTRAS_DO_NOT_RETRY = "do_not_retry"
    SYNC_EXTRAS_EXPEDITED = "expedited"
    SYNC_EXTRAS_FORCE = "force"
    SYNC_EXTRAS_IGNORE_BACKOFF = "ignore_backoff"
    SYNC_EXTRAS_IGNORE_SETTINGS = "ignore_settings"
    SYNC_EXTRAS_INITIALIZE = "initialize"
    SYNC_EXTRAS_MANUAL = "force"
    SYNC_EXTRAS_OVERRIDE_TOO_MANY_DELETIONS = "deletions_override"
    SYNC_EXTRAS_REQUIRE_CHARGING = "require_charging"
    SYNC_EXTRAS_UPLOAD = "upload"
    SYNC_OBSERVER_TYPE_ACTIVE = 0x00000004
    SYNC_OBSERVER_TYPE_PENDING = 0x00000002
    SYNC_OBSERVER_TYPE_SETTINGS = 0x00000001

    def acquireContentProviderClient(self, uriOrAuthotithy, isUri=True):
        """Returns a ContentProviderClient that is associated with the
        ContentProvider that services the content at uriOr Authority,
        starting the provider if necessary."""
        pass

    def acquireUnstableContentProviderClient(self, uriOrAuthotithy, isUri=True):
        """Like acquireContentProviderClient(String), but for use when you do
        not trust the stability of the target content provider."""
        pass

    def addPeriodicSync(self, account, authority, extras, pollFrequency):
        """Specifies that a sync should be requested with the specified the
        account, authority, and extras at the given frequency."""
        pass

    def addStatusChangeListener(self, mask, callback):
        """Request notifications when the different aspects of the SyncManager
        change."""
        pass

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

    def cancelSync(self, request=None, account=None, authority=None):
        """Remove the specified sync or Cancel any active or pending syncs
        that match account and authority."""
        pass

    def canonicalize(self, url):
        """Transform the given url to a canonical representation of its
        referenced resource, which can be used across devices, persisted,
        backed up and restored, etc."""
        pass

    def delete(self, uri, where, selectionArgs):
        """Deletes row(s) specified by a content URI."""
        pass

    def getCurrentSync(self):
        """This method was deprecated in API level 11. Since multiple concurrent
        syncs are now supported you should use getCurrentSyncs() to get the
        accurate list of current syncs. This method returns the first item from
        the list of current syncs or null if there are none."""
        pass

    def getCurrentSyncs(self):
        """Returns a list with information about all the active syncs."""
        pass

    def getIsSyncable(self, account, authority):
        """Check if this account/provider is syncable."""
        pass

    def getMasterSyncAutomatically(self):
        """Gets the master auto-sync setting that applies to all the providers
        and accounts."""
        pass

    def getOutgoingPersistedUriPermissions(self):
        """Return list of all persisted URI permission grants that are hosted
        by the calling app."""
        pass

    def getPeriodicSyncs(self, account, authority):
        """Get the list of information about the periodic syncs for the given
        account and authority."""
        pass

    def getPersistedUriPermissions(self):
        """Return list of all URI permission grants that have been persisted
        by the calling app."""
        pass

    def getStreamTypes(self, url, mimeTypeFilter):
        """Query for the possible MIME types for the representations the given
        content URL can be returned when opened as as stream with
        openTypedAssetFileDescriptor(Uri, String, Bundle)."""
        pass

    def getSyncAdapterTypes(self):
        """Get information about the SyncAdapters that are known to the system."""
        pass

    def getSyncAutomatically(self, account, authority):
        """Check if the provider should be synced when a network tickle is
        received This method requires the caller to hold the permission
        Manifest.permission.READ_SYNC_SETTINGS."""
        pass

    def getType(self, url):
        """Return the MIME type of the given content URL."""
        pass

    def insert(self, url, values):
        """Inserts a row into a table at the given URL."""
        pass

    def isSyncActive(self, account, authority):
        """Returns true if there is currently a sync operation for the
        given account or authority actively being processed."""
        pass

    def isSyncPending(self, account, authority):
        """Return true if the pending status is true of any matching authorities."""
        pass

    def notifyChange(self, uri, observer, syncToNetwork=None, flags=None):
        """Notify registered observers that a row was updated."""
        pass

    def openAssetFileDescriptor(self, uri, mode, cancellationSignal=None):
        """Open a raw file descriptor to access data under a URI."""
        pass

    def openFileDescriptor(self, uri, mode, cancellationSignal=None):
        """Open a raw file descriptor to access data under a URI."""
        pass

    def openInputStream(self, uri):
        """Open a stream on to the content associated with a content URI."""
        pass

    def openOutputStream(self, uri, mode='w'):
        """Open a stream on to the content associated with a content URI."""
        pass

    def openTypedAssetFileDescriptor(self, uri, mimeType, opts, cancellationSignal=None):
        """Open a raw file descriptor to access (potentially type transformed)
        data from a "content:" URI."""
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

    def releasePersistableUriPermission(self, uri, modeFlags):
        """Relinquish a persisted URI permission grant."""
        pass

    def removePeriodicSync(self, account, authority, extras):
        """Remove a periodic sync."""
        pass

    def removeStatusChangeListener(self, handle):
        """Remove a previously registered status change listener."""
        pass

    def requestSync(self, request=None, account=None, authority=None, extras=None):
        """Start an asynchronous sync operation."""
        pass

    def setIsSyncable(self, account, authority, syncable):
        """Set whether this account/provider is syncable."""
        pass

    def setMasterSyncAutomatically(self, sync):
        """Sets the master auto-sync setting that applies to all the providers
        and accounts."""
        pass

    def setSyncAutomatically(self, account, authority, sync):
        """Set whether or not the provider is synced when it receives a network tickle."""
        pass

    def startSync(self, uri, extras):
        """This method was deprecated in API level 5. instead use
        requestSync(android.accounts.Account, String, android.os.Bundle)"""
        pass

    def takePersistableUriPermission(self, uri, modeFlags):
        """Take a persistable URI permission grant that has been offered."""
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