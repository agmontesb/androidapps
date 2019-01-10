# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET
import Tkinter as tk
import re
import bisect
import Android.BasicViews
from Android.content.res import Resources

ON_CREATE = 'onCreate'
ON_START = 'onStart'
ON_RESUME = 'onResume'
ON_PAUSE = 'onPause'
ON_STOP = 'onStop'
ON_DESTROY = 'onDestroy'

class Activity(object):
    def __init__(self, launcher, intent):
        self.widgetMapping = {}
        self.master = launcher
        name = hex(16*self.__hash__())
        self.frame = frame = tk.Frame(launcher, name=name)
        frame.droidInstance = self
        self.menuframe = menuframe = tk.Frame(frame, padx=4, pady=4, bg='light sea green')
        menuframe.pack(side=tk.TOP, fill=tk.X)
        tk.Button(menuframe, text='BACK', command=lambda: self.finish()).pack(side=tk.LEFT)
        mod = self.__module__
        glob = sys.modules[mod].__dict__
        self._res = Resources.Resources(glob)
        self._result = None
        self._intent = intent
        self.form = None
        self.radioGroups = {}
        self.nameToId = {}
        self.enEquations = {}
        self.dependents = {}

    def onCreate(self):
        self.onCreateOptionsMenu(self.menuframe)
        pass

    def onStart(self):
        pass

    def onResume(self):
        pass

    def onPause(self):
        pass

    def onStop(self):
        pass

    def onDestroy(self):
        pass

    def onCreateOptionsMenu(self, menuframe):
        pass

    def getMenuInflater(self):
        return MenuInflater(self)

    def onOptionsItemSelected(self, menu):
        pass

    def onActivityResult(self, requestCode, resultCode, anIntent):
        pass

    def close(self):
        self.onDestroy()
        self.destroy()
        pass

    def getIntent(self):
        return self._intent
    
    def getResources(self):
        return self._res

    def setContentView(self, viewid, settings=None):
        selPanel = self.getResources().getLayout(viewid).find('category')
        form = Android.BasicViews.formFrameGen(self.frame, settings, selPanel)
        form.pack(fill=tk.BOTH, expand=tk.YES)
        form.onClickEvent = self.onClickEvent
        form.onChangeSelEvent = self.onChangeSelEvent
        self.form = form

    def findViewById(self, viewid):
        if isinstance(viewid, basestring):
            viewname = viewid
        else:
            viewname = self.getResources().getResourceEntryName(viewid)
            viewname = viewname.lower()
        return getattr(self.form, viewname)

    def setResult(self, resultCode, anIntent):
        self._result = (resultCode, anIntent)

    def onClickEvent(self, resid):
        pass

    def onChangeSelEvent(self, resid):
        pass

    def onLifecycleEvent(self, event):
        if event == ON_CREATE:
            self.onCreate()
        elif event == ON_START:
            self.onStart()
        elif event == ON_RESUME:
            self.onResume()
        elif event == ON_PAUSE:
            self.onPause()
        elif event == ON_STOP:
            self.onStop()
        elif event == ON_DESTROY:
            self.onDestroy()


    """ Delegate Methods"""

    def startActivity(self, anIntent, options=None):
        return self.master.startActivity(anIntent, options)

    def startActivityForResult(self, anIntent, requestCode, options=None):
        return self.master.startActivityForResult(anIntent, requestCode, options)

    def finish(self):
        return self.master.finishActivity()


