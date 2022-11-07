# -*- coding: utf-8 -*-

PKS_SEPARATOR = ","


def join_pks(ls):
    return PKS_SEPARATOR.join([str(v) for v in ls]) if ls else ""


def split_pks(s):
    return [v for v in s.split(PKS_SEPARATOR) if v] if s else []
