# -*- coding: utf-8 -*-
# Ported from:
# https://github.com/frohoff/jdk8u-dev-jdk/blob/master/src/share/classes/sun/util/locale/LanguageTag.java
#
import re

from Android import Object
from Android.java.Locale import Locale


class LanguageTag(Object):
    entries = [
        # {"tag", "preferred"},
        ("art-lojban", "jbo"),
        ("cel-gaulish", "xtg-x-cel-gaulish"), # fallback
        ("en-GB-oed", "en-GB-x-oed"), # fallback
        ("i-ami", "ami"),
        ("i-bnn", "bnn"),
        ("i-default", "en-x-i-default"), # fallback
        ("i-enochian", "und-x-i-enochian"), # fallback
        ("i-hak", "hak"),
        ("i-klingon", "tlh"),
        ("i-lux", "lb"),
        ("i-mingo", "see-x-i-mingo"), # fallback
        ("i-navajo", "nv"),
        ("i-pwn", "pwn"),
        ("i-tao", "tao"),
        ("i-tay", "tay"),
        ("i-tsu", "tsu"),
        ("no-bok", "nb"),
        ("no-nyn", "nn"),
        ("sgn-BE-FR", "sfb"),
        ("sgn-BE-NL", "vgt"),
        ("sgn-CH-DE", "sgg"),
        ("zh-guoyu", "cmn"),
        ("zh-hakka", "hak"),
        ("zh-min", "nan-x-zh-min"), # fallback
        ("zh-min-nan", "nan"),
        ("zh-xiang", "hsn"),
    ]
    GRANFATHERED = {x[0].lower(): x for x in entries}
    SEP = '-'
    PRIVATEUSE = 'x'
    UNDETERMINED = 'und'
    PRIVUSE_VARIANT_PREFIX = 'lvariant'

    isLanguage = re.compile(r'[a-zA-Z]{2,8}$').match
    isExtLang = re.compile(r'[a-zA-Z]{3}$').match
    isScript = re.compile(r'[a-zA-Z]{4}$').match
    isRegion = re.compile(r'(?:[a-zA-Z]{2}|[0-9]{3})$').match
    isVariant = re.compile(r'(?:[0-9a-zA-Z]{5,8}|(?:[0-9][0-9a-zA-Z]{3}))$').match
    isExtension = re.compile(r'[0-9a-wy-zA-WY-Z]$').match
    isExtensionSubtag = re.compile(r'[0-9a-zA-Z]{2,8}').match
    isPrivateUseSubtag = re.compile(r'[0-9a-zA-Z]{1,8}$').match

    def __init__(self):
        super(LanguageTag, self).__init__()
        self.language = None
        self.script = None
        self.region = None
        self.extlangs = None
        self.variants = None
        self.extensions = None
        self.privateuse = None

    @classmethod
    def parse(cls, languagetagStr, status=None):
        SEP = cls.SEP
        gfmap = cls.GRANFATHERED.get(languagetagStr.lower())
        if gfmap:
            languagetagStr = gfmap[1]
        lngtag = cls()
        tagSplit = lambda x: x.split(SEP, 1) if SEP in x else (x, '')

        prefix, suffix = tagSplit(languagetagStr)
        if cls.isLanguage(prefix):    # lang
            lngtag.language = prefix if prefix != cls.UNDETERMINED else ''
            languagetagStr = suffix
            k = 0
            status = ''
            while not status and languagetagStr:
                k += 1
                if k == 1:            # extlang
                    languagetagStr, dmy = cls._parseComponent(languagetagStr, cls.isExtLang, SEP, limit=3)
                    lngtag.extlangs = dmy
                elif k in (2, 3):     # script, regn
                    predicate = (cls.isScript, cls.isRegion)[k - 2]
                    attrname = ('script', 'region')[k - 2]
                    languagetagStr, dmy = cls._parseComponent(languagetagStr, predicate, SEP)
                    if dmy: setattr(lngtag, attrname, dmy[0])
                    if len(dmy) > 1: status = '%s has %s tags' % (attrname.title(), len(dmy))
                elif k == 4:            # variant
                    languagetagStr, dmy = cls._parseComponent(languagetagStr, cls.isVariant, SEP)
                    lngtag.variants = dmy
                elif k == 5:            # extensions
                    seen = set()
                    lngtag.extensions = []
                    while languagetagStr:
                        prefix, suffix = tagSplit(languagetagStr)
                        if cls.isExtension(prefix):
                            if prefix not in seen:
                                predicate = cls.isExtensionSubtag
                                languagetagStr = suffix
                                languagetagStr, dmy = cls._parseComponent(languagetagStr, predicate, SEP)
                                if dmy:
                                    lngtag.extensions.append(prefix + SEP + SEP.join(dmy))
                                else:
                                    status = 'Incomplete extension "%s"' % prefix
                                    break
                                seen.add(prefix)
                                continue
                            status = 'two extensions with "%s" single-letter' % prefix
                        break
                else:
                    break
        if not status and languagetagStr:
            prefix, suffix = tagSplit(languagetagStr)
            if prefix == cls.PRIVATEUSE:
                languagetagStr = suffix
                # k = len(patterns) - 1
                languagetagStr, dmy = cls._parseComponent(languagetagStr, cls.isPrivateUseSubtag, SEP)
                lngtag.privateuse = cls.PRIVATEUSE + SEP + SEP.join(dmy)
        if not status and languagetagStr:
            prefix = tagSplit(languagetagStr)[0]
            status = ("Invalid subtag: " + prefix) if prefix else "Empty subtag"
        status = status or 'OK'
        return lngtag, status

    @classmethod
    def parseLocale(cls, locale):
        lang = locale.getLanguage()
        scrit = locale.getScript()
        regn = locale.getCountry()
        vart = locale.getVariant()

        hassubtag = False
        privuseVar = None
        tag = cls()

        if cls.isLanguage(lang):
            try:
                ndx = ('iw', 'ji', 'in').index(lang)
                lang = ('he', 'yi', 'id')[ndx]
            except:
                pass
            tag.language = lang
        if cls.isScript(scrit):
            tag.script = cls.canonicalizeScript(scrit)
            hassubtag = True
        if cls.isRegion(regn):
            tag.region = cls.canonicalizeRegion(regn)
            hassubtag = True
        if tag.language == 'no' and tag.region == 'NO' and vart == 'NY':
            tag.language = 'nn'
            vart = ''
        if vart:
            vart, dmy = cls._parseComponent(vart, cls.isVariant, Locale.SEP)
            tag.variants = dmy
            if vart:
                vart, dmy = cls._parseComponent(vart, cls.isPrivateUseSubtag, Locale.SEP)
                privuseVar = cls.SEP.join(dmy)
        privateuse = None
        extensions = []
        if locale.extensions:
            locExtensions = locale.extensions
            for key, ext in locExtensions.items():
                if cls.isPrivateUseSubtag(key):
                    privateuse = ext
                else:
                    extensions.append(key + cls.SEP + ext)
        if extensions:
            tag.extensions = extensions
            hassubtag = True
        if privuseVar:
            if privateuse:
                privateuse = cls.PRIVUSE_VARIANT_PREFIX + cls.SEP + privuseVar
            else:
                privateuse += cls.SEP + cls.PRIVUSE_VARIANT_PREFIX + cls.SEP
                privateuse += privuseVar.replace(Locale.SEP, cls.SEP)
        if privateuse:
            tag.privateuse = privateuse
        if not tag.language and (hassubtag or privateuse is None):
            tag.language = cls.UNDETERMINED
        return tag

    @staticmethod
    def _parseComponent(languagetagStr, predicate, SEP, limit=None):
        tagSplit = lambda x: x.split(SEP, 1) if SEP in x else (x, '')
        dmy = []
        while languagetagStr:
            prefix, suffix = tagSplit(languagetagStr)
            bFlag = predicate(prefix)
            if bFlag:
                languagetagStr = suffix
                dmy.append(prefix)
            if not bFlag or (limit and len(dmy) > limit):
                break
        return languagetagStr, dmy

    def getLanguage(self):
        return self.language

    def getExtlangs(self):
        extlangs = self.extlangs or []
        return tuple(extlangs)

    def getScript(self):
        return self.script

    def getRegion(self):
        return self.region

    def getVariants(self):
        variants = self.variants or []
        return tuple(variants)

    def getExtensions(self):
        extensions = self.extensions or []
        return tuple(extensions)

    def getPrivateuse(self):
        return self.privateuse

    def canonicalizeLanguage(self, s):
        return s.lower()

    def canonicalizeExtlangs(self, s):
        return s.lower()

    def canonicalizeScript(self, s):
        return s.title()

    def canonicalizeRegion(self, s):
        return s.upper()

    def canonicalizeVariant(self, s):
        return s.lower()

    def canonicalizeExtension(self, s):
        return s.lower()

    def canonicalizePrivateuse(self, s):
        return s.lower()

    def toString(self):
        lang = self.getLanguage()
        sb = []
        if lang:
            sb.append(lang)
            sb.extend(self.getExtlangs())
            if self.getScript(): sb.append(self.getScript())
            if self.getRegion(): sb.append(self.getRegion())
            sb.extend(self.getVariants())
            sb.extend(self.getExtensions())
        if self.getPrivateuse(): sb.append(self.getPrivateuse())
        return self.SEP.join(sb)



