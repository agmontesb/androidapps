'''
Created on 18/09/2014

@author: Alex Montes Barrios
'''

import Tkinter as tk
import tkSimpleDialog
import tkFileDialog
import ttk
import os
import fnmatch
import operator
import importlib

def widgetFactory(master, settings, selPane, panelModule=None, k=-1):
    widgetTypes = dict(sep=settSep, lsep=settSep,
                       text=settText,
                       label=settLabel,
                       optionlst=settOptionList,
                       number=settNumber, ipaddress=settNumber,
                       slider=settSlider,
                       bool=settBool,
                       enum=settEnum, labelenum=settEnum,
                       drpdwnlst=settDDList,
                       file=settFile, audio=settFile, video=settFile, image=settFile, executable=settFile,
                       folder=settFolder,
                       fileenum=settFileenum,
                       action=settAction,
                       container=settContainer,
                       fragment=settFragment, )

    if not panelModule and selPane.get('lib'):
        panelModule = selPane.get('lib')
        panelModule = importlib.import_module(panelModule, __package__)
    enableEc = []
    for xmlwidget in selPane:
        k += 1
        options = xmlwidget.attrib
        options['name'] = str(k)
        if options.get('enable', None):
            enableEc.append((k, xmlwidget.attrib['enable']))
        wType = xmlwidget.tag
        widgetClass = widgetTypes.get(wType, None)
        if not widgetClass and panelModule and hasattr(panelModule, wType):
            widgetClass = getattr(panelModule, wType)
            assert issubclass(widgetClass, baseWidget), 'All user defined widget must be inherited from baseWidget'
        else:
            assert widgetClass is not None, 'The setting type "%s" is not a define type. \n' \
                                            'It must me one of: %s ' % (wType, ', '.join(sorted(widgetTypes.keys())))

        if options.get('id'): options['id'] = options['id'].split('/')[-1]

        wId = options.get('id')
        if wId and panelModule and hasattr(panelModule, wId):
            idClass = getattr(panelModule, wId)
            assert issubclass(idClass, widgetClass), \
                'In module %s the class "%s" must be ' \
                'inherited from %s' % (panelModule.__name__, wId, widgetClass.__name__)
            setattr(idClass, 'me', master)
            widgetClass = idClass

        dummy = widgetClass(master, **options)
        if isinstance(dummy, settContainer):
            wcontainer = dummy
            if hasattr(wcontainer, 'innerframe'):
                wcontainer = wcontainer.innerframe
            k, deltEnableEc = widgetFactory(wcontainer, settings, xmlwidget, panelModule=panelModule, k=k)
            enableEc += deltEnableEc
        if hasattr(dummy, 'id'):
            key = dummy.id
            if settings and settings.has_key(key):
                dummy.setValue(settings[key])
            dummy.form.registerWidget(options['id'], dummy.path)
    return k, enableEc

def formFrameGen(master, settings, selPane):
    formclass = formFrame
    formModule = None
    if selPane.get('lib'):
        libname = selPane.get('lib')
        try:
            baseframe = master.nametowidget('.base_frame')
        except:
            pckname = master.__module__.rsplit('.', 1)[0]
        else:
            pckname = baseframe.droidInstance.__module__.rsplit('.', 1)[0]
        formModule = importlib.import_module(libname, pckname)
        classname = selPane.get('label').title().replace(' ', '')
        try:
            formClass = getattr(formModule, classname)
        except:
            pass
        else:
            if issubclass(formClass, formFrame): formclass = formClass

    return formclass(master, settings, selPane, formModule)


