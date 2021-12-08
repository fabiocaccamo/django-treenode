# -*- coding: utf-8 -*-

import django

if django.VERSION >= (3, 0):
    from django.utils.encoding import force_str
else:
    from django.utils.encoding import force_text as force_str
