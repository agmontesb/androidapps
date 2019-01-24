# -*- coding: utf-8 -*-
import collections


class ClossureTable(object):
    def __init__(self, dbase, tablename, idcolumn, parentcolumn):
        super(ClossureTable, self).__init__()
        self._dbase = dbase
        self._tablename = tablename
        self._idcolumn = idcolumn
        self._parentcolumn = parentcolumn
        # self.onCreate(dbase)
        dbase.insert = self.decorateIDU(dbase.insert)
        dbase.delete = self.decorateIDU(dbase.delete)
        dbase.update = self.decorateIDU(dbase.update)

    @staticmethod
    def onCreate(db):
        '''
        The clossure table is a special table that stores the relation between the
        records in COMPONENT_TABLE.
        it has three columns:
            'predecessor' -> Nodo aguas arriba en el camino de la raiz al successor
            'successor' -> Nodo aguas abajo partiendo del predecessor
            'depth' ->  Niveles entre el predeccessor hasta el successor
        '''
        SQL_CREATE_TABLE = "CREATE TABLE " + 'clossure' + " ("
        SQL_CREATE_TABLE += 'predecessor' + " INTEGER NOT NULL, "
        SQL_CREATE_TABLE += 'successor' + " INTEGER NOT NULL, "
        SQL_CREATE_TABLE += 'depth' + " INTEGER NOT NULL);"
        db.execSQL(SQL_CREATE_TABLE)

    def decorateIDU(self, func):
        def wrapper(tablename, *args, **kwargs):
            fname = func.__name__
            if tablename == self._tablename:
                if fname == 'insert':
                    nodeid = func(tablename, *args, **kwargs)
                    dmy, values, = args
                    parent = values[self._parentcolumn]
                    self.insertClossureRecords(nodeid, parent)
                    return nodeid
                if fname == 'delete':
                    selection, selectionArgs = args
                    if selection.startswith(self._idcolumn):
                        nodes = [selectionArgs]
                    else:
                        cursor = self._dbase.query(
                            table=self._tablename,
                            columns=(self._idcolumn,),
                            selection=selection,
                            selectionArgs=selectionArgs
                        )
                        nodes = cursor.fetchall()
                    toDelete = set()
                    for node, in nodes:
                        delta = self.deleteClossureRecords(node)
                        toDelete.update(delta)
                    selection = self._idcolumn + " IN ({})".format(', '.join(map(str, toDelete)))
                    selectionArgs = None
                    args = [selection, selectionArgs]
                elif fname == 'update':
                    values, selection, selectionArgs = args
                    if self._parentcolumn in values:
                        parent = self._parentcolumn
                        self.updateClossureTable(values[parent], selection, selectionArgs)
                    pass
            return func(tablename, *args, **kwargs)
        return wrapper

    def insertClossureRecords(self, node, parent, offset=-1):
        db = self._dbase
        componentStack = self.getAllAncestors(parent)
        fieldnames = ('predecessor', 'successor', 'depth')
        maxdepth = len(componentStack) + max(0, offset)
        trnf = lambda x: db.insert(
            'clossure', None,
            dict(zip(fieldnames, (x[1], node, maxdepth - x[0])))
        )
        map(trnf, enumerate(componentStack))
        if offset == -1:
            trnf((maxdepth, node))

    def deleteClossureRecords(self, node):
        whereClauseStr = '(successor IN ({0})) OR (predecessor IN ({0}))'
        return self._deleteClossureRecords(node, whereClauseStr)

    def updateClossureTable(self, newParent, selection, selectionArgs):
        cursor = self._dbase.query(
            table=self._tablename,
            columns=(self._idcolumn,),
            selection=selection,
            selectionArgs=selectionArgs
        )
        for node, in cursor.fetchall():
            descendants = self._deleteNodePredecessor(node)
            qstr = ', '.join(map(str, descendants))
            whereClauseStr = '(successor IN ({0}) AND (predecessor = ?))'
            kwargs = dict(
                table='clossure',
                columns=('successor','depth',),
                selection=whereClauseStr.format(qstr),
                selectionArgs=(node,),
                orderBy='depth ASC'
            )
            cursor = self._dbase.query(**kwargs)
            trnfcn = lambda x: self.insertClossureRecords(x[0], newParent, offset=x[1])
            map(trnfcn, cursor.fetchall())

    def _deleteNodePredecessor(self, node):
        whereClauseStr = '(successor IN ({0}) AND NOT (predecessor IN ({0})))'
        return self._deleteClossureRecords(node, whereClauseStr)

    def _deleteClossureRecords(self, node, whereClauseStr):
        descendants = self.getAllDescendants(node)
        qstr = ', '.join(map(str, descendants))
        kwargs = dict(
            whereClause=whereClauseStr.format(qstr),
        )
        cursor = self._dbase.delete('clossure', **kwargs)
        return descendants

    def getAllDescendants(self, source_node, addDepth=False, inDepth=None):
        sel_string = 'predecessor=?'
        if inDepth:
            sel_string += ' AND depth={}'.format(inDepth)
        kwargs = dict(
            table='clossure',
            columns=('successor', 'depth'),
            selection=sel_string,
            selectionArgs=(source_node,),
            orderBy='depth ASC'
        )
        cursor = self._dbase.query(**kwargs)
        answ = collections.OrderedDict(cursor.fetchall())
        if addDepth:
            return answ
        return answ.keys()

    def getAllDescendantsRecords(self, source_node, inDepth=None):
        depth = self.getAllDescendants(source_node, addDepth=True, inDepth=inDepth)
        kwargs = dict(
            table=self._tablename,
            selection='{0} IN ({1})'.format(self._idcolumn, str(depth.keys())[1:-1]),
        )
        cursor = self._dbase.query(**kwargs).fetchall()
        return sorted(cursor, key=lambda x:(depth[x[0]],x[0]))

    def getDirectDescendants(self, source_node):
        kwargs = dict(
            table='clossure',
            columns=None,
            selection='predecessor=? AND depth=1',
            selectionArgs=(source_node,),
        )
        cursor = self._dbase.query(**kwargs)
        return map(lambda x: x[1], cursor.fetchall())

    def getAllSiblings(self, source_node):
        cursor = self._dbase.query(
            table=self._tablename,
            columns=(self._parentcolumn,),
            selection=self._idcolumn + ' = ?',
            selectionArgs=(source_node,)
        )
        parent, = cursor.fetchone()
        return self.getDirectDescendants(parent)

    def getAllAncestors(self, source_node, addDepth=False):
        kwargs = dict(
            table='clossure',
            columns=('predecessor', 'depth'),
            selection='successor=?',
            selectionArgs=(source_node,),
            orderBy='depth DESC'
        )
        cursor = collections.OrderedDict(self._dbase.query(**kwargs).fetchall())
        if addDepth:
            return cursor
        return cursor.keys()

    def getAllAncestorsRecords(self, source_node):
        depth = self.getAllAncestors(source_node, addDepth=True)
        kwargs = dict(
            table=self._tablename,
            selection='{0} IN ({1})'.format(self._idcolumn, str(depth.keys())[1:-1]),
        )
        cursor = self._dbase.query(**kwargs).fetchall()
        return sorted(cursor, key=lambda x:(-depth[x[0]],x[0]))