class formFrame(tk.Frame):
    def __init__(self, master, settings, selPane, formModule=None):
        tk.Frame.__init__(self, master)
        self.settings = {}
        self.enEquations = {}
        self.dependents = {}
        self.widgetMapping = {}
        self.nameToId = {}
        self.radioGroups = {}
        # self.frame = frame = settContainer(self, name="frame")
        # frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, anchor=tk.NE)

        self.populateWithSettings(settings, selPane, formModule)
        pass

    def __getattr__(self, attr):
        if attr in self.__dict__['widgetMapping']:
            widgetMapping = self.__dict__['widgetMapping']
            wpath = widgetMapping.get(attr)
            widget = self
            while wpath:
                wdName, wpath = wpath.partition('.')[0:3:2]
                widget = widget.nametowidget(wdName)
            return widget
        raise AttributeError("The '%s' form doesn't have an attribute call '%s'" % (self, attr))

    def populateWithSettings(self, settings, selPane, formModule):
        enableEq = widgetFactory(self, settings, selPane, panelModule=formModule)[1]
        self.nameToId = {value.rsplit('.', 1)[-1]: key for key, value in self.widgetMapping.items()}
        self.category = selPane.get('label')
        self.registerEc(enableEq)
        self.setDependantWdgState()
        self.registerChangeListeners()

    def setChangeSettings(self, settings):
        form = self
        mapping = [key for key in self.widgetMapping.keys()
                   if hasattr(getattr(form, key), 'setValue')]
        toModify = set(settings.keys()).intersection(mapping)
        map(lambda w: w.setValue(settings[w.id]), self.getWidgets(toModify))
        toReset = set(mapping).difference(toModify)
        map(lambda w: w.setValue(w.default), self.getWidgets(toReset))

    def registerEc(self, enableEquations):
        for posWidget, enableEc in enableEquations:
            enableEc = self.getAbsEcuation(posWidget, enableEc)
            wVars = map(str, self.findVars(enableEc))
            assert set(wVars).issubset(self.nameToId), 'The enable equation for "%s" widget' \
                                                       ' reference a non id widget' \
                                                       % (self.nameToId[str(posWidget)])
            for elem in wVars:
                self.dependents[elem] = self.dependents.get(elem, []) + [str(posWidget)]
            self.enEquations[str(posWidget)] = enableEc.replace('+', ' and ')

    def getAbsEcuation(self, pos, enableEc):
        for tag in ['eq(', 'lt(', 'gt(']:
            enableEc = enableEc.replace(tag, tag + '+')
        enableEc = enableEc.replace('+-', '-').replace('!', 'not ')
        enableEc = enableEc.replace('true', 'True').replace('false', 'False').replace(',)', ',None)')
        for tag in ['eq(', 'lt(', 'gt(']:
            enableEc = enableEc.replace(tag, tag + str(pos))
        return enableEc

    def findVars(self, enableEc):
        enableEc = enableEc.replace('not ', '').replace('*', '+')
        eq = lt = gt = lambda x, a: [x]
        vars = eval(enableEc)
        try:
            retval = set(vars)
        except:
            retval = []
        else:
            retval = list(retval)
        return retval
        # return [elem for k, elem in enumerate(vars) if elem not in vars[0:k]]

    def findWidgetState(self, enableEq):
        eq = lambda x, a: getattr(self, self.nameToId[str(x)]).getValue() == a
        lt = lambda x, a: getattr(self, self.nameToId[str(x)]).getValue() < a
        gt = lambda x, a: getattr(self, self.nameToId[str(x)]).getValue() > a
        state = eval(enableEq) >= 1
        return tk.NORMAL if state else tk.DISABLED

    def setDependantWdgState(self):
        for key in sorted(self.enEquations.keys(), key=int):
            enableEq = self.enEquations[key]
            calcState = self.findWidgetState(enableEq)
            widget = getattr(self, self.nameToId[key])
            try:
                idKey = widget.id
                widget.children[idKey].configure(state=calcState)
            except:
                pass

    def registerChangeListeners(self):
        for key in self.dependents.keys():
            widget = getattr(self, self.nameToId[key])
            widget.setListener(self.varChange)

    def varChange(self, widgetName):
        for depname in self.dependents[widgetName]:
            enableEq = self.enEquations[depname]
            calcState = self.findWidgetState(enableEq)
            widget = getattr(self, self.nameToId[depname])
            try:
                idKey = widget.id
                widget.children[idKey].configure(state=calcState)
            except:
                pass

    def registerWidget(self, wdId, wdPath):
        self.widgetMapping[wdId.lower()] = wdPath

    def getWidgets(self, widgetsIds=None):
        widgetsIds = widgetsIds or self.widgetMapping.keys()
        return [self.__getattr__(key) for key in widgetsIds]

    def getGroupVar(self, groupName):
        return self.radioGroups.setdefault(groupName, tk.StringVar())

    def getGroupValue(self, groupName):
        return self.radioGroups[groupName].get()

    def getChangeSettings(self, settings):
        changedSettings = dict(reset=[])
        for child in self.getWidgets():
            try:
                flag = child.isValueSetToDefault()
            except:
                pass
            else:
                key, value = child.getSettingPair()
                if not flag:
                    changedSettings[key] = value
                elif key and settings.has_key(key):
                    changedSettings['reset'].append(key)
        filterFlag = lambda key: (not settings.has_key(key) or settings[key] != changedSettings[key])
        toProcess = dict([(key, value) for key, value in changedSettings.items() if filterFlag(key)])
        return toProcess


