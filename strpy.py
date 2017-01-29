from sys import maxunicode
import re

class __STRPY(object):
    """
    An object-to-string converter that respects python types. Also escapes backslashes or quotes so
    there are no "strings 'within' \\"the\\" string".
    """

    def __init__(self, *args, **kwargs):
        self.replace_map = {
            '"': "{/dq/}", # double-quote
            "'": "{/sq/}", # single-quote
            '\\': "{/bs/}", # backslash
        }
        self.unicode_map = dict([(unichr(i), '{/%s/}' % i) for i in xrange(127, maxunicode + 1)])
        self.unicode_key_regex = r"\{/[0-9]{3,5}/\}"
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
        for k, v in self.replace_map.iteritems():
            ss = ss.replace(v, k)
        return str(ss)

    def __unicodeit(self, ss):
        ss = unicode(self.__stringit(ss))
        # all of the unicode chars in the `unicode_map` fit this regex. performance boost.
        found = re.findall(self.unicode_key_regex, ss)
        if found:
            for k in found:
                if k in rev_unicode_map.keys():
                    ss = ss.replace(k, self.rev_unicode_map[k])
        return ss

    def __set_type(self, ss, stype):
        return self.type_map[stype](ss)

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
            if any(map(lambda x: x in obj, self.replace_map.values() + self.unicode_map.values())):
                raise self.StrpyError('The str "{}" has tag syntax reserved for STRPY.'.format(obj))
            try:
                obj.encode('ascii')
            except UnicodeEncodeError:
                for k, v in self.unicode_map.iteritems():
                    obj = obj.replace(k, v)
            ttype = self.__typify(obj)
            for k, v in self.replace_map.iteritems():
                obj = obj.replace(k, v)
            full_str += "{%s}%s{/%s}" % (ttype, obj, ttype)
        else:
            ttype = self.__typify(obj)
            raise self.StrpyError('STRPY does not support {}.'.format(ttype))
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
        regex = re.compile(r'{([a-zA-Z0-9_]*)}(.*?)(?={/\1})', re.DOTALL)
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
            keyhead = None
            for x in self.iterables.iterkeys():
                if key.startswith(x):
                    keyhead = x
            foundlist = []
            for lkey, lcontent in re.findall(regex, content):
                if lkey in self.items.iterkeys():
                    foundlist.append(self.__set_type(lcontent, lkey))
                else:
                    foundlist.append(self.loads('{%s}%s{/%s}' % (lkey, lcontent, lkey)))
            result = self.__set_type(foundlist, keyhead)
        return result

strpy = __STRPY()
