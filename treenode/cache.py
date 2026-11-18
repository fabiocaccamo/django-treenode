import logging

from django.conf import settings
from django.core.cache import cache as default_cache
from django.core.cache import caches

from treenode.exceptions import CacheError
from treenode.utils import split_pks

logger = logging.getLogger(__name__)


def _get_cache():
    return caches["treenode"] if "treenode" in settings.CACHES else default_cache


def _get_cache_name():
    return "treenode" if "treenode" in settings.CACHES else "default"


def _cache_key(cls, suffix):
    return f"treenode_{suffix}:{cls._meta.label_lower}"


def _get_cached_collection(cls, suffix, empty_factory):
    c = _get_cache()
    key = _cache_key(cls, suffix)
    value = c.get(key, None)
    if value is None:
        value = empty_factory()
        c.set(key, value)
    return value


def _get_cached_collections(cls):
    ls = _get_cached_collection(cls, "list", list)
    d = _get_cached_collection(cls, "dict", dict)
    return (ls, d)


def _set_cached_collections(cls, ls, d):
    c = _get_cache()
    c.set(_cache_key(cls, "list"), ls)
    c.set(_cache_key(cls, "dict"), d)


def clear_cache(cls):
    c = _get_cache()
    c.delete(_cache_key(cls, "list"))
    c.delete(_cache_key(cls, "dict"))


def query_cache(cls, pk=None, pks=None):
    ls, d = _get_cached_collections(cls)
    if not ls or not d:
        update_cache(cls)
        ls, d = _get_cached_collections(cls)
    if pk is not None:
        return d.get(str(pk))
    elif pks is not None:
        return [d.get(str(pk)) for pk in split_pks(pks)]
    else:
        return list(ls)


def update_cache(cls):
    objs = list(cls.objects.all())
    d = {str(obj.pk): obj for obj in objs}
    _set_cached_collections(cls, objs, d)
    # ensure cache has been updated correctly
    if len(objs):
        ls2, d2 = _get_cached_collections(cls)
        if not ls2 or not d2:
            cn = _get_cache_name()
            msg = (
                f"Unable to update cache '{cn}', "
                "please check 'settings.CACHES' configuration."
            )
            logger.warning(msg)
            raise CacheError(msg)
