# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.23.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.23.2) - 2025-09-04
-   Fix `set_parent` not properly finding descendants. #196
-   Bump test requirements.
-   Bump `pre-commit` hooks.

## [0.23.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.23.1) - 2025-04-30
-   Fix call to `update_tree` upon migration to zero causes `ProgrammingError`. #188 (by [@danilo-botelho](https://github.com/danilo-botelho) in #189)
-   Update linter settings.
-   Bump `pre-commit` hooks.

## [0.23.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.23.0) - 2025-04-03
-   Add `Django 5.2` support.
-   Bump `pre-commit` hooks.
-   Bump requirements.

## [0.22.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.22.2) - 2025-02-05
-   Fix when `list_display_links = None` there is no encapsulating `<a>` tag. (by [@bernieke](https://github.com/bernieke) in #168)
-   Bump test requirements.
-   Bump `pre-commit` hooks.

## [0.22.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.22.1) - 2023-09-20
-   Increase `tn_priority` max value to `9999999999` to allow nodes sorting by timestamp. (by [@simensol](https://github.com/simensol) in #166)
-   Bump test requirements.
-   Bump `pre-commit` hooks.

## [0.22.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.22.0) - 2023-01-31
-   Ensure cache has been updated, otherwise log a warning.
-   Fix tree methods not working if cache is not configured correctly.
-   Code refactoring.
-   Bump requirements.
-   Bump `pre-commit` hooks.
-   Bump GitHub action.

## [0.21.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.21.0) - 2023-12-05
-   Add `Python 3.12` support.
-   Add `Django 5.0` support.
-   Speed-up test workflow.
-   Bump requirements.
-   Bump `pre-commit` hooks.

## [0.20.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.20.2) - 2023-09-26
-   Use specific database for write operations in multi-database setup. #123 (by [@Nathan-Cohen](https://github.com/Nathan-Cohen) in #124)
-   Bump requirements and `pre-commit` hooks.

## [0.20.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.20.1) - 2023-06-02
-   Fix `AttributeError: 'NoneType' object has no attribute 'get_parent_pk'` when loading fixtures. #88
-   Fix model tree update when receiving `post_migrate` signal.

## [0.20.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.20.0) - 2023-05-29
-   Add `pyupgrade` (`Python >= 3.8`) to `pre-commit` config.
-   Add `Django 4.2` support and drop `Django 2.2` support.
-   Add `django-upgrade` (`Django >= 3.2`) to `pre-commit` hooks.
-   Add `metadata` module.
-   Add locales support.
-   Add string primary key support. #81
-   Fix XSS vulnerability in `get_display_text` method.
-   Replace `str.format` with `f-string`.
-   Replace `flake8` with `Ruff`.
-   Replace `setup.py` in favor of `pyproject.toml`.
-   Run `pre-commit` also with `tox`.
-   Pin test requirements.
-   Bump requirements and `pre-commit` hooks.
-   Rename default branch from `master` to `main`.

## [0.19.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.19.0) - 2022-12-14
-   Add `Python 3.11` and `django 4.1` support.
-   Drop `Python < 3.8` and `Django < 2.2` support. #67
-   Add `pre-commit`.
-   Bump requirements and actions.
-   Replace `str.format` with `f-strings`.
-   Replace `setup.py test` in favor of `runtests.py`.

## [0.18.2](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.18.2) - 2022-07-19
-   Improved `get_breadcrumbs` performance.

## [0.18.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.18.1) - 2021-12-22
-   Fixed positive integer fields for big trees. #51

## [0.18.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.18.0) - 2021-12-08
-   Added django 4.0 compatibility.
-   Added `cascade` option to `delete` method. #40
-   Added documentation for bulk operations. #41 #42 #45
-   Removed console verbose logging. #36
-   Removed display fallback to str method due to recursion error.
-   Fixed order field too small for big trees. #44
-   Fixed tests auto-field warning.

## [0.17.1](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.17.1) - 2021-12-07
-   Replaced travis CI with GitHub workflow.
-   Added python 3.10 support.
-   Added feature: use `__str__` as default fallback for `treenode_display_field`.
-   Fixed backward compatibility.

## [0.17.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.17.0) - 2021-06-11
-   Added handling for `UUID` primary keys (thanks to @cperrin88). #31
-   Reduced admin changelist queries.
-   Added `TreeNodeModel` utility methods and properties to retrieve only pk(s):
    - method `get_ancestors_pks()` / property `ancestors_pks`
    - method `get_children_pks()` / property `children_pks`
    - method `get_descendants_pks()` / property `descendants_pks`
    - method `get_parent_pk()` / property `parent_pk`
    - method `get_root_pk()` / property `root_pk`
    - method `get_siblings_pks()` / property `siblings_pks`

## [0.16.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.16.0) - 2021-04-21
-   Added `python 3.9` and `django 3.2` to `tox` and `travis`.
-   Added `get_display_text` method. #27
-   Fixed `TreeNodeModelAdmin` duplicated query.
-   Updated `debug_performance` decorator to work only if `settings.DEBUG = True`.

## [0.15.0](https://github.com/fabiocaccamo/django-treenode/releases/tag/0.15.0) - 2020-09-16
-   Added custom `cache` back-end support. #19 #24
-   Fixed tests warning (admin.W411).

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
