# -*- coding: utf-8 -*-
import collections

from Tools.aapt.Compile import ResourceUtils
from Tools.aapt.ResourcesValues import Attribute
from Tools.aapt.test.Common import parseNameOrDie

Symbol = collections.namedtuple('Symbol', 'id attribute isPublic')

class Context(object):

    def __init__(self):
        super(Context, self).__init__()
        self.mCompilationPackage = ''
        self.mPackageId = None
        self.mDiagnostics = ResourceUtils.Diagnostics()
        self.mSymbols = None
        self.mNameMangler = None
    
    def getExternalSymbols(self):
        assert self.mSymbols, "test symbols not set"
        return self.mSymbols
    
    def setSymbolTable(self, symbols):
        self.mSymbols =symbols
    
    def getDiagnostics(self):
        assert self.mDiagnostics, "test diagnostics not set"
        return self.mDiagnostics
    
    def getCompilationPackage(self):
        assert self.mCompilationPackage, "package name not set"
        return self.mCompilationPackage
    
    def getPackageId(self):
        assert self.mPackageId, "package ID not set"
        return self.mPackageId
    
    def getNameMangler(self):
        assert self.mNameMangler, "test name mangler not set"
        return self.mNameMangler
    

class ContextBuilder(object):

    def __init__(self):
        super(ContextBuilder, self).__init__()
        self.mContext = Context()

    def setCompilationPackage(self, package):
        self.mContext.mCompilationPackage = package
        return self
    
    def setPackageId(self, id):
        self.mContext.mPackageId = id
        return self
    
    def setSymbolTable(self, symbols):
        self.mContext.mSymbols = symbols
        return self
    
    def setDiagnostics(self, diag):
        self.mContext.mDiagnostics = diag
        return self
    
    def setNameManglerPolicy(self, policy):
        self.mContext.mNameMangler = policy
        return self
    
    def build(self):
        return self.mContext
    

class StaticSymbolTableBuilder(object):

    class SymbolTable(object):

        def __init__(self):
            super(StaticSymbolTableBuilder.SymbolTable, self).__init__()
            self.mSymbols = []
            self.mNameMap = {}
            self.mIdMap = {}

        def findByName(self, name):
            return self.mNameMap.get(name, None)

        def findById(self, id):
            return self.mIdMap.get(id, None)

    def __init__(self):
        super(StaticSymbolTableBuilder, self).__init__()
        self.mSymbolTable = StaticSymbolTableBuilder.SymbolTable()

    def addSymbol(self, name, id, attr=None):
        attr = attr or Attribute()
        symbol = Symbol(id, attr, False)
        self.mSymbolTable.mNameMap[parseNameOrDie(name)] = symbol
        self.mSymbolTable.mIdMap[id] = symbol
        self.mSymbolTable.mSymbols.append(symbol)
        return self
    
    def build(self):
        return self.mSymbolTable
    
