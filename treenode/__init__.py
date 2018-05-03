# -*- coding: utf-8 -*-

class classproperty(object):

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)