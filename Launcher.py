# -*- coding: utf-8 -*-
import sys
import Tkinter as tk
import importlib
import Android.BasicViews as BasicViews
from Android.Intent import Intent
from Android.Activity import Activity
from Android.Activity import ON_CREATE, ON_START, ON_RESUME
from Android.Activity import ON_PAUSE, ON_STOP, ON_DESTROY


PACK_OPTIONS = dict(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
packages = ['TestActivity', 'DatosBVC']
classnames = ['FragmentTest', 'MainActivity']


class App(tk.Tk):

    def __init__(self, starterComponent=None, width=600, height=400):
        tk.Tk.__init__(self)
        self.config(width=width, height=height)
        self.pack_propagate(0)
        self.bind_all("<Control-q>", self.quit)
        self.activetask = None
        self.tasks = dict()
        self.setGUI(starterComponent)

    def setGUI(self, starterComponent):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES,
                         anchor=tk.S, ipadx=2, ipady=2, padx=2, pady=2)
        tk.Button(bottomFrame, text='Home', command=self.activateLauncher).pack(side=tk.LEFT)
        tk.Button(bottomFrame, text='Back', command=self.backbtn).pack(side=tk.RIGHT)
        backStack = self.tasks.setdefault('StarterActivity', [])
        if starterComponent is None:
            frame = BasicViews.settContainer(self, label='Available Apps',
                                                          scrollable='true')
            for k, label in enumerate(packages):
                btn = BasicViews.settAction(frame.innerframe, label=label, id=str(k))
                frame.applyGeoManager(btn)
                pass
        else:
            anIntent = Intent(component=starterComponent)
            activity = self.resolveComponent(anIntent)
            frame = activity(self, anIntent)
            frame.onLifecycleEvent(ON_CREATE)
        backStack.append(frame)
        self.activateLauncher()

    def activateLauncher(self):
        self.setTaskOn('StarterActivity')

    def backbtn(self):
        self.finishActivity()

    def onClickEvent(self, wdgid):
        wdgid = int(wdgid)
        components = zip(packages, classnames)
        package, module = component = components[wdgid]
        if package not in self.tasks:
            anIntent = Intent(component=component)
            self.startActivity(anIntent)
        else:
            self.setTaskOn(package)

    def setTaskOn(self, task):
        if self.activetask == task: return
        if self.activetask: self.setActiveTaskOff()
        self.activetask = task
        self.setActiveTaskOn()

    def setActiveTaskOff(self):
        activetask = self.activetask
        taskStack = self.tasks.setdefault(activetask, [])
        activity = taskStack[-1]
        if isinstance(activity, Activity):
            activity.onLifecycleEvent(ON_PAUSE)
            activity.frame.pack_forget()
            activity.onLifecycleEvent(ON_STOP)
        else:
            activity.pack_forget()
        return taskStack

    def setActiveTaskOn(self):
        activetask = self.activetask
        taskStack = self.tasks.setdefault(activetask, [])
        activity = taskStack[-1]
        if isinstance(activity, Activity):
            activity.onLifecycleEvent(ON_START)
            activity.frame.pack(**PACK_OPTIONS)
            activity.onLifecycleEvent(ON_RESUME)
        else:
            activity.pack(**PACK_OPTIONS)
        return taskStack

    def resolveComponent(self, anIntent):
        selector = anIntent.getSelector()
        component = selector.getComponent()
        if not component:
            # TODO: Establecer la lógica para resolver el intent implícito
            pass
        package, module = component
        try:
            fullmodulename = '%s.%s' % (package, module)
            return getattr(importlib.import_module(fullmodulename), module)
        except Exception as e:
            raise Exception('ActivityNotFoundException')


    def startActivity(self, anIntent, options=None):
        """
        Inicia la ejecución de una actividad. Se supone que el nombre de la actividad
        es igual al nombre del módulo
        :param anIntent: Intent con información para identificar la nueva activity
        :return: Nada
        """
        self.startActivityForResult(anIntent, -1, options)

    def startActivityForResult(self, anIntent, requestCode, options=None):
        activity = self.resolveComponent(anIntent)
        self.setActiveTaskOff()
        newFrame = activity(self, anIntent)
        self.activetask = activetask = anIntent.getPackage()
        taskStack = self.tasks.setdefault(activetask, [])
        taskStack.append(newFrame)
        if requestCode >= 0:
            newFrame.requestcode = requestCode
        newFrame.onLifecycleEvent(ON_CREATE)
        self.setActiveTaskOn()

    def finishActivity(self):
        activetask = self.activetask
        if activetask == 'StarterActivity': return
        taskStack = self.setActiveTaskOff()
        activity = taskStack.pop()
        bflag = hasattr(activity, 'requestcode')
        if bflag:
            requestCode = activity.requestcode
            resultCode, anIntent = activity._result
        activity.onLifecycleEvent(ON_DESTROY)
        del activity.frame
        del activity

        if taskStack:
            activity = taskStack[-1]
            activity.onLifecycleEvent(ON_START)
            activity.frame.pack(**PACK_OPTIONS)
            activity.onLifecycleEvent(ON_RESUME)
            if bflag:
                activity.onActivityResult(requestCode, resultCode, anIntent)
        else:
            self.tasks.pop(self.activetask)
            self.activetask = 'StarterActivity'
            self.setActiveTaskOn()


    def quit(self, event):
        print("quitting...")
        sys.exit(0)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--package', action='store', dest='package', help='Package name')
    parser.add_argument('-a', '--activity', action='store', dest='activity', help='Activity name')
    parser.add_argument('--hasargs', action='store_true', default=False)
    args = parser.parse_args()
    component = None
    if args.hasargs and args.package and args.activity:
        component = (args.package, args.activity)

    app = App(starterComponent=component)
    app.mainloop()
