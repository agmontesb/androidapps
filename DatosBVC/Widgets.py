# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import idewidgets
from Android import BasicViews

class ScrolledList(BasicViews.baseWidget):
    def __init__(self, master, **options):
        wdgName = options.get('name').lower()
        self.isTree = options.get('tree', 'false') == 'true'
        BasicViews.baseWidget.__init__(self, master, varType='string', name=wdgName, id=options.get('id', ''))
        self.setGUI(options)
        self.name = wdgName

    def setGUI(self, options):
        if options.get('id'): self.id = options.get('id').lower().replace('.', '__')
        colHeadings = options.get('columnsheadings')
        columnsId = dcolumns = map(lambda x: x.strip(), colHeadings.split(','))
        self.columnsId = columnsId
        values = options.get('default', '')
        self.default = self.parseValues(values)
        uFrame = self

        hbar = ttk.Scrollbar(uFrame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)

        vbar = ttk.Scrollbar(uFrame)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        dshow = 'headings'
        if self.isTree:
            dshow = 'tree ' + dshow
            dcolumns = '#all'
        tree = idewidgets.TreeList(uFrame, show=dshow, columns=columnsId, displaycolumns=dcolumns)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        hbar.config(command=tree.xview)
        vbar.config(command=tree.yview)  # xlink sbar and tree
        tree.config(xscrollcommand=hbar.set)  # move one moves other
        tree.config(yscrollcommand=vbar.set)  # move one moves other
        for column in columnsId:
            tree.heading(column, text=column, anchor=tk.W)
        self.tree = tree

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
        dlg = BasicViews.TreeDialog(self, title='Add', xmlFile=xmlDlg, isFile=False)
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
            dlg = BasicViews.TreeDialog(self, title='Edit', xmlFile=xmlDlg, isFile=False)
            if dlg.allSettings:
                result = dict(dlg.allSettings)
                record = [result[col].strip() for col in columnsId]
                for k, col in enumerate(columnsId):
                    self.tree.set(iid, col, record[k])

    def onDel(self):
        iid = self.tree.focus()
        if iid: self.tree.delete(iid)

    @classmethod
    def parseValues(self, values, sep=('|', ',')):
        if values == '': return
        seprow, sepcol = sep
        bDatos = [map(lambda x: x.strip(), record.split(sepcol))
                  for record in values.split(seprow)]
        return bDatos

    @classmethod
    def unparseValues(self, values, sep=('|', ',')):
        if not values:return ''
        seprow, sepcol = sep
        return seprow.join(map(lambda x: sepcol.join(x), values))

    def setValue(self, bDatos):
        lista = self.tree.get_children('')
        self.tree.delete(*lista)
        if bDatos is None: return
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
            bDatos.append(iidValues)
            children = self.tree.get_children(iid)
            if children:
                stack.extend(list(children)[::-1])
        return bDatos
