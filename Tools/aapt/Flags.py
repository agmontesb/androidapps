# -*- coding: utf-8 -*-
import itertools
import collections
import operator

class Flags(object):
    Flag = collections.namedtuple('Flag', 'name description action dest required numArgs parsed')
    Flag.__new__.func_defaults = ('', '', None, False, 0, False)

    def __init__(self):
        super(Flags, self).__init__()
        self.mFlags = []
        self.mArgs = []
        self.mOptions = {}

    def requiredFlag(self, name, description, varName=None):
        varName = varName or name.lstrip('-')
        func = lambda x, y=varName: operator.setitem(self.mOptions, varName, x)
        flag = Flags.Flag(name, description, func, varName, True, 1, False)
        self.mFlags.append(flag)
        return self

    def requiredFlagList(self, name, description, varName=None):
        varName = varName or name.lstrip('-')
        func = lambda x, y=varName: operator.setitem(self.mOptions, varName, x)
        flag = Flags.Flag(name, description, func, varName, True, 1, False)
        self.mFlags.append(flag)
        return self

    def optionalFlag(self, name, description, varName=None):
        varName = varName or name.lstrip('-')
        func = lambda x, y=varName: operator.setitem(self.mOptions, varName, x)
        flag = Flags.Flag(name, description, func, varName, False, 1, False)
        self.mFlags.append(flag)
        return self

    def optionalFlagList(self, name, description, varName=None):
        varName = varName or name.lstrip('-')
        func = lambda x, y=varName: operator.setitem(self.mOptions, varName, x)
        flag = Flags.Flag(name, description, func, varName, False, 1, False)
        self.mFlags.append(flag)
        return self

    def optionalSwitch(self, name, description, varName=None):
        varName = varName or name.lstrip('-')
        func = lambda x=True, y=varName: operator.setitem(self.mOptions, varName, x)
        flag = Flags.Flag(name, description, func, varName, False, 0, False)
        self.mFlags.append(flag)
        return self

    def usage(self, command, out=''):
        out += command + " [options]"
        out += ' arg '.join([flag.name for flag in self.mFlags])
        out += " files...\n\nOptions:\n"
        out += '\n'.join(
            [
                ' ' + flag.name + bool(flag.numArgs)*' arg' + ' ' + flag.description
                for flag in self.mFlags
            ])
        out += '\n ' + "-h Displays this help menu\n"
        return out

    def parse(self, command, args, diag):
        self.mArgs = []
        self.mOptions = {}
        i = 0
        while i < len(args):
            arg = args[i]
            if arg[0] != '-':
                self.mArgs.append(arg)
                i += 1
                continue
            if arg in ('-h', '--help'):
                self.usage(command)
                return False
            match = False
            for k, flag in enumerate(self.mFlags):
                if arg != flag.name: continue
                if flag.numArgs:
                    try:
                        value = args[i + 1: i + 1 + flag.numArgs]
                        flag.action(value) if flag.numArgs > 1 else flag.action(*value)
                        i += flag.numArgs
                    except:
                        outError = flag.name + " missing argument.\n\n"
                        self.usage(command, outError)
                else:
                    flag.action()
                self.mFlags[k] = flag._replace(parsed=True)
                match = True
                break
            if not match:
                outError = "unknown option '" + arg + "'.\n\n"
                self.usage(command, outError)
                return False
            i += 1
        it = itertools.dropwhile(
            lambda x: not x.required or x.parsed,
            self.mFlags
        )
        try:
            flag = it.next()
            diag.error = "missing required flag " + flag.name + ": " + flag.description + "\n\n"
            return False
        except:
            return True

    def getArgs(self):
        return self.mArgs

    def __getattr__(self, item):
        if item in self.mOptions:
            return self.mOptions[item]
        optionals = (x for x in self.mFlags if not x.required and x.dest == item)
        try:
            optionals.next()
            return None
        except:
            raise AttributeError