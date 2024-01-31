import logging
from collections import defaultdict

from django.conf import settings
from django.core.cache import cache as default_cache, caches

from treenode.exceptions import CacheError
from treenode.utils import split_pks

logger = logging.getLogger(__name__)


def _get_cache():
    return caches["treenode"] if "treenode" in settings.CACHES else default_cache


def _get_cache_name():
    return "treenode" if "treenode" in settings.CACHES else "default"


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
    objs = list(cls.objects.all())
    ls, d = _get_cached_collections()
    ls[cls] = objs
    d[cls] = {str(obj.pk): obj for obj in objs}
    _set_cached_collections(ls, d)
    # ensure cache has been updated correctly
    if len(objs):
        ls, d = _get_cached_collections()
        if not ls[cls] or not d[cls]:
            cn = _get_cache_name()
            msg = (
                f"Unable to update cache '{cn}', "
                "please check 'settings.CACHES' configuration."
            )
            logger.warning(msg)
            raise CacheError(msg)
