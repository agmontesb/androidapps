# -*- coding: utf-8 -*-
#
# Resources for appCompat:
# https://github.com/aosp-mirror/platform_frameworks_support.git
#
import sys
import Tkinter as tk
import importlib

import Android.BasicViews as BasicViews
from Android.content.ComponentName import ComponentName
from Android.content.Intent import Intent
from Android.app.Activity import Activity
from Android.app.Activity import ON_CREATE, ON_START, ON_RESUME
from Android.app.Activity import ON_PAUSE, ON_STOP, ON_DESTROY
from Android.content.pm.PackageManager import PackageManager

ACTIVITY_SHOW = 'show'
ACTIVITY_HIDE = 'hide'
ACTIVITY_DESTROY = 'destroy'
PACK_OPTIONS = dict(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
ROOT_PACKAGE = 'com.AdroidApps.'

class AppStart(tk.Tk):

    def __init__(self, starterComponent=None, width=600, height=400):
        tk.Tk.__init__(self)
        self.config(width=width, height=height)
        self.pack_propagate(0)
        self.bind_all("<Control-q>", self.quit)
        self.activetask = None
        self.tasks = dict()
        starterComponent = ComponentName(*starterComponent)
        self.setGUI(starterComponent)

    def setGUI(self, starterComponent):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES,
                         anchor=tk.S, ipadx=2, ipady=2, padx=2, pady=2)
        tk.Button(bottomFrame, text='Home', command=self.activateLauncher).pack(side=tk.LEFT)
        tk.Button(bottomFrame, text='Back', command=self.backbtn).pack(side=tk.RIGHT)
        backStack = self.tasks.setdefault('StarterActivity', [])
        anIntent = Intent().setComponent(starterComponent)
        activity = self.resolveComponent(anIntent)
        frame = activity(self, anIntent)
        frame.onLifecycleEvent(ON_CREATE)
        backStack.append(frame)
        self.activateLauncher()

    def activateLauncher(self):
        self.setTaskOn('StarterActivity')

    def backbtn(self):
        self.finishActivity()

    def windowEvent(self, activity, event):
        windowid = hex(16*activity.__hash__())
        display = self.children[windowid]
        if event == ACTIVITY_SHOW:
            display.pack(**PACK_OPTIONS)
        elif event == ACTIVITY_HIDE:
            display.pack_forget()
        elif event == ACTIVITY_DESTROY:
            display.destroy()
        else:
            raise Exception('displayEvent: Not an allowed event')

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
            self.windowEvent(activity, ACTIVITY_HIDE)
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
            self.windowEvent(activity, ACTIVITY_SHOW)
            activity.onLifecycleEvent(ON_RESUME)
        else:
            activity.pack(**PACK_OPTIONS)
        return taskStack

    def resolveComponent(self, anIntent):
        pm = PackageManager()
        component = anIntent.resolveActivity(pm)
        package, fullmodulename = component.getPackageName(), component.getClassName()
        fullmodulename = fullmodulename.split(ROOT_PACKAGE, 1)[-1]
        module = fullmodulename.rsplit('.', 1)[-1]
        try:
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
        self.activetask = activetask = anIntent.getComponent().getPackageName().split(ROOT_PACKAGE, 1)[-1]
        taskStack = self.tasks.setdefault(activetask, [])
        if not options or not taskStack:
            newFrame = activity(self, anIntent)
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
        self.windowEvent(activity, ACTIVITY_DESTROY)
        del activity

        if taskStack:
            activity = taskStack[-1]
            activity.onLifecycleEvent(ON_START)
            self.windowEvent(activity, ACTIVITY_SHOW)
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
