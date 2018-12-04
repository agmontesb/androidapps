# -*- coding: utf-8 -*-
import os
import datetime

import Android as android
from Android import Activity
from Android.content.Intent import Intent
from AppCompat import AppCompatResources as appcompat
from CapturaDatosBVC import getFormIndicesBVC, getWebData, getFormAccionesBVC, indicesFields, eodFields, intradiaFields, \
    finalEODFields, outDirectory, processarDB, csvFileFor
from CapturaDatosBVC import tableIndicesBody, tableEODBody, tableIntradiaBody

from DatosBVCManager import R
import Tkinter as tk
from sharedObjects import threadManager, PROCESS_MESSAGE, PROCESS_DATA
import tkFileDialog
import idewidgets
from datascience import *
import numpy as np
import sharedObjects


class MainActivity(Activity):

    def onCreate(self):
        Activity.onCreate(self)
        self.dummy = None
        self.bilboard = tk.StringVar()
        self.datosEOD = None
        self.datosIntradia = None
        self.datosIndices = None
        self.dateProcess = None
        thManager = threadManager(guiOwner=self.frame, numWorkers=3)
        self.thManager = thManager

        self.setContentView(R.layout.MainActivity)

    def onClickEvent(self, resourceEntry):
        form = self.form
        res = self.getResources()
        resid = res.getIdentifier(resourceEntry, defType='id')
        if resid == R.id.getData:
            day = form.diafecha.getValue()
            month = form.mesfecha.getValue()
            year = form.aniofecha.getValue()
            self.dateProcess = (year, month, day)
            bFlag = form.copiatexto.getValue()
            if bFlag:
                importerPath = tkFileDialog.askdirectory(title='Enter path for KodiScriptImporter module')
                self.importerPath = importerPath
            formUrl = getFormIndicesBVC(year, month, day)
            startEq = 'lt("iday_",1)'
            thManager = self.thManager
            thManager.loadThread(getWebData, (formUrl, tableIndicesBody),
                                 {}, self.processMessage,
                                 processTag='iday_datosIndices',
                                 startEq=startEq)
            formUrl = getFormAccionesBVC(year, month, day)
            thManager.loadThread(getWebData, (formUrl, tableEODBody),
                                 {}, self.processEOD,
                                 processTag='datos_EOD',
                                 startEq=startEq)

            result = idewidgets.waitWindow(self, self.bilboard, 'dummy', thManager.lock)

            anIntent = Intent(component=('DatosBVC', 'DatosEod'))
            extras = dict(datosEOD=self.datosEOD, datosIntradia=self.datosIntradia)
            anIntent.putExtras(extras)
            self.startActivity(anIntent)

    def onChangeSelEvent(self, resid):
        form = self.form
        res = self.getResources()
        resid = res.getIdentifier(resid, defType='id')
        if resid == R.id.fechaProceso:
            selection = form.fechaproceso.getValue()
            if selection == '1':
                ddate = datetime.datetime.now()
                form.diafecha.setValue(str(ddate.day))
                form.mesfecha.setValue(str(ddate.month))
                form.aniofecha.setValue(str(ddate.year))

    def processEOD(self, *args, **kwargs):
        form = self.form
        msgId, processTag, answer = args
        if msgId == sharedObjects.PROCESS_START:
            self.datosEOD = []
            thrTag = 'Procesando datos acciones'
            self.bilboard.set(thrTag)
        elif msgId == PROCESS_DATA:
            self.datosEOD = answer
            if self.importerPath:
                fileName = 'bvc_%s%s%s02_eod.csv' % self.dateProcess
                fileName = os.path.join(self.importerPath, fileName)
                csvFileFor(answer, fileName)
        elif msgId == sharedObjects.PROCESS_END:
            year, month, day = self.dateProcess
            startEq = 'lt("iday_",1)'
            for k, row in enumerate(self.datosEOD):
                nemo = row[0]
                urlTemplate = getFormAccionesBVC(year, month, day, nemo='xxxxxxxxxx')
                urlTemplate = urlTemplate.replace('xxxxxxxxxx', '{:10s}')
                """Para cada linea de datosEOD se genera un proceso. debido a 
                la startEq utilizada, el proceso es secuencial. Utilizando 
                otra startEq se podria utilizar los tres threads de que dispone
                el thread manager thManager
                """
                formUrl = urlTemplate.format(nemo)
                self.thManager.loadThread(getWebData, (formUrl, tableIntradiaBody),
                                          {}, self.processMessage,
                                          processTag='iday_%s' % nemo,
                                          startEq=startEq)
        elif msgId == PROCESS_MESSAGE:
            pass
        else:
            pass

    def processMessage(self, *args, **kwargs):
        """
        Proceso de la informacion recopilada. El flujo de la aplicacion
        es lineal, para asimilarlo al comportamiento de la aplicacion de
        excel.
        :param args: Segun lo definido como mensajes
        :param kwargs: Segun lo definido como mensajes
        :return:
        """
        datosIndices, datosEOD, datosIntradia = self.datosIndices, self.datosEOD, self.datosIntradia
        form = self.form

        msgId, thrTag, message = args
        thrTag = thrTag[5:]
        if msgId == sharedObjects.PROCESS_START:
            if thrTag == 'datosIndices':
                self.datosIntradia = []
                self.datosIndices = []
                thrTag = "Procesando datos indicadores"
                self.bilboard.set(thrTag)
            else:
                indx = [x[0] for x in datosEOD].index(thrTag) + 1
                thrTag = 'Procesando ({:0>2}/{}): {}'.format(indx, len(datosEOD), thrTag)
                self.bilboard.set(thrTag)
        elif msgId == sharedObjects.PROCESS_DATA:
            if thrTag == 'datosIndices':
                date = '/'.join(self.dateProcess)
                self.datosIndices = map(lambda x: (date,) + x, message)
                if self.importerPath:
                    fileName = 'bvc_%s%s%s01_indicadores.csv' % self.dateProcess
                    fileName = os.path.join(self.importerPath, fileName)
                    csvFileFor(self.datosIndices, fileName)
            else:
                mnemo = thrTag
                date = '/'.join(self.dateProcess)
                message = map(lambda x: (mnemo, date) + x, message)
                self.datosIntradia.extend(message)
                if self.importerPath:
                    fileName = 'bvc_%s%s%s03_%s.csv' % (self.dateProcess + (mnemo,))
                    fileName = os.path.join(self.importerPath, fileName)
                    csvFileFor(message, fileName)
            return
        elif msgId == sharedObjects.PROCESS_END:
            if thrTag != 'datosIndices' and thrTag == datosEOD[-1][0]:
                """Debido a la naturaleza secuencial de la aplicacion, en este
                punto se sabe que se recibio el intradia de la ultima especie 
                registrada en la tabla EOD"""
                """ ** Colocar la logica de los procesos """
                if form.actualizarbd.getValue():    #Actualizar bases de datos
                    # tablas = processarDB(self.dateProcess, datosEOD, datosIntradia, datosIndices)
                    # tablaEOD, tablaIntradia = tablas
                    # filename = '{}{:0>2}{:0>2}_eod_table.csv'.format(*self.dateProcess)
                    # filename = os.path.join(self.importerPath, filename)
                    # tablaEOD.to_csv(filename)
                    # filename = '{}{:0>2}{:0>2}_intradia_table.csv'.format(*self.dateProcess)
                    # filename = os.path.join(outDirectory, filename)
                    # tablaIntradia.to_csv(filename)
                    pass
                if form.analisisdiario.getValue():  # Analisis diario
                    pass

                if form.copiatexto.getValue():      # Hacer copia a archivo texto
                    pass

                """Con la siguiente instruccion se cierra el dialogo modal."""

                thrTag = "FINAL DE PROCESO"
                self.bilboard.set(thrTag)
                self.dummy = False
        else:
            message = str(message)
        self.form.messageboard.setValue(message)



if __name__ == '__main__':
    Root = tk.Tk()
    Root.withdraw()
    mainWindow = MainActivity()
    Root.wait_window(mainWindow)


