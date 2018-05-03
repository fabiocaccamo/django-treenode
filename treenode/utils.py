# -*- coding: utf-8 -*-

PKS_SEPARATOR = ','

def join_pks(l):
    if not l:
        return ''
    s = PKS_SEPARATOR.join([str(v) for v in l])
    return s

def split_pks(s):
    if not s:
        return []
    l = [int(v) for v in s.split(PKS_SEPARATOR) if v]
    return l
