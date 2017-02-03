# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sys import maxunicode
import re

__version__ = '0.1.1'

__author__ = 'Chris Babiak <chrisb@biak.co>'

class __STRPY(object):
    """
    An object-to-string converter that respects the following python types:
    dict, list, set, tuple, frozenset, str, unicode, int, float, long, bool, complex
    Also escapes backslashes or quotes so there are no "strings 'within' \\"the\\" string".
    """

    def __init__(self, *args, **kwargs):
        self.str_replace_map = dict([(o, "{/%s/}" % ord(o)) for o in ('"', "'", '\\')])
        self.rev_str_replace_map = dict([(v, k) for k, v in self.str_replace_map.iteritems()])
        self.str_key_regex = re.compile(r"'|\\|\"")
        self.min_char = 127
        self.max_char = maxunicode
        self.unicode_key_regex = r"\{/[0-9]{3,5}/\}" # must be numbers
        self.reserved_regex = re.compile(r"\{/[0-9]{2,5}/\}")
        self.unicode_map = dict(
            [(unichr(i), '{/%s/}' % i) for i in xrange(self.min_char, self.max_char + 1)])
        self.rev_unicode_map = dict([(v, k) for k, v in self.unicode_map.iteritems()])
        self.items = {
            'in': int,
            'st': self.__stringit,
            'un': self.__unicodeit,
            'fl': float,
            'lo': long,
            'co': complex,
            'bo': self.__boolit,
        }
        self.iterables = {
            'li': list,
            'tu': tuple,
            'se': set,
            'fr': frozenset,
        }
        self.type_map = self.items.copy()
        self.type_map.update(self.iterables)

    class StrpyError(Exception):
        pass

    def __typify(self, thing):
        return str(type(thing))[7:9] # returns key to match self.type_map dict

    def __boolit(self, ss):
        if ss.lower() == 'true':
            return True
        return False

    def __stringit(self, ss):
        if re.search(self.reserved_regex, ss):
            ss = self.__replace_repeat(ss, self.rev_str_replace_map)
        return str(ss)

    def __unicodeit(self, ss):
        ss = unicode(self.__stringit(ss))
        # all of the unicode chars in the `unicode_map` fit this regex. performance boost.
        found = re.findall(self.unicode_key_regex, ss)
        if found:
            found = [k for k in found if k in self.rev_unicode_map.keys()]
            for k in found:
                ss = ss.replace(k, self.rev_unicode_map[k])
        return ss

    def __set_type(self, ss, stype):
        return self.type_map[stype](ss)

    @staticmethod
    def __replace_repeat(text, dicc):
        for k, v in dicc.iteritems():
            text = text.replace(k, v)
        return text

    def __dumps(self, obj, nn=0):
        """
        Like json.dumps(). Convert an object to a flat string.

        Args:
            obj: a python built-in type.
            nn: number for recursion.

        Returns:
            a curly-braced ascii string representation of the obj.
        """
        full_str = ''
        if isinstance(obj, dict):
            full_str += "{di%s}" % nn
            full_str += self.__dumps(obj.items(), nn + 1)
            full_str += "{/di%s}" % nn
        elif isinstance(obj, (list, set, tuple, frozenset)):
            ttype = self.__typify(obj)
            full_str += "{%s%s}" % (ttype, nn)
            for n, item in enumerate(obj, 1):
                full_str += self.__dumps(item, nn + n)
            full_str += "{/%s%s}" % (ttype, nn)
        elif isinstance(obj, (int, float, long, bool, complex)):
            ttype = self.__typify(obj)
            full_str += "{%s}%s{/%s}" % (ttype, obj, ttype)
        elif isinstance(obj, (str, unicode)):
            if re.search(self.reserved_regex, obj):
                raise self.StrpyError('The str "{}" has tag syntax reserved for STRPY.'.format(obj))
            try:
                obj.encode('ascii')
            except UnicodeEncodeError:
                obj = self.__replace_repeat(obj, self.unicode_map)
            ttype = self.__typify(obj)
            if re.search(self.str_key_regex, obj):
                obj = self.__replace_repeat(obj, self.str_replace_map)
            full_str += "{%s}%s{/%s}" % (ttype, obj, ttype)
        else:
            ttype = self.__typify(obj)
            raise self.StrpyError('STRPY does not support {}.'.format(str(type(obj))))
        return str(full_str)

    def dumps(self, obj):
        """
        Like json.dumps(). Convert an object to a flat string.

        Args:
            obj (dict, list, set, tuple, frozenset, str, unicode, int, float, long, bool, complex):
                a python built-in type.

        Returns:
            a curly-braced ascii string representation of the obj.
        """
        return self.__dumps(obj)

    def loads(self, obj):
        """
        Like json.loads(). Convert a strpy string to its python self.

        Args:
            obj (str): a strpy-like string.

        Returns:
            a python-typed version of the strpy-string.
        """
        regex = re.compile(r'{([a-zA-Z0-9_]+)}(.*?)(?={/\1})', re.DOTALL)
        match = re.search(regex, obj)
        if not match:
            raise self.StrpyError('Could not parse object "{}". Check syntax.'.format(obj))
        key = match.group(1)
        content = match.group(2)
        if key in self.items.iterkeys():
            result = self.__set_type(content, key)
        elif key.startswith('di'):
            result = dict(self.loads(content))
        else:
            keyhead = key[0:2]
            if keyhead not in self.iterables.keys():
                raise self.StrpyError('Could not find a type key "{}".'.format(keyhead))
            foundlist = []
            for lkey, lcontent in re.findall(regex, content):
                if lkey in self.items.iterkeys():
                    foundlist.append(self.__set_type(lcontent, lkey))
                else:
                    foundlist.append(self.loads('{%s}%s{/%s}' % (lkey, lcontent, lkey)))
            result = self.__set_type(foundlist, keyhead)
        return result

dumps = __STRPY().dumps
loads = __STRPY().loads