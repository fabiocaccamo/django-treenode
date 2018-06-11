# -*- coding: utf-8 -*-

from collections import defaultdict

from .utils import split_pks


__list__ = defaultdict(list)
__dict__ = defaultdict(dict)


def clear_cache(cls):
    del __list__[cls][:]
    __dict__[cls].clear()


def query_cache(cls, pk=None, pks=None):
    if not __list__[cls] or not __dict__[cls]:
        update_cache(cls)
    if pk != None:
        return __dict__[cls].get(str(pk))
    elif pks != None:
        return [__dict__[cls].get(str(pk)) for pk in split_pks(pks)]
    else:
        return list(__list__[cls])


def update_cache(cls):
    __list__[cls] = list(cls.objects.all())
    __dict__[cls] = {str(obj.pk):obj for obj in __list__[cls]}
