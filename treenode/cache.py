from collections import defaultdict

from django.conf import settings
from django.core.cache import cache, caches

from .utils import split_pks


def _get_cache():
    return caches["treenode"] if "treenode" in settings.CACHES else cache


def _get_cached_collection(key, dict_cls):
    c = _get_cache()
    value = c.get(key, None)
    if value is None:
        value = defaultdict(dict_cls)
        c.set(key, value)
    return value


def _get_cached_collections():
    ls = _get_cached_collection("treenode_list", list)
    d = _get_cached_collection("treenode_dict", dict)
    return (ls, d)


def _set_cached_collections(ls, d):
    c = _get_cache()
    c.set("treenode_list", ls)
    c.set("treenode_dict", d)


def clear_cache(cls):
    ls, d = _get_cached_collections()
    del ls[cls][:]
    d[cls].clear()
    _set_cached_collections(ls, d)


def query_cache(cls, pk=None, pks=None):
    ls, d = _get_cached_collections()
    if not ls[cls] or not d[cls]:
        update_cache(cls)
        ls, d = _get_cached_collections()
    if pk is not None:
        return d[cls].get(str(pk))
    elif pks is not None:
        return [d[cls].get(str(pk)) for pk in split_pks(pks)]
    else:
        return list(ls[cls])


def update_cache(cls):
    ls, d = _get_cached_collections()
    ls[cls] = list(cls.objects.all())
    d[cls] = {str(obj.pk): obj for obj in ls[cls]}
    _set_cached_collections(ls, d)
