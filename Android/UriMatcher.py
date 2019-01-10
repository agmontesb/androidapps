# -*- coding: utf-8 -*-
import re
import collections


class UriMatcher(object):
    NO_MATCH = 0xffffffff

    def __init__(self, code):
        self._uri_tree = collections.defaultdict(list)
        self._uri_tree[''] = [('/', code)]
        pass

    def addURI(self, authority, path, code):
        path = self._scapeStr(path)
        pattern = '^' + path.replace('#', '[0-9]+').replace('*', '.+?') + '$'
        cpath = re.compile(pattern)
        self._uri_tree[authority].append((cpath, code))

    def match(self, uri):
        authority = uri.getAuthority()
        path = uri.getPath().lstrip('/')
        patterns = self._uri_tree[authority]
        for pattern, code in patterns:
            if pattern.match(path):
                return code
        else:
            return self._uri_tree[''][1]

    def _scapeStr(self, strToScape):
        special = '|([])?+^$,!<>='
        to_scape  = set(strToScape) & set(special)
        while to_scape:
            ch = to_scape.pop()
            strToScape = strToScape.replace(ch, r'\%s' % ch)
        return strToScape
