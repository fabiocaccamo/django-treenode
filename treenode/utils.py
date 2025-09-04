PKS_SEPARATOR = ","


def contains_pk(ls, pk):
    return str(pk) in split_pks(ls)


def join_pks(ls):
    if not ls:
        return ""
    s = PKS_SEPARATOR.join([str(v) for v in ls])
    return s


def split_pks(s):
    if not s:
        return []
    ls = [v for v in s.split(PKS_SEPARATOR) if v]
    return ls
