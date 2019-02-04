# -*- coding: utf-8 -*-
import abc
import copy
import sys
import Tkinter as tk
import ttk
import itertools
import locale


class Context(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def method1(self):
        pass

    @abc.abstractmethod
    def method2(self):
        pass


class ContextWrapper(Context):
    def __init__(self, basecontext):
        super(ContextWrapper, self).__init__()
        self.base = basecontext

    def attatchBaseContext(self, basecontext):
        if self.base:
            raise Exception('IllegalStateException: "Base context already set"')
        self.base = basecontext

    # def __getattribute__(self, name):
    #     bFlag = super(ContextWrapper, self).__
    #     if hasattr(self.base, name):
    #         return getattr(self.base, name)
    #     raise AttributeError

    def method1(self):
        return self.base.method1()

    def method2(self):
        return self.base.method2()


class Application(ContextWrapper):
    def __init__(self):
        base = ContextImpl()
        super(Application, self).__init__(base)
        pass

    def app1method(self):
        print 'app1method'

    def app2method(self):
        print 'app2method'


class ContextImpl(Context):
    def method1(self):
        print 'method1'

    def method2(self):
        print 'method2'

class AppStart(tk.Tk):
    def __init__(self, width=600, height=400):
        tk.Tk.__init__(self)
        self.config(width=width, height=height)
        self.pack_propagate(0)
        self.bind_all("<Control-q>", self.quit)
        self.setGUI()

    def activateLauncher(self):
        pass

    def backbtn(self):
        pass

    def setGUI(self):
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.YES,
                         anchor=tk.S, ipadx=2, ipady=2, padx=2, pady=2)
        tk.Button(bottomFrame, text='Home', command=self.activateLauncher).pack(side=tk.LEFT)
        tk.Button(bottomFrame, text='Back', command=self.backbtn).pack(side=tk.RIGHT)
        self.nbook = nbook = ttk.Notebook(self)
        self.nbook.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        f1 = tk.Frame(nbook)
        print nbook.add(f1)
        tk.Button(f1, text='Primer TAB').pack()
        f2 = tk.Frame(nbook)
        print nbook.add(f2)
        tk.Button(f2, text='Segundo TAB').pack()
        print nbook.tabs()
        nbook.hide(0)


    def quit(self, event):
        print("quitting...")
        sys.exit(0)

class notebook:

        # initialization. receives the master widget
        # reference and the notebook orientation
        def __init__(self, master, side=tk.LEFT):

            self.active_fr = None
            self.count = 0
            self.choice = tk.IntVar(0)

            # allows the TOP and BOTTOM
            # radiobuttons' positioning.
            if side in (tk.TOP, tk.BOTTOM):
                self.side = tk.LEFT
            else:
                self.side = tk.TOP

            # creates notebook's frames structure
            self.rb_fr = tk.Frame(master, borderwidth=2, relief=tk.RIDGE)
            self.rb_fr.pack(side=side, fill=tk.BOTH)
            self.screen_fr = tk.Frame(master, borderwidth=2, relief=tk.RIDGE)
            self.screen_fr.pack(fill=tk.BOTH)

        # return a master frame reference for the external frames (screens)
        def __call__(self):

            return self.screen_fr

        # add a new frame (screen) to the (bottom/left of the) notebook
        def add_screen(self, fr, title):

            b = tk.Radiobutton(self.rb_fr, text=title, indicatoron=0, \
                            variable=self.choice, value=self.count, \
                            command=lambda: self.display(fr))
            b.pack(fill=tk.BOTH, side=self.side)

            # ensures the first frame will be
            # the first selected/enabled
            if not self.active_fr:
                fr.pack(fill=tk.BOTH, expand=1)
                self.active_fr = fr

            self.count += 1
            # returns a reference to the newly created
            # radiobutton (allowing its configuration/destruction)
            return b

        # hides the former active frame and shows
        # another one, keeping its reference
        def display(self, fr):
            self.active_fr.forget()
            fr.pack(fill=tk.BOTH, expand=1)
            self.active_fr = fr


