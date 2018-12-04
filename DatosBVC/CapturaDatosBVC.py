# -*- coding: utf-8 -*-
import os
import Tkinter as tk
import tkSimpleDialog
import tkFileDialog

import idewidgets
from Android.BasicViews import settAction, settDDList
import datetime
from collections import OrderedDict

import formDetector
import sharedObjects
from sharedObjects import threadManager, PROCESS_MESSAGE, PROCESS_DATA
import network
import CustomRegEx

from datascience import *
import numpy as np

outDirectory = r'E:/basura'

datosEOD      = None
datosIntradia = None
datosIndices = None

bvc_url = r'https://www.bvc.com.co/pps/tibco/portalbvc/Home/Mercados/enlinea/acciones'
indicesbvc_url = r'https://www.bvc.com.co/pps/tibco/portalbvc/Home/Mercados/enlinea/indicesbursatiles?com.tibco.ps.pagesvc.renderParams.sub45d083c1_14321f5c9c5_-78350a0a600b=action%3Dmercado%26org.springframework.web.portlet.mvc.ImplicitModel%3Dtrue%26'
initConf = r'curl  --user-agent "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36" --cookie-jar "cookies.lwp" --location'

tableIndicesBody = r'(?#<div id="text_27" .tr<td{1.a.*=&td1& 2.*=&td2& 3.*=&td3& 4.*=&td4& 5.*=&td5&}>*>)'
indicesFields = ['Fecha', 'Mnemotecnico', 'TIPO INDICADOR', 'ACTUAL', 'ANTERIOR', 'Variacion %']
eodFields = ['Mnemotecnico', 'CANTIDAD TRANSADA', 'VOLUMEN NEGOCIADO', 'ACTUAL', 'Variacion %']
tableEODHead = r'(?#<table id="textTitulos" .tr<th{1.a.*=&Mnemo& 2.*=&Cantidad& 3.a.*=&Volumen& 4.*=&PCierre& 5.a.*=&Variacion&}>*>)'
tableEODBody = r'(?#<div id="tbAcNegociadas" .tr<td{1.a.*=&td1& 2.*=&td2& 3.*=&td3& 4.*=&td4& 5.*=&td5&}>*>)'
intradiaFields = ['Mnemotecnico', 'Fecha', 'Hora_Trans', 'Precio', 'Cantidad', 'Promedio', 'oper']
tableIntradiaHead = r'(?#<table id="texto_33" .tr<th{1.*=&td1& 2.*=&td2& 3.*=&td3& 4.*=&td4& 5.*=&td5&}>*>)'
tableIntradiaBody = r'(?#<table id="texto_27" .tr<td{1.*=&td1& 2.*=&td2& 3.*=&td3& 4.*=&td4& 5.*=&td5&}>*>)'

finalEODFields = ['Fecha', 'Mnemotecnico', 'Emisor', 'ESPECIE', '# OPER',
                  'CANTIDAD TRANSADA', 'VOLUMEN NEGOCIADO', 'PART.%', 'MAXIMO',
                  'MINIMO', '1aOperacion', 'PROMEDIO', 'ACTUAL', 'Variacion %',
                  'Fecha Cierre', 'PrecioMedio_GI', 'Volumen_GI', 'NumOper_GI',
                  'PrecioMedio_PI', 'Volumen_PI', 'NumOper_PI']

def getWebData(url, regexPattern, initConf=None, **kwargs):
    yield [PROCESS_MESSAGE, ('Contactando sitio web bvc',), kwargs]
    if not initConf:
        initConf = r'curl  --user-agent "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36" --cookie-jar "cookies.lwp" --location'
    net = network.network(initConf)
    content, end_url = net.openUrl(url)
    if isinstance(content, Exception):
        raise content
    yield [PROCESS_MESSAGE, ('Pagina web entregada',), kwargs]

    reg = CustomRegEx.compile(regexPattern)

    response = reg.findall(content)
    yield [PROCESS_DATA, (response,), kwargs]

def getFormAccionesBVC(year, month, day, nemo=''):
    allSettings = [('fa_action',
                    '/pps/tibco/portalbvc/Home/Mercados/enlinea/acciones?com.tibco.ps.pagesvc.action=portletAction&com.tibco.ps.pagesvc.targetSubscription=5d9e2b27_11de9ed172b_-74187f000001&action=buscar'),
                    ('fa_id', 'formulario'),
                    ('fa_method', 'post'),
                    ('fa_name', 'busqueda'),
                    ('tipoMercado', '1'),
                    ('diaFecha', '15'),
                    ('mesFecha', '04'),
                    ('anioFecha', '2018'),
                    ('nemo', '')]
    formAttr = dict([(key[3:], value) for key, value in allSettings if key.startswith('fa_')])
    formFields = [(key, value) for key, value in allSettings if not key.startswith('fa_')]
    formFields = OrderedDict(formFields)
    formFields['diaFecha'] = '{:0>2}'.format(day)
    formFields['mesFecha'] = '{:0>2}'.format(month)
    formFields['anioFecha'] = str(year)
    formFields['nemo'] = '{:10s}'.format(nemo) if nemo else ''
    refererOpt = '-e ' + '"' + bvc_url + '"'
    curlCommand = formDetector.getCurlCommand(bvc_url, formAttr, formFields.items(), refererOpt)
    return curlCommand