class MenuInflater(object):
    def __init__(self, context):
        self.context = context

    def inflate(self, menuidentifier, menuframe):
        from PIL import ImageTk
        res = self.context.getResources()
        groups = {}
        menuxml = res._unpack_pointer(menuidentifier)
        menuxml = ET.parse(menuxml).getroot()
        for item in menuxml.findall('./item'):
            ids_ref = ('id', 'title', 'icon')
            ids_set = set(item.attrib.keys()).intersection(ids_ref)
            ids = dict(zip(ids_set, map(res.getIdentifier, map(item.get, ids_set))))
            options = dict(name=str(ids['id']), text=res.getString(ids['title']))
            if 'icon' in ids:
                photo = ImageTk.PhotoImage(self.res.getDrawable(ids['icon']))
                options['image'] = photo
            if item.get('numericShorcut'):
                options['underline'] = int(item.get('numericShorcut'))
            options['state'] = tk.NORMAL if item.get('enable') != 'false' else tk.DISABLED
            menubutton = tk.Menubutton(menuframe, **options)
            if options.get('underline', None) is not None:
                npos = options['underline']
                ashort = options['text'][npos]
                myevent = '<<ALT-%s>>' % ashort.upper()
                menubutton.event_add(myevent, '<Alt-%s>' % ashort.lower(),
                                     '<Alt-%s>' % ashort.upper())
                menubutton.bind_all(myevent, lambda x, y=menubutton: y.focus_set())

            menubutton.pack(side=tk.LEFT)
            menubutton.menu = AndroidMenu(menubutton, tearoff=0)
            menubutton['menu'] = menubutton.menu
            stack = [(menubutton.menu, item[0].findall('./')[::-1])]
            while stack:
                menumaster, menuxml = stack.pop()
                while menuxml:
                    sitem = menuxml.pop()
                    if sitem.tag == 'group':
                        id = sitem.attrib.pop('id')
                        grpid = res.getIdentifier(id)
                        groups[grpid] = sitem.attrib.copy()
                        members = sitem.findall('./')
                        if grpid:
                            map(lambda x: x.set('grpid', grpid), members)

                        if sitem.get('checkeableBehavior') == 'single':
                            itype = tk.RADIOBUTTON
                        elif sitem.get('checkeableBehavior') == 'all':
                            itype = tk.CHECKBUTTON
                        else:
                            itype = None
                        if itype:
                            map(lambda x: x.set('itype', itype), members)

                        for key in ('visible', 'enabled'):
                            if not sitem.get(key): continue
                            value = sitem.get(key)
                            map(lambda x: x.set(key, value), members)

                        menuxml.extend(members[::-1])

                        if grpid:
                            order = 100 * int(sitem.get('menuCategory', 0)) + int(sitem.get('orderInCategory', 0))
                            order = order or None
                            menumaster._add(tk.SEPARATOR, groupId=grpid, order=order)
                    elif sitem.tag == 'item':
                        self.getMenuItem(sitem, menumaster, stack)
                    pass

    def getItemType(self, sitem):
        if list(sitem):
            itype = 'cascade'
        else:
            bflag = sitem.get('checkable') == 'true'
            default = tk.CHECKBUTTON if bflag else tk.COMMAND
            itype = sitem.get('itype', default)
        return itype

    def getMenuItem(self, sitem, menumaster, stack):
        res = self.context.getResources()
        itype = self.getItemType(sitem)
        title = res.getIdentifier(sitem.get('title'))
        grpid = sitem.get('grpid')
        itemId = res.getIdentifier(sitem.get('id'))
        order = 100*int(sitem.get('menuCategory', 0)) + int(sitem.get('orderInCategory', 0))
        order = order or None
        if itype != tk.CASCADE:
            menuitem = menumaster._add(itype, title, groupId=grpid, itemId=itemId, order=order)
        else:
            submenu = menumaster.addSubMenu(title, groupId=grpid, itemId=itemId, order=order)
            stack.append((submenu, sitem[0].findall('./')[::-1]))
            menuitem = menumaster.findItem(itemId)

        if sitem.get('icon'):
            icon = res.getIdentifier(sitem.get('icon'))
            menuitem.setIcon(icon)

        context = self.context
        if sitem.get('onClick'):
            callback = getattr(context, sitem['onClick'])
        else:
            callback = context.onOptionsItemSelected
        onclick = lambda x=menuitem: callback(x)
        menuitem.setOnMenuItemListener(onclick)

        if sitem.get('alphabeticShorcut'):
            alphachar = sitem.get('alphabeticShorcut')
            alphamod = sitem.get('alphabeticModifiers')
            menuitem.setAlphabeticShorcut(alphachar, alphamod)

        if sitem.get('numericShorcut'):
            numericchar = int(sitem.get('numericShorcut'))
            nummod = sitem.get('numericModifiers')
            menuitem.setNumericShorcut(numericchar, nummod)

        enable = sitem.get('enable') != 'false'
        menuitem.setEnable(enable)

        visible = sitem.get('visible') != 'false'
        menuitem.setVisible(visible)


