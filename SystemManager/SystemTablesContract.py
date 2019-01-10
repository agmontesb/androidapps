# -*- coding: utf-8 -*-
from Android.interface.IBaseColumns import IBaseColumns
from Android.Uri import Uri


"""
 The "Content authority" is a name for the entire content provider, similar to the
 relationship between a domain name and its website. A convenient string to use for the
 content authority is the package name for the app, which is guaranteed to be unique on the
 Play Store.
 """
CONTENT_AUTHORITY = "com.androidapps.systemmanager"

"""
 Use CONTENT_AUTHORITY to create the base of all URI's which apps will use to contact
 the content provider for Sunshine.
"""
BASE_CONTENT_URI = Uri.parse("content://" + CONTENT_AUTHORITY)

class SystemComponents(IBaseColumns):
    BASE_CONTENT_URI

    # Table name used by our database
    TABLE_NAME = "system_components"

    # Identifier in the SystemsComponents table for the manifest tag of this package
    COLUMN_PACKAGE_ID = "package_id"
    # Date is stored as int representing time of creation of task
    COLUMN_PARENT = "parent"
    # Task is stored as String representing work to be done
    COLUMN_TYPE = "tag_type"
    # Status is stored as boolean representing current status of task
    COLUMN_CONTENT = "content"

    """
    /* The base CONTENT_URI used to query the SystemComponents table 
    from the content provider */
    """
    CONTENT_URI = Uri.withAppendedPath(BASE_CONTENT_URI, TABLE_NAME)

    @staticmethod
    def buildUriWithId(id):
        """
         * Builds a URI that adds the task _ID to the end of the todo content URI path.
         * This is used to query details about a single todo entry by _ID. This is what we
         * use for the detail view query.
         *
        :param id: Unique id pointing to that row
        :return: to query details about a single todo entry
        """
        return Uri.withAppendedPath(BASE_CONTENT_URI, '%s/%s' % (SystemComponents.TABLE_NAME, str(id)))


class InstalledPackages(IBaseColumns):
    BASE_CONTENT_URI

    # Table name used by our database
    TABLE_NAME = "installed_packages"

    # Package name as it is stated in the AndroidManifest.xml file
    COLUMN_NAME = "name"
    # Path to the AndroidManifest.xml file
    COLUMN_PATH = "path"

    """
    /* The base CONTENT_URI used to query the installed_packages table 
    from the content provider */
    """
    CONTENT_URI = Uri.withAppendedPath(BASE_CONTENT_URI, TABLE_NAME)

    @staticmethod
    def buildUriWithId(id):
        """
         * Builds a URI that adds the task _ID to the end of the todo content URI path.
         * This is used to query details about a single todo entry by _ID. This is what we
         * use for the detail view query.
         *
        :param id: Unique id pointing to that row
        :return: to query details about a single todo entry
        """
        return Uri.withAppendedPath(BASE_CONTENT_URI, '%s/%s' % (SystemComponents.TABLE_NAME, str(id)))