def getFormIndicesBVC(year, month, day):
    allSettings = [ ('fa_action',
                        '/pps/tibco/portalbvc/Home/Mercados/enlinea/indicesbursatiles?com.tibco.ps.pagesvc.renderParams.sub45d083c1_14321f5c9c5_-78350a0a600b=action%3Dmercado%26org.springframework.web.portlet.mvc.ImplicitModel%3Dtrue%26&com.tibco.ps.pagesvc.action=portletAction&com.tibco.ps.pagesvc.targetSubscription=45d083c1_14321f5c9c5_-78350a0a600b&action=buscar'),
                    ('fa_id', 'form'),
                    ('fa_method', 'post'),
                    ('fa_name', 'forma'),
                    ('tipoMercado', '1'),
                    ('dia', '15'),
                    ('mes', '04'),
                    ('anio', '2018'),
                    ('codigoIndice', 'all'),
                    ('mercadoIn', 'RENTA VARIABLE'),
                    ('mercadono', 'all')]
    formAttr = dict([(key[3:], value) for key, value in allSettings if key.startswith('fa_')])
    formFields = [(key, value) for key, value in allSettings if not key.startswith('fa_')]
    formFields = OrderedDict(formFields)
    formFields['dia'] = '{:0>2}'.format(day)
    formFields['mes'] = '{:0>2}'.format(month)
    formFields['anio'] = str(year)
    refererOpt = '-e ' + '"' + indicesbvc_url + '"'
    curlCommand = formDetector.getCurlCommand(indicesbvc_url, formAttr, formFields.items(), refererOpt)
    return curlCommand

def csvFileFor(iterable, filename):
    dataStr = '\n'.join(map(lambda x: '*'.join(x), iterable))
    dataStr = dataStr.replace('.', '').replace(',', '.').replace('*',',')
    with open(filename, 'w') as f:
        f.write(dataStr)

