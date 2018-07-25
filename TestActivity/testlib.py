from Android.BasicViews import settText, settBool, settAction, settDDList
import tkMessageBox
import datetime

class fechaProceso(settDDList):
    def onChangeSel(self):
        selection = self.getValue()
        if selection == '1':
            form = self.form
            ddate = datetime.datetime.now()
            form.diafecha.setValue(str(ddate.day))
            form.mesfecha.setValue(str(ddate.month))
            form.aniofecha.setValue(str(ddate.year))


class actualizarBD(settBool):
    def setValue(self, value):
        print "Cambiando el valor de actualizarBD"
        settBool.setValue(self, value)

class copiaTexto(settBool):
    pass

class submitButton(settAction):
    def __init__(self, master, **options):
        settAction.__init__(self, master, **options)

    def onClick(self):
        tkMessageBox.showinfo('Prueba de Action Button', 'Saludos desde forma')
        form = self.form
        #form.messageboard.setValue('pulsado action button')
        pass
