# -*- coding: utf-8 -*-
import collections
import os
import tkFileDialog
from Android import Activity, BasicViews
import xml.etree.ElementTree as ET
from Android.content import Intent
from Android.content.ComponentName import ComponentName
from Android.content.pm.PackageManager import PackageManager
from SystemManagerManager import R
from SystemTablesProvider import SystemTablesProvider
from SystemTablesContract import InstalledPackages, SystemComponents

uri_package = InstalledPackages.CONTENT_URI
uri_str = SystemComponents.CONTENT_URI

packages = ['TestActivity', 'DatosBVC']
classnames = ['FragmentTest', 'MainActivity']


class SystemLauncher(Activity):
    componentPackage = []
    packages = []

    def onCreate(self):
        Activity.onCreate(self)
        self.setContentView(R.layout.SystemLauncher)
        view = self.findViewById(R.id.installed_applications)
        self.packages = packages = self.getAvailablePackages()
        view.setValue(packages)
        pass

    def getAvailablePackages(self):
        intent = Intent.Intent(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_LAUNCHER)
        pm = PackageManager()
        allapps = pm.queryIntentActivities(intent, 0)
        self.componentPackage = []
        packages = []
        for ri in allapps:
            ai = ri.activityInfo
            packages.append(ai.applicationInfo.name)
            self.componentPackage.append(ComponentName(ai.packageName, ai.name))
        return packages

    def onCreateOptionsMenu(self, menuframe):
        Activity.onCreateOptionsMenu(self, menuframe)
        inflater = self.getMenuInflater()
        inflater.inflate(R.menu.system, menuframe)
        return True

    def onOptionsItemSelected(self, menuitem):
        itemId = menuitem.getItemId()
        if itemId == R.id.sys_install:
            self.onInstall()
        print self.getResources().getResourceName(itemId)

    def onClickEvent(self, resid):
        scrlist = self.findViewById(resid)
        selId = scrlist.tree.selection()[0]
        package = scrlist.tree.set(selId, column='Nombre')
        pckindx = self.packages.index(package)
        component = self.componentPackage[pckindx]
        anIntent = Intent.Intent().setComponent(component)
        self.startActivity(anIntent, 1)

    def onInstall(self):
        manifest_path = tkFileDialog.askdirectory(title='Enter path for Application To Install')
        if not manifest_path: return
        manifest_file = os.path.join(manifest_path, 'AndroidManifest.xml')

        provider = SystemTablesProvider()
        insertValueMap = lambda uri, valueMap: int(provider.insert(uri, valueMap).getLastPathSegment())

        stack = collections.deque()
        root = ET.parse(manifest_file).getroot()
        package = root.attrib.pop('package')
        stack.append((-1, root))
        while stack:
            parent_id, element = stack.popleft()
            items = [(key.split('}')[-1], value) for key, value in element.items()]
            tag, attrib = element.tag, dict(items)
            content = ' '.join(['%s="%s"' % x for x in attrib.items()])
            valueMap = dict(parent=parent_id, tag_type=tag, content=content)
            tagid = insertValueMap(uri_str, valueMap)
            if valueMap['parent'] == -1:
                valueMap = dict(component_id=tagid, name=package, path=manifest_path)
                insertValueMap(uri_package, valueMap)
            stack.extend([(tagid, item) for item in element])

