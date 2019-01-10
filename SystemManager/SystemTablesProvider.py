# -*- coding: utf-8 -*-
import itertools

import Android as android
from Android.AndroidManifest import AndroidManifest
from Android.Os.Parcel import Parcel
from Android.UriMatcher import UriMatcher
import Android.interface.IPackageManager as PckMng
from Android.content import Intent
from Android.content.ComponentName import ComponentName
from Android.content.pm.ActivityInfo import ActivityInfo
from Android.content.pm.ComponentInfo import ComponentInfo
from Android.content.pm.ProviderInfo import ProviderInfo
from Android.content.pm.ResolveInfo import ResolveInfo
from Android.interface.IContentProvider import IContentProvider
from Android.interface.IContentResolver import IContentResolver
import SystemTablesContract
from SystemTablesDbHelper import SystemTablesDbHelper
from Android.content.IntentFilter import MATCH_CATEGORY_MASK, IntentFilter

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
    def getContext(self):
        return dict(android=android.R)

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
        try:
            nodeid = db.insert(table_class.TABLE_NAME, None, values)
        except Exception as e:
            raise Exception(e.message)
        if nodeid == -1:
            raise Exception('UnsupportedOperationException: Unknown uri: ' + uri.toString())
        return table_class.buildUriWithId(nodeid)

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
        if not table_class:
            return
        if itemId:
            selection = table_class._ID + " = ? "
            selectionArgs = (itemId,)

        _id = db.delete(table_class.TABLE_NAME, selection, selectionArgs)
        if _id != -1:
            # self.getContext().getContentResolver().notifyChange(uri, None)
            return table_class.buildUriWithId(_id)

    def update(self, uri, values, selection, selectionArgs):
        db = self.mOpenHelper.getWritableDatabase()
        table_class, itemId = self._getTableClass(uri)
        if not table_class:
            return
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
            itemId = int(uri.getLastPathSegment())
        if codeForUri == CODE_MANIFEST:
            table_class = SystemTablesContract.SystemComponents
        elif codeForUri == CODE_PACKAGE:
            table_class = SystemTablesContract.InstalledPackages
        else:
            table_class = None
        return table_class, itemId

    def getComponentRootIdForPackage(self, package_name):
        pckid_subquery = 'SELECT _id FROM {0} WHERE {1}=?'.format(
            SystemTablesContract.InstalledPackages.TABLE_NAME,
            SystemTablesContract.InstalledPackages.COLUMN_NAME
        )
        sel_string = '{0}=({1}) AND {2}=-1'.format(
            SystemTablesContract.SystemComponents.COLUMN_PACKAGE_ID,
            pckid_subquery,
            SystemTablesContract.SystemComponents.COLUMN_PARENT
        )
        sel_args = (package_name, )
        table_class = SystemTablesContract.SystemComponents
        kwargs = dict(uri=table_class.CONTENT_URI, selection=sel_string, selectionArgs=sel_args)
        try:
            cursor = self.query(**kwargs)
            rootid = cursor.fetchone()[0]
            cursor.close()
            return rootid
        except:
            raise Exception('PackageManager.NameNotFoundException')

    def getPackageInfo(self, package_name, flags):
        rootid = self.getComponentRootIdForPackage(package_name)
        raw_info = self.mOpenHelper.getAllDescendantsRecords(rootid)
        componentMap = {}
        self.getComponentIdInfo(rootid, flags, componentMap)
        pckid = componentMap.keys()[0]
        appid = itertools.dropwhile(lambda x: x[3] != 'application', raw_info).next()[0]
        elements = [(PckMng.GET_ACTIVITIES, 'activity', 'activities'),
                    (PckMng.GET_CONFIGURATIONS, 'uses-configuration', 'configPreferences'),
                    (PckMng.GET_INSTRUMENTATION, 'instrumentation', 'instrumentation'),
                    (PckMng.GET_PERMISSIONS, 'permission', 'permissions'),
                    (PckMng.GET_PROVIDERS, 'provider', 'providers'),
                    (PckMng.GET_RECEIVERS, 'receiver', 'receivers'),
                    (PckMng.GET_PERMISSIONS, 'uses-permission', 'requestedPermissions'),
                    (PckMng.GET_SERVICES, 'service', 'services'),
                    ]
        felements = reduce(lambda t, x: (t + [x[1]]) if x[0] & flags else t, elements, ['manifest', 'application'])
        componentMap.update({x[0]:None for x in raw_info[1:] if x[3] not in felements})
        for item in raw_info:
            self.getComponentIdInfo(item, flags, componentMap)
        pckginfo = componentMap[pckid]
        pckginfo.applicationInfo = componentMap[appid]
        tagMap = {x[1]:x[2] for x in elements}
        for item in raw_info[1:]:
            id, pckid, parent, tag, content = item
            if tag not in felements[2:]:continue
            getattr(pckginfo, tagMap[tag]).append(componentMap[id])
        return pckginfo

    def getComponentInfo(self, component, flags):
        package_name = component.getPackageName()
        rootid = self.getComponentRootIdForPackage(package_name)
        component_info = self.mOpenHelper.getAllDescendantsRecords(rootid, inDepth=2)
        for item in component_info:
            ifilter = self._contentConverter(item)
            class_name = ifilter.get('name')
            if class_name and component.equals(ComponentName.createRelative(package_name, class_name)):
                # return item[:-1] + (ifilter, )
                return self.getComponentIdInfo(item[0], flags)
        else:
            raise Exception('PackageManager.NameNotFoundException')

    def getComponentsInfoForIntent(self, component_type, intent, flags):
        table_class = SystemTablesContract.SystemComponents
        table_name = table_class.TABLE_NAME
        type_subquery = 'SELECT {0} FROM {1} WHERE {2}=?'.format(
            table_class._ID,
            table_name,
            table_class.COLUMN_TYPE
        )
        packageName = intent.getPackage()
        if packageName:
            pckid_subquery = "{0}=(SELECT _id FROM {1} WHERE {2}='{3}')".format(
                SystemTablesContract.SystemComponents.COLUMN_PACKAGE_ID,
                SystemTablesContract.InstalledPackages.TABLE_NAME,
                SystemTablesContract.InstalledPackages.COLUMN_NAME,
                packageName
            )
            type_subquery += ' AND ' + pckid_subquery
        sel_string = "{0}='{1}' AND {2} IN ({3})".format (
            table_class.COLUMN_TYPE,
            'intent-filter',
            table_class.COLUMN_PARENT,
            type_subquery
        )
        sel_args = (component_type, )

        kwargs = dict(uri=table_class.CONTENT_URI, selection=sel_string, selectionArgs=sel_args)
        try:
            cursor = self.query(**kwargs)
            intent_filters = cursor.fetchall()
        except:
            raise Exception('PackageManager.NameNotFoundException')
        ifilters = []
        SUCCESS = MATCH_CATEGORY_MASK
        for item in intent_filters:
            ifilter = self._contentConverter(item)
            imatch = ifilter.match(None, intent, False, '')
            if imatch & SUCCESS:
                item =(item[2], ifilter, imatch,)
                ifilters.append(item)
        componentMap = {}
        answ = []
        for componentid, ifilter, match in ifilters:
            # TODO revisar si es encesario adjuntar los flags
            # TODO revisar la forma en que se crea el intentfilter para incluir icon y demas
            componentinfo = self.getComponentIdInfo(componentid, flags, componentMap)
            resolveinfo = ResolveInfo()
            resolveinfo.filter = ifilter
            resolveinfo.isDefault = ifilter.hasCategory(Intent.CATEGORY_DEFAULT)
            resolveinfo.match = match
            resolveinfo.resolvePackageName = componentinfo.packageName
            if isinstance(componentinfo, ActivityInfo):
                resolveinfo.activityInfo = componentinfo
            elif isinstance(componentinfo, ProviderInfo):
                resolveinfo.providerInfo = componentinfo
            # elif isinstance(componentinfo, ServiceInfo):
            #     resolveinfo.serviceInfo = componentinfo
            answ.append(resolveinfo)
        return answ

    def _contentConverter(self, item):
        componentType, componentContent = item[-2], str(item[-1])
        ifilterStr = bytearray(componentContent.decode('base64'))
        parcel = Parcel()
        parcel.unmarshall(ifilterStr, 0, len(ifilterStr))
        parcel.setDataPosition(0)
        if componentType == 'intent-filter':
            return parcel.readTypedObject(IntentFilter.CREATOR)
        ifilter = {}
        parcel.readMap(ifilter, None)
        return ifilter

    def getComponentIdInfo(self, componentid, flags, componentMap=None):
        cFactory = AndroidManifest.componentFactory
        if isinstance(componentid, int): # se requiere procesar los ancestors
            predecessor_info = self.mOpenHelper.getAllAncestorsRecords(componentid)
        elif isinstance(componentid, tuple) and componentMap is not None: # 'ComponentMap is not None only when all ancestors are processed'
            predecessor_info = [componentid]
        else:
            raise Exception('Bad ancestor processing')
        if componentMap is None: componentMap = {}
        for item in predecessor_info:
            id, pckid, parent, tag, content = item
            pckid = 'pck{:0>3d}'.format(pckid)
            if id in componentMap: continue
            valuesMap = self._contentConverter(item)
            component = cFactory(tag)
            if component:
                map(lambda x: setattr(component, x[0], x[1]), valuesMap.items())
                if parent > 0:
                    component.packageName = componentMap[pckid].packageName
                    if isinstance(component, ComponentInfo):
                        component.applicationInfo = componentMap[parent]
                    componentMap[id] = component
                else:
                    component.packageName = component._unclassifiedFields.get('package')
                    componentMap[pckid] = component
            else:
                if tag == 'meta-data' and flags & PckMng.GET_META_DATA:
                    key = valuesMap.get('name')
                    if valuesMap.has_key('resource'):
                        componentMap[parent].putInt(key, valuesMap['resource'])
                    elif valuesMap.has_key('value'):
                        componentMap[parent].putString(key, valuesMap['value'])
                elif tag == 'uses-library' and flags & PckMng.GET_SHARED_LIBRARY_FILES:
                    name = valuesMap.get('name')
                    required = valuesMap.get('required', True)
                    if name and required:
                        componentMap[parent].sharedLibraryFiles.append(name)
        default = componentMap.get(pckid)
        component = componentMap.get(componentid, default)
        return component