def processarDB(dateProcess, datosEOD, datosIntradia, datosIndices):
    def trnfcn(x):
        x = x.replace('.', '').replace(',', '.')
        try:
            x = float(x)
        except:
            if x.endswith('%'):
                x = float(x[:-1]) / 100
        return x

    def fromArrayToTable(array, arrayFields):
        tableValues = map(lambda x: make_array(*x), zip(*array))
        tableItems = zip(arrayFields, tableValues)
        return Table().with_columns(*tableItems)

    def statOnOneField(twoFieldTable, collectFn, statFields):
        dummy = twoFieldTable.group('Mnemotecnico', collect=collectFn)
        stats = zip(statFields, zip(*dummy['Precio']))
        stats = map(lambda x: (x[0], make_array(*x[1])), stats)
        stats = Table().with_columns(*stats).with_column('Mnemotecnico', dummy['Mnemotecnico'])
        return stats

    def statInversionist(filterTable, colLabels):
        dummy = filterTable.with_column('oper', 1)
        dummy = dummy.select('Mnemotecnico', 'Cantidad', 'Promedio', 'oper')
        dummy = dummy.group('Mnemotecnico', collect=np.sum)
        dummy = dummy.with_column('pmedio', dummy['Promedio sum'] / dummy['Cantidad sum']).drop('Cantidad sum')
        dummy = dummy.relabel(['Promedio sum', 'oper sum', 'pmedio'], colLabels)
        rows_missing = [(key, 0, 0, 0) for key in datosEOD['Mnemotecnico'] if key not in dummy['Mnemotecnico']]
        dummy = dummy.with_rows(rows_missing)
        return dummy

    datosIndices = [map(trnfcn, x) for x in datosIndices]
    datosIndices = fromArrayToTable(datosIndices, indicesFields)
    datosEOD = [map(trnfcn, x) for x in datosEOD]
    datosEOD = fromArrayToTable(datosEOD, eodFields)
    datosIntradia = [map(trnfcn, x) for x in datosIntradia]
    datosIntradia = fromArrayToTable(datosIntradia, intradiaFields)
    # datosIntradia.set_format(['Precio', 'Cantidad', 'Promedio'], formats.NumberFormatter)

    """Se calculan los datos de '1aOperacion', 'MAXIMO', 'MINIMO', 'ACTUAL'"""
    dummy = datosIntradia.select('Mnemotecnico', 'Precio')
    collectFn = lambda x: (x[0], np.max(x), np.min(x), x[-1])
    statFields = ['1aOperacion', 'MAXIMO', 'MINIMO', 'ACTUAL']
    stats = statOnOneField(dummy, collectFn, statFields)
    datosEOD = datosEOD.join('Mnemotecnico', stats.drop('ACTUAL'))

    """Se calculan los datos de '# OPER', 'PROMEDIO'"""
    dummy = datosIntradia
    dummy = statInversionist(dummy, ['VOLUMEN NEGOCIADO', '# OPER', 'PROMEDIO'])
    datosEOD = datosEOD.join('Mnemotecnico', dummy.drop('VOLUMEN NEGOCIADO'))

    """Se calculan los datos de 'Volumen_PI', 'NumOper_PI', 'PrecioMedio_PI'"""
    LIM_PI = 40 * 1000000.0
    dummy = datosIntradia.where('Promedio', are.below_or_equal_to(LIM_PI))
    dummy = statInversionist(dummy, ['Volumen_PI', 'NumOper_PI', 'PrecioMedio_PI'])
    datosEOD = datosEOD.join('Mnemotecnico', dummy)

    """Se calculan los datos de 'Volumen_GI', 'NumOper_GI', 'PrecioMedio_GI'"""
    LIM_GI = 100 * 1000000.0
    dummy = datosIntradia.where('Promedio', are.above_or_equal_to(LIM_GI))
    dummy = statInversionist(dummy, ['Volumen_GI', 'NumOper_GI', 'PrecioMedio_GI'])
    datosEOD = datosEOD.join('Mnemotecnico', dummy)

    """Se agregan las columnas que faltan en la tabla final de datosEOD"""
    volTot = np.sum(datosEOD['VOLUMEN NEGOCIADO'])
    datosEOD['PART.%'] = map(lambda x: x / volTot, datosEOD['VOLUMEN NEGOCIADO'])
    datosEOD = datosEOD.with_column('Fecha', datosIntradia['Fecha'][0])

    """Se procesa la informacion de indicadores"""
    table = datosIndices
    table = table.select(['Fecha', 'Mnemotecnico', 'ACTUAL', 'Variacion %'])
    totalescols = ['# OPER', 'CANTIDAD TRANSADA', 'VOLUMEN NEGOCIADO',
                   'PART.%',
                   'PrecioMedio_GI', 'Volumen_GI', 'NumOper_GI',
                   'PrecioMedio_PI', 'Volumen_PI', 'NumOper_PI']
    totcols = map(lambda x: (x, sum(datosEOD.column(x))), totalescols)
    table = table.with_columns(*totcols)

    for key in ['1aOperacion', 'MAXIMO', 'MINIMO', 'PROMEDIO']:
        table[key] = 0

    datosEOD = datosEOD.append(table)

    """Se agregan las columnas que faltan para el maquillaje de la tabla final"""
    datosEOD = datosEOD.with_column('Fecha Cierre', datosIntradia['Fecha'][0])
    datosEOD['Emisor'] = datosEOD['Mnemotecnico']
    datosEOD['ESPECIE'] = datosEOD['Mnemotecnico']

    """Se ordenan las columnas de la tabla"""
    itempairs = [(key, datosEOD[key]) for key in finalEODFields]
    datosEOD = Table().with_columns(*itempairs)
    datosEOD = datosEOD.sort('VOLUMEN NEGOCIADO', descending=True)

    """ Se formatea la tabla datosEOD"""
    numbercols = ['# OPER', 'CANTIDAD TRANSADA', 'VOLUMEN NEGOCIADO',
                  'MAXIMO', 'MINIMO', '1aOperacion', 'PROMEDIO', 'ACTUAL',
                  'PrecioMedio_GI', 'Volumen_GI', 'NumOper_GI',
                  'PrecioMedio_PI', 'Volumen_PI', 'NumOper_PI']
    datosEOD = datosEOD.set_format(numbercols, formats.NumberFormatter)
    percentcols = ['PART.%', 'Variacion %']
    datosEOD = datosEOD.set_format(percentcols, formats.PercentFormatter)

    return  datosEOD, datosIntradia


class MyDialog(tkSimpleDialog.Dialog):
    def __init__(self, master, bildboardVar, *args, **kwargs):
        self.bilboardVar = bildboardVar
        tkSimpleDialog.Dialog.__init__(self, master, *args, **kwargs)

    def geometry(self, posStr):
        posx = (self.winfo_screenwidth() - 200)/2
        posy = (self.winfo_screenheight() - 100)/2
        posStr = "%dx%d+%d+%d" % (200, 100, posx, posy)
        tkSimpleDialog.Dialog.geometry(self, posStr)


    def body(self, master):

        tk.Label(master, text="First:").grid(row=0)
        tk.Label(master, text="Second:").grid(row=1)

        self.e1 = tk.Entry(master, textvariable=self.bilboardVar)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print first, second # or something