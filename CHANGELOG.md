# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.17.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.17.0) - 2021-06-11
-  Added handling for `UUID` primary keys (thanks to @cperrin88). #31
-  Reduced admin changelist queries.
-  Added `TreeNodeModel` utility methods and properties to retrieve only pk(s):
    - method `get_ancestors_pks()` / property `ancestors_pks`
    - method `get_children_pks()` / property `children_pks`
    - method `get_descendants_pks()` / property `descendants_pks`
    - method `get_parent_pk()` / property `parent_pk`
    - method `get_root_pk()` / property `root_pk`
    - method `get_siblings_pks()` / property `siblings_pks`

## [0.16.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.16.0) - 2021-04-21
-  Added `python 3.9` and `django 3.2` to `tox` and `travis`.
-  Added `get_display_text` method. #27
-  Fixed `TreeNodeModelAdmin` duplicated query.
-  Updated `debug_performance` decorator to work only if `settings.DEBUG = True`.

## [0.15.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.15.0) - 2020-09-16
-  Added custom `cache` back-end support. #19 #24
-  Fixed tests warning (admin.W411).

## [0.14.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.14.2) - 2020-03-07
## [0.14.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.14.1) - 2020-03-04
## [0.14.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.14.0) - 2019-12-03
## [0.13.4](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.13.4) - 2019-07-24
## [0.13.3](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.13.3) - 2019-07-01
## [0.13.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.13.2) - 2019-06-28
## [0.13.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.13.1) - 2019-04-12
## [0.13.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.13.0) - 2019-03-25
## [0.12.3](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.12.3) - 2019-03-19
## [0.12.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.12.2) - 2019-02-06
## [0.12.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.12.1) - 2018-12-15
## [0.12.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.12.0) - 2018-12-14
## [0.11.3](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.11.3) - 2018-09-06
## [0.11.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.11.2) - 2018-07-12
## [0.11.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.11.1) - 2018-06-30
## [0.11.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.11.0) - 2018-06-29
## [0.10.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.10.1) - 2018-06-27
## [0.10.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.10.0) - 2018-06-18
## [0.9.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.9.0) - 2018-06-11
## [0.8.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.8.1) - 2018-05-17
## [0.8.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.8.0) - 2018-05-17
## [0.7.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.7.1) - 2018-05-11
## [0.7.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.7.0) - 2018-05-11
## [0.6.4](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.6.4) - 2018-05-09
## [0.6.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.6.0) - 2018-05-08
## [0.5.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.5.0) - 2018-05-03
## [0.4.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.4.1) - 2018-04-24
## [0.3.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.3.0) - 2018-04-20
## [0.2.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.2.2) - 2018-04-18
## [0.2.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.2.1) - 2018-04-17
## [0.1.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.1.0) - 2018-04-13