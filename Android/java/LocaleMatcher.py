# -*- coding: utf-8 -*-
import itertools
import re
from operator import methodcaller as mcall

import LocaleEquivalentMaps
from Android import Object
from Android.java.LanguageTag import LanguageTag
from Android.java.Locale import Locale

MIN_WEIGHT = MIN_WEIGHT
MAX_WEIGHT = MAX_WEIGHT

class LocaleMatcher(Object):
    _isExtendedRange = re.compile(r'(?:[a-z]{1,8}|\*)(?:-(?:[0-9a-z]{1,8}|\*))*$').match

    @classmethod
    def filter(cls, priorityList, locales, mode):
        if not priorityList or not locales:
            return []
        tags = map(mcall('toLanguageTag'), locales)
        filteredTags = cls.filterTags(priorityList, tags, mode)
        filteredLocales = map(Locale.forLanguageTag, filteredTags)
        return filteredLocales

    @classmethod
    def filterTags(cls, priorityList, tags, mode):
        FilteringMode = Locale.FilteringMode
        lista = []
        if mode == FilteringMode.EXTENDED_FILTERING:
            return cls.filteredExtended(priorityList, tags)
        for lr in sorted(priorityList, key=mcall('getWeight')):
            range = lr.getRange()
            if cls._isExtendedRange(range):
                if mode == FilteringMode.AUTOSELECT_FILTERING:
                    return cls.filterExtended(priorityList, tags)
                elif mode == FilteringMode.MAP_EXTENDED_RANGES:
                    if range[0] == '*':
                        range = '*'
                    else:
                        range = range.replace('-*', '')
                    lista.append(Locale.LanguageRange(range, lr.getWeight()))
                elif mode == FilteringMode.REJECT_EXTENDED_RANGES:
                    raise Exception('IllegalArgumentException: An extended range '
                                    '"%s" found in REJECT_EXTENDED_RANGES mode.' % range)
            else:
                lista.append(lr)
        return cls.filterBasic(lista, tags)

    @classmethod
    def filterBasic(cls, priorityList, tags):
        lista = []
        priorityList = map(mcall('getRange'), priorityList)
        if '*' in priorityList: return tags
        for range in priorityList:
            range += LanguageTag.SEP
            for tag in tags:
                tag = tag.lower()+ LanguageTag.SEP
                if tag.startswith(range) and tag[:-1] not in lista:
                    lista.append(tag[:-1])
        return lista

    @classmethod
    def filterExtended(cls, priorityList, tags):
        lista = []
        priorityList = map(mcall('getRange'), sorted(priorityList, key=mcall('getWeight')))
        if '*' in priorityList: return tags
        for range in priorityList:
            rangeSubtags = range.split(LanguageTag.SEP)
            for tag in tags:
                tagSubtags = tag.split(LanguageTag.SEP)
                if rangeSubtags[0] != '*' and tagSubtags[0] != rangeSubtags[0]:
                    continue
                rangeIndx = 1
                tagIndx = 1
                while rangeIndx < len(rangeSubtags) and tagIndx < len(tagSubtags):
                    if rangeSubtags[rangeIndx] == '*':
                        rangeIndx += 1
                    elif rangeSubtags[rangeIndx] == tagSubtags[tagIndx]:
                        rangeIndx += 1
                        tagIndx += 1
                    elif len(tagSubtags[tagIndx]) == 1 and tagSubtags[tagIndx] != "*":
                        break
                    else:
                        tagIndx += 1
                if len(rangeSubtags) == rangeIndx and tag not in lista:
                    lista.append(tag)
        return lista

    @classmethod
    def lookup(cls, priorityList, locales):
        if not priorityList or not locales:
            return None
        tags = map(mcall('toLanguageTag'), locales)
        lookedUpTag = cls.lookupTag(priorityList, tags)
        return Locale.forLanguageTag(lookedUpTag) if lookedUpTag else None

    @classmethod
    def lookupTag(cls, priorityList, tags):
        if not priorityList or not tags:
            return None
        priorityList = map(mcall('getRange'), sorted(priorityList, key=mcall('getWeight')))
        for range in priorityList:
            if range == '*': continue
            rangeForRegex = range.replace('*', r'[0-9a-z]{1,8}')
            while rangeForRegex:
                isMatch = re.compile(rangeForRegex).match
                it = itertools.dropwhile(lambda x: not(isMatch(x.lower())), tags)
                try:
                    return it.next()
                except:
                    pass
                if LanguageTag.SEP not in rangeForRegex:
                    rangeForRegex = ''
                    break
                rangeForRegex = rangeForRegex.rsplit(LanguageTag.SEP, 1)[0]
                if rangeForRegex[-2] == LanguageTag.SEP:
                    rangeForRegex = rangeForRegex[:-3]
        return None

    @classmethod
    def parse(cls, ranges):
        def addLanguageRange(r, w):
            if r and r not in tempList:
                lr = Locale.LanguageRange(r, w)
                lista.append(lr)
                tempList.append(r)

        ranges = ranges.replace(' ', '')
        if ranges.startsWith("accept-language:"):
            ranges = ranges.split('accept-language:')[-1]
        langRanges = ranges.split(',')
        lista = []
        tempList = []
        for range in langRanges:
            try:
                r, w = range.split(';q=')
            except:
                r, w = range, MAX_WEIGHT
            else:
                try:
                    w = float(w)
                    if w < MIN_WEIGHT or w >  MAX_WEIGHT:
                        message = 'IllegalArgumentException: "weight=%s ' \
                                  'for language range %s. It must be between %s and %s."'
                        raise Exception(message % (w, r, MIN_WEIGHT, MAX_WEIGHT))
                except:
                    message = 'IllegalArgumentException: "weight=%s for language range %s"'
                    raise Exception(message % (w, r))
            addLanguageRange(r, w)
            equivalent = cls.getEquivalentForRegionAndVariant(r)
            addLanguageRange(equivalent, w)
            equivalents = cls.getEquivalentsForLanguage(r)
            if not equivalents: continue
            map(lambda x: (addLanguageRange(x, w),
                           addLanguageRange(cls.getEquivalentForRegionAndVariant(x), r)
                           ), equivalents
                )

        return sorted(lista, key=lambda x: x.getWeight())

    @classmethod
    def getEquivalentsForLanguage(cls, range):
        r = range
        while r:
            if LocaleEquivalentMaps.singleEquivMap.has_key(r):
                equiv = LocaleEquivalentMaps.singleEquivMap.get(r)
                return range.replace(r, equiv, 1)
            elif LocaleEquivalentMaps.multiEquivsMap.has_key(r):
                equivs = LocaleEquivalentMaps.multiEquivsMap.get(r)
                return map(lambda x: range.replace(r, x, 1), equivs)
            try:
                r, suffix = r.rsplit(LanguageTag.SEP)
            except:
                break
        return None

    @classmethod
    def getEquivalentForRegionAndVariant(cls, range):
        try:
            extensionKeyIndex = re.search(r'-[0-9a-zA-Z]-').start()
        except:
            extensionKeyIndex = None

        for subtag in LocaleEquivalentMaps.regionVariantEquivMap:
            index = range.find(subtag)
            if index == -1 or (extensionKeyIndex and index > extensionKeyIndex):
                continue
            dmy = index + len(subtag)
            if len(range) == dmy or range[dmy] == LanguageTag.SEP:
                return range.replace(subtag, LocaleEquivalentMaps.regionVariantEquivMap.get(subtag))
        return None

    @classmethod
    def mapEquivalents(cls, priorityList, map):
        if not priorityList: return None
        if not map: return priorityList
        keyMap = {key.lower():key for key in map}
        lista = []
        for lr in priorityList:
            range = lr.getRange()
            r = range
            hasEquivalent = False
            while r:
                if keyMap.has_key(r):
                    hasEquivalent = True
                    equivalents = map[keyMap[r]]
                    if equivalents:
                        dmy = len(r)
                        for equivalent in equivalents:
                            langRange = Locale.LanguageRange(
                                equivalent.lower() + range[dmy:],
                                lr.getWeight()
                            )
                            lista.append(langRange)
                    break
                try:
                    r = r.rsplit(LanguageTag.SEP, 1)[0]
                except:
                    break
            if not hasEquivalent:
                lista.append(lr)
        return lista











