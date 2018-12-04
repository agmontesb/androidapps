# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import re
from basicFunc import openUrl
import CustomRegEx as crgx
import itertools
from IPython import start_ipython


def start_notebook(working_dir=None):
    '''
    Inicia el jupyter notebook in working_directory
    :param working_dir: Directorio de arranque para el jupyter
                        notebook
    :return: None
    '''
    working_dir = working_dir or os.path.dirname(__file__)
    os.chdir(working_dir)
    start_ipython(['notebook', '--no-browser',])


class CreateAndroidClassStub(object):

    def __init__(self, classUrl):
        self._log = sys.stdout
        self.classUrl = classUrl
        self._content = None
        self._sections = None
        self._classSignature = ''
        self._classname = ''

    @classmethod
    def formatDocString(self, fdoc, indent, right):
        left = len(indent)
        length = right - left
        answ = []
        fdoc = '"""\n' + fdoc + '\n"""'
        fdoc = fdoc.replace('&lt;', '<').replace('&gt;', '>')
        for equis in fdoc.split('\n'):
            pos = 0
            while len(equis) > length and pos >= 0:
                pos = equis[:length].rfind(' ')
                toansw, equis = equis[:pos + 1], equis[pos + 1:]
                answ.append(toansw)
            else:
                answ.append(equis)
        return indent + indent.join(answ)

    def getUrlContent(self):
        if self._content is None:
            url, content = openUrl(self.classUrl)
            self._content = content
        return self._content

    def _getSectionDelimiters(self, section):
        sections = self._sections
        if self._sections is None:
            content = self.getUrlContent()
            pattern = r'(?#<h[12] class="api.+?">)'
            sections = crgx.findall(pattern, content)
            sections = filter(lambda x: 'Protected' not in x, sections)
            sections.append(u'<!-- end jd-content -->')
            self._sections = sections
        it = itertools.dropwhile(lambda x: section not in x, sections)
        return (it.next(), it.next())

    def _getSectionText(self, section):
        try:
            prefix, suffix = self._getSectionDelimiters(section)
        except:
            return ''
        pattern = prefix + '(.+?)' + suffix
        texto = re.search(pattern, self.getUrlContent(), re.DOTALL)
        return texto.group()

    def _getStringContent(self, pattern, texto):
        pini = 0
        lista = []
        while True:
            answ = crgx.search(pattern, texto[pini:])
            if not answ: break
            fdef = ''.join(answ.groups()).strip('\n ')
            lista.append(fdef)
            pini += answ.end()
        return lista

    def parseAndroidConstants(self):
        texto = self._getSectionText('Constants')
        pattern = r'(?#<div data-version-added .*>)'
        lista = self._getStringContent(pattern, texto)
        indent = '\n'
        for raw in lista:
            raw = map(lambda x: x.strip(' '), raw.split('\n'))
            key, value = raw[0], raw[-1][1:-1]
            cdoc = '\n'.join(raw[3:-3])
            cdoc = cdoc.replace(key, key + ':\n')
            cdoc = cdoc.replace('Constant Value:', '').strip('\n')
            cdoc = self.formatDocString(cdoc, indent, 80)
            print(cdoc, file=self._log)
            print('%s = %s' % (key, value), file=self._log)

    def parseClassDefinition(self):
        if not self._classSignature:
            classDoc = ''
            classDoc += '# -*- coding: utf-8 -*-\n"""%s"""\n'
            classDoc += 'from Android import overload\n\n'
            self._classSignature = classDoc
            print(classDoc % self.classUrl, file=self._log)
        else:
            texto = self._getSectionText('')
            pattern = r'(?#<code class="api-signature" *=label>)'
            m = crgx.search(pattern, texto)
            classSignature = m.group('label')
            classSignature = classSignature.replace('\n', '').split(' ')
            classSignature = ' '.join(filter(lambda x: x, classSignature))
            self._classSignature = classSignature
            pos = m.end('label')
            m = crgx.search(r'(?#<p>)', texto[pos:])
            classDoc = m.group()
            classDoc = ' '.join(re.findall('>(.*?)<', classDoc, re.DOTALL))
            classDoc = classDoc.replace('\n', '')
            classDoc = re.sub(r' +', ' ', classDoc)
            classType, className = classSignature.split(' class ')
            indent = '\n    '
            classDoc = self.formatDocString(classDoc, indent, 80)
            if 'abstract' in classType:
                template = '\nclass I{0}(object):{1}{2}__metaclass__ = abc.ABCMeta'
            else:
                template = '\nclass {0}(object):{1}'
            self._classname = className
            print(template.format(className, classDoc, indent), file=self._log)

    def parseAndroidPublicConstructors(self):
        texto = self._getSectionText('Public constructors')
        pattern = r'(?#<div data-version-added .*>)'
        lista = self._getStringContent(pattern, texto)
        indent = '\n        '
        pattern = r'\(([^)]+)\)'
        for k, raw in enumerate(lista):
            try:
                vars = re.search(pattern, raw).group(1).rstrip(',')
                vars = map(lambda x: x.rsplit(' ', 1), vars.split(','))
                varstype, varsname = zip(*vars)
            except:
                fdef = '{0}@overload{0}def __init__(self)'.format('\n    ', k)
                fdoc = ''
                template = '''{0}:{2}pass'''
            else:
                signature = "'%s'" % "', '".join(varstype)
                vars = ', '.join(varsname)
                fdef = '{0}@__init__.adddef({3}){0}def {1}(self, {2})'.format(
                    '\n    ', self._classname, vars, signature)

                params = ''
                for var in zip(varsname, varstype):
                    params += '\n:param {0}: {1}.'.format(*var)
                fdoc = params[1:]
                fdoc = self.formatDocString(fdoc, indent, 80)
                template = '''{0}:{1}{2}pass'''
            ofunc = template.format(fdef, fdoc, indent)
            print(ofunc, file=self._log)

    def parseAndroidFields(self):
        texto = self._getSectionText('Fields')
        # content = self.getUrlContent()
        # pattern = r'<!-- Fields -->(.+?)<!-- Public ctors -->'
        # texto = re.search(pattern, content, re.DOTALL)
        # texto = texto.group()
        pattern = r'(?#<div data-version-added .*>)'
        lista = self._getStringContent(pattern, texto)
        indent = '\n    '
        for raw in lista:
            raw = map(lambda x: x.strip(' '), raw.split('\n'))
            key = raw[0]
            cdoc = '\n'.join(raw[3:])
            prefix, suffix = cdoc.split(key, 1)
            cdoc = '%s%s:\n%s' % (prefix, key, suffix)
            cdoc = self.formatDocString(cdoc, indent, 80)
            print(cdoc, file=self._log)
            print(indent[1:] + '%s = None' % key, file=self._log)

    def _fdocPartition(self, suffix):
        seek = ['fdoc', 'Parameters', 'Returns(?=[A-Za-z])', 'Throws(?=[A-Z])', 'See also:(?=[a-zA-Z])']
        frst = 0
        scnd = 1
        while scnd < len(seek):
            try:
                seek[frst], suffix = re.split(seek[scnd], suffix, 1)
                frst = scnd
            except:
                seek[scnd] = ''
            scnd += 1
        if frst < len(seek):
            seek[frst] = suffix
        return seek

    def parseAndroidMethods(self):
        def trf(m):
            vars = m.group(1).strip(',')
            vars = map(lambda x: x.rsplit(' ', 1)[-1], vars.split(','))
            vars = '(%s)' % ', '.join(vars)
            return vars

        texto = self._getSectionText('Public methods')
        pattern = r'(?#<div data-version-added .*>)'
        lista = self._getStringContent(pattern, texto)

        indent = '\n        '
        pkey = ''
        noverload = 0
        for k, raw in enumerate(lista):
            #         print raw
            raw = map(lambda x: x.strip(' '), raw.split('\n'))
            key = raw[0]
            noverload = (noverload + 1) if pkey == key else 0
            pkey = key
            fdoc = '\n'.join(raw[2:])
            fdef, fdoc = fdoc.split(')', 1)
            fdef += ')'
            pattern = r'\(([^)]+)\)'
            try:
                vars = re.search(pattern, fdef).group(1).rstrip(',')
                vars = map(lambda x: x.rsplit(' ', 1), vars.split(','))
                varstype, vars = zip(*vars)
            except:
                vars = []
            fdef = fdef.replace('(', '(a self,')
            fprefix, fdef = fdef.split(key, 1)
            fdef = key + fdef.strip()
            fdef = re.sub(pattern, trf, fdef)
            ret_type = fprefix.strip().rsplit(' ', 1)[-1]
            fdef = '''{0}def {1}'''.format('\n    ', fdef)
            if noverload:
                signature = "'%s'" % "', '".join(map(lambda x: x.replace('\n', ''), varstype))
                prefix = '{0}@{1}.adddef({2})'.format('\n    ', key, signature)
                fdef = prefix + fdef
            if noverload == 1:
                prefix = '{0}{1} = overload({1}){0}'.format('\n    ', key)
                fdef = prefix + fdef
            if 'static' in fprefix:
                fdef = '\n    @classmethod' + fdef
            if 'asbstract' in fprefix:
                fdef = '\n    # @abc.abstractmethod' + fdef

            if fdoc:
                suffix = fdoc
                parts = self._fdocPartition(suffix)
                if parts[1]:
                    mparams = ''
                    params = parts[1]
                    for var in vars:
                        pattern = var + '(?=[A-Za-z])'
                        prefix, params = re.split(pattern, params, 1)
                        mparams += '\n' + prefix
                        params = ':param %s: ' % var + params
                    params = mparams.strip('\n') + '\n' + params
                    parts[1] = params
                if parts[2]:
                    parts[2] = ':return: %s. ' % ret_type + parts[2].split(ret_type, 1)[1]
                if parts[3]:
                    parts[3] = ':raises: ' + parts[3]
                if parts[4]:
                    parts[4] = 'See also: ' + parts[4]

                parts = map(lambda x: re.sub('\n(?!:)', ' ', x).strip(' \n'), parts)
                fdoc = '\n'.join(filter(lambda x: x, parts))
                fdoc = self.formatDocString(fdoc, indent, 80)
                template = '''{0}:{1}{2}pass'''
            else:
                template = '''{0}:{2}pass'''
                fdoc = ''

            ofunc = template.format(fdef, fdoc, indent)
            print(ofunc, file=self._log)

    def __call__(self, filename=None):
        if filename:
            self._log = open(filename, 'w')
        self.parseClassDefinition()
        self.parseAndroidConstants()
        self.parseClassDefinition()
        self.parseAndroidFields()
        self.parseAndroidPublicConstructors()
        self.parseAndroidMethods()
        if self._log != sys.stdout:
            self._log.close()
            self._log = sys.stdout