class baseWidget(tk.Frame, object):
    def __new__(cls, *args, **options):
        instance = super(baseWidget, cls).__new__(cls, *args, **options)
        return instance

    def __init__(self, master, **options):
        wdgName = options.get('name', '').lower()
        try:
            self._id = options.pop('id')
        except:
            self._id = wdgName
        if options.has_key('varType'): self.setVarType(options.pop('varType'))
        self.default = None
        if not issubclass(self.__class__, settContainer):
            baseConf = dict(bd=1, highlightbackground='dark grey', highlightthickness=2,
                            highlightcolor='green', takefocus=1)
            baseConf.update(options)
            if wdgName: baseConf['name'] = wdgName
        else:
            baseConf = dict(name=self._id)
            if options.get('bg'): baseConf['bg'] = options['bg']
        tk.Frame.__init__(self, master, **baseConf)
        if issubclass(master.__class__, settContainer):
            self.path = master.path + '.' + baseConf.get('name', '')
            self.form = master.form
            master.applyGeoManager(self)
        else:
            self.path = baseConf.get('name', '')
            self.form = master
            self.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES, ipadx=2, ipady=2, padx=1, pady=1)

    def setVarType(self, varType='string'):
        if varType == 'int':
            self.value = tk.IntVar()
        elif varType == 'double':
            self.value = tk.DoubleVar()
        elif varType == 'boolean':
            self.value = tk.BooleanVar()
        else:
            self.value = tk.StringVar()

    def getSettingPair(self, tId=False):
        id = self._id if tId else self.id
        return (id, self.getValue())

    def isValueSetToDefault(self):
        return self.getValue() == self.default

    def setValue(self, value):
        self.value.set(value)

    def getValue(self):
        return self.value.get()

    def getConfig(self, option):
        return self.children[self.id].cget(option)

    def setConfig(self, **options):
        self.children[self.id].configure(**options)

    def setListener(self, function):
        self.listener = function
        self.value.trace("w", self.callListener)

    def callListener(self, *args):
        self.listener(self.name)

    def getDroidInstance(self):
        try:
            basic_frame = self.master.nametowidget('.base_frame')
        except:
            return
        return basic_frame.droidInstance


class settLabel(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT, fill=tk.X, expand=1)