class MenuItem(object):
    def __init__(self, itemId, menumaster):
        self._itemId = itemId
        self._menumaster = menumaster
        try:
            parentname = re.match(r'(\.0x[0-9a-f]+)\.', str(menumaster))
            parent = menumaster.nametowidget(parentname.group(1))
        except:
            self._res = None
        else:
            droidInstance = parent.droidInstance
            self._res = droidInstance.getResources()

    def getAlphabeticModifier(self):
        accelerator = self._entrycget('accelerator')
        return re.split(r'[+-]', accelerator)[0]

    def getAlphabeticShorcut(self):
        accelerator = self._entrycget('accelerator')
        return re.split(r'[+-]', accelerator)[-1]

    def getGroupId(self):
        itemId, menumaster = self._itemId, self._menumaster
        return menumaster._grp_for(itemId)

    def getIcon(self):
        return self._entrycget('image')

    def getItemId(self):
        return self._itemId

    def getMenuInfo(self):
        pass

    def getNumericModifiers(self):
        pass

    def getNumericShorcut(self):
        return self._entrycget('underline')

    def getOrder(self):
        menumaster, itemId = self._menumaster, self._itemId
        order = menumaster.ids[itemId]
        return order

    def getSubMenu(self):
        if self.hasSubMenu():
            name = self._entrycget('menu')
            return self._menumaster.nametowidget(name)

    def getTitle(self):
        return self._entrycget('label')

    def getTooltipText(self):
        pass

    def hasSubMenu(self):
        return self._entrycget('type') == tk.CASCADE

    def isCheckable(self):
        return self._entrycget('type') in (tk.CHECKBUTTON, tk.RADIOBUTTON)

    def isChecked(self):
        pass

    def isEnabled(self):
        enable = self._entrycget('state')
        return enable == tk.NORMAL

    def isVisible(self):
        pass

    def _entrycget(self, coption):
        itemId, menumaster = self._itemId, self._menumaster
        indx = menumaster._findIndex(itemId)
        if coption == 'type':
            return menumaster.type(indx)
        return menumaster.entrycget(indx, coption)

    def _entryconfigure(self, **kwargs):
        itemId, menumaster = self._itemId, self._menumaster
        indx = menumaster._findIndex(itemId)
        menumaster.entryconfigure(indx, **kwargs)
        return menumaster, itemId, indx

    def setAlphabeticShorcut(self, alphachar, alphamod):
        accelerator = '%s+%s' % (alphamod, alphachar)
        menumaster, itemId, indx = self._entryconfigure(accelerator=accelerator)

        alphachar, alphamod = alphachar.upper(), alphamod.upper()
        myevent = '<<%s-%s>>' % (alphamod, alphachar)
        alphamod = dict(CTRL='Control', ALT='Alt').get(alphamod, 'Control')
        menumaster.event_add(myevent,
                             '<%s-%s>' % (alphamod, alphachar.lower()),
                             '<%s-%s>' % (alphamod, alphachar))
        menumaster.bind_all(myevent, lambda x, y=indx: menumaster.invoke(y))

    def setCheckable(self, checkable):
        if checkable:
            itemId, menumaster = self._itemId, self._menumaster
            menumaster._setCheckable(itemId)
        pass

    def setChecked(self, checked):
        itemId, menumaster = self._itemId, self._menumaster
        indx = menumaster._findIndex(itemId)
        if menumaster.type(indx) in (tk.CHECKBUTTON, tk.RADIOBUTTON):
            menumaster.invoke(indx)
        pass

    def setEnable(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        self._entryconfigure(state=state)

    def setIcon(self, icon):
        from PIL import ImageTk
        res = self._res
        if isinstance(icon, int):
            icon = res.getDrawable(icon)
        image = ImageTk.PhotoImage(icon)
        menumaster, itemId, indx = self._entryconfigure(image=image)
        attribs = menumaster.itemattr.setdefault(itemId, {})
        attribs['image'] = image

    def setNumericShorcut(self, numericchar, nummod):
        self._entryconfigure(underline=numericchar)

    def setOnActionExpandListener(self, listener):
        pass

    def setOnMenuItemListener(self, listener):
        self._entryconfigure(command=listener)

    def setTitle(self, title):
        res = self._res
        if isinstance(title, int):
            title = res.getString(title)
        self._entryconfigure(label=title)

    def setTooltipText(self, tooltiptext):
        pass

    def setVisible(self, visible):
        pass


class AndroidMenu(tk.Menu):
    def __init__(self, master, *args, **kwargs):
        tk.Menu.__init__(self, master, *args, **kwargs)
        self._groupDividerEnabled = True
        self.counter = 0
        self.groups = {}
        self.groupvars = {}
        self.ids = {}
        self.order = []
        self.itemattr = {}

    def _grp_for(self, itemId):
        for grpid, members in self.groups.items():
            if itemId in members: return grpid

    def _findIndex(self, itemId, allowNew=False):
        try:
            order = self.ids[itemId]
        except:
            return
        indx = bisect.bisect_left(self.order, order)
        indx = None if not allowNew and indx > len(self.order) else indx
        return indx

    def _add(self, mitype, title='', groupId=None, itemId=None, order=None):
        if order is None:
            self.counter += 1
            order = self.counter

        if mitype == tk.SEPARATOR:
            if self._groupDividerEnabled and groupId and not self.ids.get(groupId):
                self._insertSeparator(groupId, order)
            return

        if not isinstance(title, basestring):
            try:
                parentname = re.match(r'(\.0x[0-9a-f]+)\.', str(self))
                parent = self.nametowidget(parentname.group(1))
            except:
                title = ''
            else:
                droidInstance = parent.droidInstance
                res = droidInstance.getResources()
                title = res.getString(title)
        soptions = dict(label=title, compound=tk.LEFT)

        if groupId and itemId:
            members = self.groups.setdefault(groupId, [])
            members.append(itemId)

        if itemId:
            self.ids[itemId] = order

        indx = bisect.bisect_left(self.order, order)
        bisect.insort_left(self.order, order)
        tk.Menu.insert(self, indx, mitype, **soptions)
        return MenuItem(itemId, self) if itemId else None

    def add(self, title, groupId=None, itemId=None, order=None):
        return self._add('command', title, groupId, itemId, order)

    def addSubMenu(self,title, groupId=None, itemId=None, order=None):
        self._add('cascade', title, groupId, itemId, order)
        indx = self._findIndex(itemId)
        menu = AndroidMenu(self, tearoff=0)
        self.entryconfigure(indx, menu=menu)
        return menu

    def clear(self):
        self.delete(0, tk.END)

    def close(self):
        pass

    def findItem(self, itemId):
        indx = self._findIndex(itemId)
        if indx is not None:
            indx = MenuItem(itemId, self)
        return indx

    def getItem(self, indx):
        try:
            order = self.order[indx]
            keys, values = zip(*self.ids.items())
            npos = values.index(order)
            itemId = keys[npos]
        except:
            raise IndexError('Not a valid index')
        return MenuItem(itemId, self)

    def performIdentifierAction(self, itemId, flags=0):
        indx = self._findIndex(itemId)
        if indx is not None:
            self.invoke(indx)
            return True
        return False

    def removeGroup(self, groupid):
        try:
            members = self.groups[groupid]
        except:
            return
        map(self.removeItem, members)
        self._removeSeparator(groupid)
        if self.ids.get(groupid): self.ids.pop(groupid)
        self.groups.pop(groupid)

    def _removeSeparator(self, groupid):
        grporder = self.ids.get(groupid)
        if grporder not in self.order: return
        indx = bisect.bisect_left(self.order, grporder)
        self.delete(indx)
        self.order.pop(indx)

    def _insertSeparator(self, groupid, grporder=None):
        grporder = grporder or self.ids.get(groupid)
        if grporder in self.order: return
        self.ids[groupid] = grporder
        indx = bisect.bisect_left(self.order, grporder)
        bisect.insort_left(self.order, grporder)
        tk.Menu.insert_separator(self, indx)

    def removeItem(self, itemId):
        indx = self._findIndex(itemId)
        if indx is None: return
        self.delete(indx)
        self.order.pop(indx)
        self.ids.pop(itemId)
        grpid = self._grp_for(itemId)
        if grpid is None: return
        self.groups[grpid].remove(itemId)

    def _setNotCheckable(self, itemId, groupid=None):
        indx = self._findIndex(itemId, allowNew=True)
        soptions = dict(label=self.entrycget(indx, 'label'))
        if self.type(indx) == tk.COMMAND:return
        itype = 'command'
        self.delete(indx)
        self.insert(indx, itype, **soptions)

    def _setCheckable(self, itemId, groupid=None):
        indx = self._findIndex(itemId, allowNew=True)
        soptions = dict(label=self.entrycget(indx, 'label'))
        if self.type(indx) == tk.CHECKBUTTON:return
        itype = 'checkbutton'
        variable = tk.StringVar()
        valuevar = 'onvalue'
        onvalue = str(itemId)
        soptions.update([('variable', variable), (valuevar, onvalue)])
        self.delete(indx)
        self.insert(indx, itype, **soptions)

    def _setExclusive(self, itemId, groupid=None):
        indx = self._findIndex(itemId, allowNew=True)
        soptions = dict(label=self.entrycget(indx, 'label'))
        if self.type(indx) == tk.RADIOBUTTON:return
        itype = 'radiobutton'
        variable = self.groupvars.setdefault(groupid, tk.StringVar())
        valuevar = 'value'
        onvalue = str(itemId)
        soptions.update([('variable', variable), (valuevar, onvalue)])
        self.delete(indx)
        self.insert(indx, itype, **soptions)

    def setGroupCheckable(self, groupid, checkable=False, exclusive=False):
        try:
            members = self.groups[groupid]
        except:
            return
        if not checkable and not exclusive:
            trnfcn = self._setNotCheckable
        else:
            trnfcn = self._setCheckable if not exclusive else self._setExclusive
        map(lambda x, y=groupid: trnfcn(x, y), members)

    def setGroupDividerEnabled(self, groupDividerEnabled):
        self._groupDividerEnabled = groupDividerEnabled
        trnfcn = self._insertSeparator if groupDividerEnabled else self._removeSeparator
        map(trnfcn, self.groups.keys())

    def setGroupEnabled(self, groupid, enabled):
        try:
            members = self.groups[groupid]
        except:
            return
        state = tk.NORMAL if enabled else tk.DISABLED

        for itemId in members:
            indx = self._findIndex(itemId)
            self.entryconfigure(indx, state=state)

    def setGroupVisible(self, groupid, visible):
        pass

    def size(self):
        return 0 if self.index(tk.END) is None else self.index(tk.END) + 1
