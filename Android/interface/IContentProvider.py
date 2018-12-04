# -*- coding: utf-8 -*-
import abc

class IContentProvider(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        was_loaded = self.onCreate()
        if not was_loaded:
            raise Exception("ContenProviderError: Can't create content provider")

    def applyBatch(self, operations):
        """Override this to handle requests to perform a batch of operations,
        or the default implementation will iterate over the operations and call
        ContentProviderOperation.apply(ContentProvider, ContentProviderResult[], int)
        on each of them."""
        pass

    def attachInfo(self, context, info):
        """After being instantiated, this is called to tell the content provider
        about itself."""
        pass

    def bulkInsert(self, uri, values):
        """Override this to handle requests to insert a set of new rows, or the
        default implementation will iterate over the values and call
        insert(Uri, ContentValues) on each of them."""
        for contentValues in values:
            self.insert(uri, contentValues)
        pass

    def call(self, method, arg, extras):
        """Call a provider-defined method."""
        method(*arg, **extras)
        pass

    def canonicalize(self, uri):
        """Implement this to support canonicalization of URIs that refer to your
        content provider."""
        pass

    @abc.abstractmethod
    def delete(self, uri, selection, selectionArgs):
        """Implement this to handle requests to delete one or more rows."""
        pass

    def dump(self, fd, writer, args):
        """Print the Provider's state into the given stream."""
        pass

    def getCallingPackage(self):
        """Return the package name of the caller that initiated the request
        being processed on the current thread."""
        pass

    def getContext(self):
        """Retrieves the Context this provider is running in."""
        pass

    def getPathPermissions(self):
        """Return the path-based permissions required for read and/or write
        access to this content provider."""
        pass

    def getReadPermission(self):
        """Return the name of the permission required for read-only access to
        this content provider."""
        pass

    def getStreamTypes(self, uri, mimeTypeFilter):
        """Called by a client to determine the types of data streams that this
        content provider supports for the given URI."""
        pass

    @abc.abstractmethod
    def getType(self, uri):
        """Implement this to handle requests for the MIME type of the data at the
        given URI."""
        pass

    def getWritePermission(self):
        """Return the name of the permission required for read/write access to
        this content provider."""
        pass

    @abc.abstractmethod
    def insert(self, uri, values):
        """Implement this to handle requests to insert a new row."""
        pass

    def onConfigurationChanged(self, newConfig):
        """Called by the system when the device configuration changes while your component is running. This method is always called on the application main thread, and must not perform lengthy operations."""
        pass

    @abc.abstractmethod
    def onCreate(self):
        """Implement this to initialize your content provider on startup."""
        pass

    def onLowMemory(self):
        """This is called when the overall system is running low on memory,
        and actively running processes should trim their memory usage.
        This method is always called on the application main thread, and must not
        perform lengthy operations."""
        pass

    def onTrimMemory(self, level):
        """Called when the operating system has determined that it is a good time
        for a process to trim unneeded memory from its process."""
        pass

    def openAssetFile(self, uri, mode, signal):
        """This is like openFile(Uri, String), but can be implemented by providers
        that need to be able to return sub-sections of files, often assets inside
        of their .apk."""
        pass

    def openFile(self, uri, mode, signal):
        """Override this to handle requests to open a file blob."""
        pass

    def openPipeHelper(self, uri, mimeType, opts, args, func):
        """A helper function for implementing openTypedAssetFile(Uri, String, Bundle), for creating a data pipe and background thread allowing you to stream generated data back to the client."""
        pass

    def openTypedAssetFile(self, uri, mimeTypeFilter, opts, signal):
        """Called by a client to open a read-only stream containing data of a
        particular MIME type."""
        pass

    @abc.abstractmethod
    def query(self, uri, projection, selection, selectionArgs, sortOrder, cancellationSignal):
        """Implement this to handle query requests from clients with support for cancellation."""
        pass

    def refresh(self, uri, args, cancellationSignal):
        """Implement this to support refresh of content identified by uri."""
        pass

    def shutdown(self):
        """Implement this to shut down the ContentProvider instance."""
        pass

    def uncanonicalize(self, url):
        """Remove canonicalization from canonical URIs previously returned by
        canonicalize(Uri)."""
        pass

    @abc.abstractmethod
    def update(self, uri, values, selection, selectionArgs):
        """Implement this to handle requests to update one or more rows."""
        pass