class settFileenum(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        self.setValue(self.default)
        spBoxValues = self.getFileList(options)
        tk.Spinbox(self, name=self.id, textvariable=self.value, values=spBoxValues).pack(side=tk.RIGHT, fill=tk.X,
                                                                                         expand=1)

    def getFileList(self, options):
        basepath = os.path.abspath('.')
        values = options.get('values', '')
        mypath = os.path.join(basepath, values)
        if not os.path.exists(mypath): return
        dirpath, dirnames, filenames = os.walk(mypath).next()
        if options.get('mask', None) == '/':
            return dirnames
        else:
            mask = options.get('mask', None)
            filenames = [elem for elem in filenames if fnmatch.fnmatch(elem, mask)]
            if options.get('hideext', 'true') == 'true':
                filenames = [elem.split('.')[0] for elem in filenames]
            return filenames


class settFolder(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        self.setValue(self.default)
        ttk.Button(self, name=self.id, textvariable=self.value, command=self.getFolder).pack(side=tk.RIGHT, fill=tk.X,
                                                                                            expand=1)

    def getFolder(self):
        folder = tkFileDialog.askdirectory()
        if folder:
            self.value.set(folder)


class settFile(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        self.setValue(self.default)
        ttk.Button(self, name=self.id, #anchor='e',
                   textvariable=self.value, command=self.getFile).pack(side=tk.RIGHT,
                                                                                                      fill=tk.X,
                                                                                                      expand=1)

    def getFile(self):
        fileName = tkFileDialog.askopenfilename()
        if fileName:
            self.value.set(fileName)


class settDDList(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        self.spBoxValues = options.get('values').split('|')
        self.lvalues = spBoxValues = options.get('lvalues').split('|')
        tk.Spinbox(self, name=self.id, command=self.onChangeSel, textvariable=self.value, values=spBoxValues).pack(
            side=tk.RIGHT, fill=tk.X, expand=1)
        self.setValue(self.default)

    def setValue(self, value):
        try:
            ndx = self.spBoxValues.index(value)
        except:
            return
        self.value.set(self.lvalues[ndx])

    def getValue(self):
        try:
            ndx = self.lvalues.index(self.value.get())
        except:
            return
        return self.spBoxValues[ndx]

    def onChangeSel(self):
        try:
            self.form.onChangeSelEvent(self._id)
        except:
            pass


class settEnum(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        if options.has_key('values'):
            spBoxValues = options.get('values').split('|')
        else:
            spBoxValues = options.get('lvalues').split('|')
        tk.Spinbox(self, name=self.id, textvariable=self.value, values=spBoxValues).pack(side=tk.RIGHT, fill=tk.X,
                                                                                         expand=1)
        self.setValue(self.default)

    def setValue(self, value):
        nPos = value.find('|')
        self.withValues = withValues = nPos != -1
        if withValues:
            spBoxValue = value[nPos + 1:].split('|')
            self.children[self.id].configure(values=spBoxValue)
            value = value[:nPos]
        self.value.set(value)

    def getValue(self, onlyValue=False):
        onlyValue = onlyValue or not self.withValues
        if onlyValue: return self.value.get()
        return '|'.join([self.value.get()] + self.children[self.id].cget('values').split(' '))

    def getSettingPair(self, tId=False):
        id = self._id if tId else self.id
        return (id, self.getValue(tId))


class TreeDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, title=None, xmlFile=None, isFile=False, settings=None):
        import xmlFileWrapper
        self.allSettings = None
        self.settings = settings = settings or {}
        self.ads = xmlFileWrapper.xmlFileWrapper(xmlFile, isFile=isFile, nonDefaultValues=settings)
        tkSimpleDialog.Dialog.__init__(self, master, title)

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        selPanel = self.ads.getActivePane()
        self.form = form = formFrameGen(master, {}, selPanel)
        form.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        wdgId = sorted(form.nameToId.keys(), key=int)[0]
        wdgId = form.nameToId[wdgId]
        widget = getattr(self.form, wdgId)
        return widget

    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = tk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        settings = self.settings
        changedSettings = self.form.getChangeSettings(settings)
        reset = changedSettings.pop('reset')
        for key in reset: settings.pop(key)
        settings.update(changedSettings)
        self.result = dict(settings)
        allwidgets = self.form.getWidgets()
        allwidgets.sort(key=operator.attrgetter('id'))
        allSettings = [widget.getSettingPair(tId=True) for widget in allwidgets]

        self.allSettings = allSettings
        self.cancel()
        pass

    def geometry(self, posStr):
        width, height = 290, 220
        posx = (self.winfo_screenwidth() - width) / 2
        posy = (self.winfo_screenheight() - height) / 2
        posStr = "+%d+%d" % (posx, posy)
        tkSimpleDialog.Dialog.geometry(self, posStr)


class settOptionList(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        self.isTree = options.get('tree', 'false') == 'true'
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        settSep(self, name='label', type='lsep', label=options.get('label'))

        if options.get('id'): self.id = options.get('id').lower().replace('.', '__')
        self.default = options.get('default', '')

        uFrame = tk.Frame(self)
        uFrame.pack(side=tk.TOP, fill=tk.BOTH)

        sbar = ttk.Scrollbar(uFrame)
        sbar.pack(side=tk.RIGHT, fill=tk.Y)

        colHeadings = options.get('columnsheadings')
        dshow = 'headings'
        columnsId = dcolumns = map(lambda x: x.strip(), colHeadings.split(','))
        if self.isTree:
            dshow = 'tree ' + dshow
            dcolumns = '#all'
        tree = ttk.Treeview(uFrame, show=dshow, columns=columnsId, displaycolumns=dcolumns)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        sbar.config(command=tree.yview)  # xlink sbar and tree
        tree.config(yscrollcommand=sbar.set)  # move one moves other
        for column in columnsId:
            tree.heading(column, text=column, anchor=tk.W)
        self.tree = tree
        self.columnsId = columnsId

        bFrame = tk.Frame(self)
        bFrame.pack(side=tk.BOTTOM, fill=tk.X)
        boton = ttk.Button(bFrame, text='Add', width=15, command=self.onAdd)
        boton.pack(side=tk.LEFT)
        boton = ttk.Button(bFrame, text='Edit', width=15, command=self.onEdit)
        boton.pack(side=tk.LEFT)
        boton = ttk.Button(bFrame, text='Del', width=15, command=self.onDel)
        boton.pack(side=tk.RIGHT)

        self.setValue(self.default)

    def xmlDlgWindow(self, tupleSett, isEdit=False, isTree=False):
        header = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<settings>
    <category label="TCombobox">
"""
        footer = """    </category>
</settings>
"""
        outStr = header
        if not isEdit and isTree:
            deltaStr = '<setting id="{0}" type="text" label="Parent Element" default="{1}" enable="false"/>\n'
            outStr += 8 * ' ' + deltaStr.format(*tupleSett[0])
            deltaStr = '<setting id="{0}" type="text" label="Element Name" default="{1}" />\n'
            outStr += 8 * ' ' + deltaStr.format(*tupleSett[1])
            tupleSett = tupleSett[2:]

        templateStr = '<setting id="{0}" type="text" label="{0}" default=""/>\n'
        if isEdit:
            templateStr = '<setting id="{0}" type="text" label="{0}" default="{1}"/>\n'
        for x, y in tupleSett:
            deltaStr = templateStr.format(x, y)
            outStr += 8 * ' ' + deltaStr
        outStr += footer
        return outStr

    def onAdd(self):
        parent = self.tree.focus()
        pair = [(col, col) for col in self.columnsId]
        if self.isTree:
            pair = [('parent', self.tree.item(parent, 'text')), ('text', '')] + pair
        xmlDlg = self.xmlDlgWindow(pair, isEdit=False, isTree=self.isTree)
        dlg = TreeDialog(self, title='Add', xmlFile=xmlDlg, isFile=False)
        if dlg.allSettings:
            result = dict(dlg.allSettings)
            columnsId = self.columnsId
            if self.isTree:
                columnsId = ['text'] + columnsId
            record = [result[col].strip() for col in columnsId]
            parent, iid, text = parent, None, ''
            if self.isTree:
                text = record[0]
                record = record[1:]
            self.tree.insert(parent, 'end', iid=iid, text=text, values=record, open=True)

    def onEdit(self):
        iid = self.tree.focus()
        if iid:
            value = self.tree.set
            columnsId = self.columnsId
            pair = [(col, value(iid, col)) for col in columnsId]
            xmlDlg = self.xmlDlgWindow(pair, isEdit=True)
            dlg = TreeDialog(self, title='Edit', xmlFile=xmlDlg, isFile=False)
            if dlg.allSettings:
                result = dict(dlg.allSettings)
                record = [result[col].strip() for col in columnsId]
                for k, col in enumerate(columnsId):
                    self.tree.set(iid, col, record[k])

    def onDel(self):
        iid = self.tree.focus()
        if iid: self.tree.delete(iid)

    def setValue(self, value, sep=('|', ',')):
        seprow, sepcol = sep
        lista = self.tree.get_children('')
        self.tree.delete(*lista)
        if value == '': return
        maxCol = len(self.columnsId) - 1
        if self.isTree: maxCol += 3
        bDatos = [map(lambda x: x.strip(), record.split(sepcol, maxCol)) for record in value.split(seprow)]
        parent, iid, text = '', None, ''
        for record in bDatos:
            if self.isTree:
                parent, iid, text = record[:3]
                record = record[3:]
            self.tree.insert(parent, 'end', iid=iid, text=text, values=record, open=True)

    def getValue(self):
        stack = list(self.tree.get_children('')[::-1])
        bDatos = []
        while stack:
            iid = stack.pop()
            iidValues = []
            if self.isTree:
                iidValues = [self.tree.parent(iid), iid, self.tree.item(iid, 'text')]
            iidValues = iidValues + list(self.tree.item(iid, 'values'))
            iidValStr = ','.join(iidValues)
            bDatos.append(iidValStr)
            children = self.tree.get_children(iid)
            if children:
                stack.extend(list(children)[::-1])
        return '|'.join(bDatos)


class settSlider(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        self.setValue(self.default)
        valRange = map(int, options.get('range').split(','))
        scale = ttk.Scale(self, variable=self.value, #showvalue=0,
                           from_=valRange[0], to=valRange[-1])
                         #orient=tk.HORIZONTAL
        scale.pack(side=tk.RIGHT, fill=tk.X, expand=1)
        if len(valRange) == 3: scale.configure(resolution=valRange[1])
        ttk.Entry(self, textvariable=self.value).pack(side=tk.RIGHT, fill=tk.X)


class settNumber(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        ttk.Label(self, text=options.get('label'), width=20, anchor=tk.NW).pack(side=tk.LEFT)
        if options.get('id'): self.id = options.get('id').lower()
        self.default = options.get('default', '')
        # valid percent substitutions (from the Tk entry man page)
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        func = self.validateNumber
        vcmd = (self.register(func),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry = entry = tk.Entry(self, name=self.id, textvariable=self.value, validate='key', validatecommand=vcmd)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=1)
        self.setValue(self.default)

    def validateNumber(self, d, i, P, s, S, v, V, W):
        return S.isdigit()

    def setValue(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
        pass


class settText(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        self.name = wdgName
        baseWidget.__init__(self, master, name=wdgName, id=options.get('id', ''))
        self.setGUI(options)

    def setGUI(self, options):
        ttk.Label(self, name='textlbl', text=options.get('label'),
                 width=20, anchor=tk.NW).pack(side=tk.LEFT)
        self.value = tk.StringVar()
        self.default = options.get('default', '')
        self.setValue(self.default)
        if options.get('id'):
            self.id = options.get('id').lower().replace('.', '__')
            ttk.Entry(self, name=self.id, textvariable=self.value).pack(side=tk.RIGHT, fill=tk.X, expand=1)
        else:
            ttk.Label(self, textvariable=self.value).pack(side=tk.RIGHT, fill=tk.X, expand=1)

    def setValue(self, value):
        if value == None:
            self.value.set('')
        else:
            self.value.set(value)

    def getValue(self):
        return self.value.get() if self.value.get() != '' else ''


class settBool(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name', '').lower()
        baseWidget.__init__(self, master, name=wdgName, id=options.get('id', ''))
        if options.has_key('group'):
            groupName = options['group']
            self.value = self.form.getGroupVar(groupName)
        else:
            self.setVarType('boolean')
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        self.id = id = options.get('id', '').lower()
        self.default = options.get('default') == 'true'
        if options.has_key('group'):
            value_on = id
            if self.default: self.setValue(id)
        else:
            value_on = True
            self.setValue(self.default)
        chkbtn = ttk.Checkbutton(self, name=self.id, variable=self.value,
                                onvalue=value_on,
                                command=self.onClick)
        chkbtn.pack(side = tk.RIGHT)
        ttk.Label(self, name="boollbl", text=options.get('label'), width=20, anchor=tk.NW)\
            .pack(side = tk.LEFT, fill=tk.X, expand=tk.YES)

    def isValueSetToDefault(self):
        return self.getValue() == self.default

    def setValue(self, value):
        self.value.set(value)

    def getValue(self):
        value = self.value.get()
        if isinstance(value, basestring):
            value = (value == self.id)
        return value

    def onClick(self):
        try:
            self.form.onClickEvent(self._id)
        except:
            pass


class settAction(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name', '').lower()
        baseWidget.__init__(self, master, name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        if options.get('id'): self.id = options.get('id').lower()
        self.value = options.get('default')
        ttk.Button(self, name=self.id, text=options.get('label'), command=self.onClick).pack(side=tk.RIGHT, fill=tk.X,
                                                                                            expand=1)

    def onClick(self):
        try:
            self.form.onClickEvent(self._id)
        except:
            pass

    def isValueSetToDefault(self):
        return True

    def setValue(self, value):
        pass

    def getValue(self):
        return None

    def setListener(self, function):
        pass

    def callListener(self, *args):
        pass


class settSep(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower().lower()
        baseWidget.__init__(self, master, name=wdgName)
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        if options.get('type', None) == 'lsep': ttk.Label(self, text=options.get('label')).pack(side=tk.LEFT)
        if not options.has_key('noline'):
            color = options.get('color', 'red')
            tk.Frame(self, relief=tk.RIDGE, height=2, bg=color).pack(side=tk.RIGHT, fill=tk.X, expand=1)

    def getSettingPair(self):
        return (None, None)

    def isValueSetToDefault(self):
        return True

    def setValue(self, value):
        pass

    def getValue(self):
        return None

    def setListener(self, function):
        pass


class settContainer(baseWidget):
    def __init__(self, master, **options):
        keys = set(('side', 'label', 'scrolled', 'type')).intersection(options)
        contoptions = {key:options.pop(key) for key in keys}
        packSide = contoptions.get('side', 'top')
        self.side = dict(top=tk.TOP, bottom=tk.BOTTOM, left=tk.LEFT, right=tk.RIGHT).get(packSide, tk.TOP)
        wdgName = options.get('name', '').lower().replace('.', '_')
        id = options.get('id', wdgName).lower()
        if id != wdgName:
            self.id = id
        baseWidget.__init__(self, master, **options)
        self.name = wdgName

        self.innerframe = self
        if contoptions.has_key('label'):
            outerframe = tk.LabelFrame(self, text=contoptions.get('label'))
            outerframe.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
            if contoptions.get('scrolled', 'false') == 'false':
                self.innerframe = innerframe = settContainer(self, name="innerframe",
                                                                side=self.side)
                innerframe.pack(in_=outerframe, side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        else:
            outerframe = tk.Frame(self)
            outerframe.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        if contoptions.get('scrolled', 'false') == 'true':
            outerframe.grid_columnconfigure(0, weight=1)
            outerframe.grid_columnconfigure(1, weight=0)
            outerframe.grid_rowconfigure(0, weight=1)

            self.vsb = tk.Scrollbar(outerframe, orient="vertical", )
            self.vsb.grid(row=0, column=1, sticky=tk.NS)

            self.canvas = tk.Canvas(outerframe, name="canvas", borderwidth=0)
            self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

            self.canvas.configure(yscrollcommand=self.vsb.set)
            self.vsb.configure(command=self.canvas.yview)

            self.canvas.xview_moveto(0)
            self.canvas.yview_moveto(0)

            self.innerframe = innerframe = settContainer(self, name="innerframe",
                                                            side=self.side)
            innerframe.pack_forget()
            self.innerframeId = self.canvas.create_window((0, 0),
                                                          window=innerframe,
                                                          anchor="nw",
                                                          tags="innerframe")


            self.canvas.bind("<Configure>", self._OnCanvasConfigure)
            self.innerframe.bind("<Configure>", self._OnInnerFrameConfigure)

    # def _OnCanvasConfigure(self, event):
    #     canvas = event.widget
    #     canvas.itemconfig(self.innerframeId, width=event.width)
    #
    # def _OnInnerFrameConfigure(self, event):
    #     height = event.height
    #     width = event.width
    #     if height <= self.canvas.winfo_reqheight():
    #         self.vsb.grid_forget()
    #     else:
    #         self.vsb.grid(row=0, column=1, sticky=tk.NS)
    #     self.canvas.config(scrollregion=(0, 0, width, height))

    def _OnCanvasConfigure(self, event):
        if self.innerframe.winfo_reqheight() <= self.canvas.winfo_height():
            self.vsb.grid_remove()
        else:
            self.vsb.grid()

        if self.innerframe.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.innerframeId, width=self.canvas.winfo_width()-4)

    def _OnInnerFrameConfigure(self, event):
        size = (self.innerframe.winfo_reqwidth(), self.innerframe.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        options = {}
        if self.innerframe.winfo_reqwidth() != self.canvas.winfo_width():
            width = self.innerframe.winfo_reqwidth()
            options['width'] = width
        if self.innerframe.winfo_reqheight() <= self.canvas.winfo_height():
            height = self.innerframe.winfo_reqheight()
            options['height'] = height
        if options:
            self.canvas.config(**options)

    def isValueSetToDefault(self):
        return True

    def setValue(self, value):
        pass

    def getValue(self):
        return self.innerframe

    def applyGeoManager(self, widget):
        innerframe = self.innerframe
        widget.pack(in_=innerframe, side=self.side, expand=tk.YES, fill=tk.X,
                    ipadx=2, ipady=2, padx=2, pady=2, anchor=tk.NW)


class settFragment(baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name', '').lower()
        baseWidget.__init__(self, master, name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        if options.get('id'): self.id = options.get('id').lower()
        tk.Frame(self, name=self.id).pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