# app = AppStart()
# app.mainloop()
def setGUI():
    a = tk.Tk()
    n = notebook(a, tk.LEFT)

    # uses the notebook's frame
    f1 = tk.Frame(n())
    b1 = tk.Button(f1, text="Button 1")
    e1 = tk.Entry(f1)
    # pack your widgets before adding the frame
    # to the notebook (but not the frame itself)!
    b1.pack(fill=tk.BOTH, expand=1)
    e1.pack(fill=tk.BOTH, expand=1)

    f2 = tk.Frame(n())
    # this button destroys the 1st screen radiobutton
    b2 = tk.Button(f2, text='Button 2', command=lambda: x1.destroy())
    b3 = tk.Button(f2, text='Beep 2', command=lambda: tk.Tk.bell(a))
    b2.pack(fill=tk.BOTH, expand=1)
    b3.pack(fill=tk.BOTH, expand=1)

    f3 = tk.Frame(n())

    # keeps the reference to the radiobutton (optional)
    x1 = n.add_screen(f1, "Screen 1")
    n.add_screen(f2, "Screen 2")
    n.add_screen(f3, "dummy")
    a.mainloop()

def AndroidEnum(cls):
    enumMembers = filter(lambda x: x[0].isupper(), cls.__dict__.items())
    glb = copy.copy(globals())
    glb[cls.__name__] = cls
    glb['enumMembers'] = enumMembers
    glb['cls'] = cls
    exec('map(lambda x: setattr(cls, x[0], cls(*x[1])), enumMembers)', glb)
    enumNames = zip(*enumMembers)[0]
    map(lambda x: setattr(getattr(cls, x), '_name_', x), enumNames)
    cls.__str__ = lambda self: '<%s member of enum %s at %s>' % (self._name_, self.__class__.__name__, hex(id(self)))
    cls.__repr__ = lambda self: '<member %s of enum %s at %s>' % (self._name_, self.__class__.__name__, hex(id(self)))
    return cls


@AndroidEnum
class Category(object):
    """
    Enum for locale categories. These locale categories are used to get/set
    the default locale for the specific functionality represented by the
    category.
    """
    """
    public static final Locale.Category DISPLAY
    Category used to represent the default locale for displaying user interfaces.
    """
    DISPLAY = (1,)

    """
    public static final Locale.Category FORMAT
    Category used to represent the default locale for formatting dates, 
    numbers, and/or currencies.
    """
    FORMAT = (2,)

    def __init__(self, value):
        super(Category, self).__init__()
        self._value = value

    @classmethod
    def valueOf(self, name):
        """
        :param name: String
        :return: Locale.Category.
        """
        return getattr(self, name.upper(), None)

    @classmethod
    def values(self):
        """
        :return: Category[].
        """
        names = sorted(filter(lambda x: x.isupper(), vars(self)))
        return map(self.valueOf, names)


# Category = AndroidEnum(Category)

@AndroidEnum
class FilteringMode(object):
    """
    public static final Locale.FilteringMode AUTOSELECT_FILTERING
    Specifies automatic filtering mode based on the given Language Priority
    List consisting of language ranges. If all of the ranges are basic,
    basic filtering is selected. Otherwise, extended filtering is selected.
    """
    AUTOSELECT_FILTERING = (1,)

    """
    public static final Locale.FilteringMode EXTENDED_FILTERING
    Specifies extended filtering.
    """
    EXTENDED_FILTERING = (2,)

    """
    public static final Locale.FilteringMode IGNORE_EXTENDED_RANGES
    Specifies basic filtering: Note that any extended language ranges included 
    in the given Language Priority List are ignored.
    """
    IGNORE_EXTENDED_RANGES = (3,)

    """
    public static final Locale.FilteringMode MAP_EXTENDED_RANGES
    Specifies basic filtering: If any extended language ranges are included 
    in the given Language Priority List, they are mapped to the basic 
    language range. Specifically, a language range starting with a 
    subtag "*" is treated as a language range "*". For example, "*-US" is 
    treated as "*". If "*" is not the first subtag, "*" and extra "-" are 
    removed. For example, "ja-*-JP" is mapped to "ja-JP".
    """
    MAP_EXTENDED_RANGES = (4,)

    """
    public static final Locale.FilteringMode REJECT_EXTENDED_RANGES
    Specifies basic filtering: If any extended language ranges are included 
    in the given Language Priority List, the list is rejected and the 
    filtering method throws IllegalArgumentException.
    """
    REJECT_EXTENDED_RANGES = (5,)

    def __init__(self, value):
        super(self.__class__, self).__init__()
        self._value = value

    @classmethod
    def valueOf(self, name):
        """
        :param name: String
        :return: Locale.FilteringMode.
        """
        return getattr(self, name.upper(), None)

    @classmethod
    def values(self):
        """
        :return: FilteringMode[].
        """
        names = sorted(filter(lambda x: x.isupper(), vars(self)))
        return map(self.valueOf, names)


# FilteringMode = AndroidEnum(FilteringMode)

if __name__ == '__main__':
    # base = ContextImpl()
    # a = ContextWrapper(base)


    # setGUI()
    pass