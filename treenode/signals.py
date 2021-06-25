# -*- coding: utf-8 -*-
import os
import sys
from django.db.models.signals import (
    post_delete, post_init, post_migrate, post_save, )

from inspect import isclass

from .memory import set_ref


def __is_treenode_signal(sender):
    from .models import TreeNodeModel
    # return isinstance(instance, TreeNodeModel) and \
    #         instance.__class__ != TreeNodeModel
    return isclass(sender) and \
            issubclass(sender, TreeNodeModel) and \
            sender != TreeNodeModel


def post_init_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(sender):
        return
    set_ref(sender, instance)


def post_migrate_treenode(sender, **kwargs):
    if not __is_treenode_signal(sender):
        return
    sender.update_tree()


def post_save_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(sender):
        return
    set_ref(sender, instance)
    sender.update_tree()


def post_delete_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(sender):
        return
    sender.update_tree()


def connect_signals():
    #
    # Try to handle loaddata and test arguments which dont want these signals
    #
    if os.getenv('SKIP_SIGNALS'):
        action = 'force_skip'
    else:
        try:
            action = sys.argv[1]
        except Exception as e:
            action = None
    if action not in ('force_skip', 'loaddata', 'test',):
        post_init.connect(
            post_init_treenode, dispatch_uid='post_init_treenode')
        post_migrate.connect(
            post_migrate_treenode, dispatch_uid='post_migrate_treenode')
        post_save.connect(
            post_save_treenode, dispatch_uid='post_save_treenode')
        post_delete.connect(
            post_delete_treenode, dispatch_uid='post_delete_treenode')


def disconnect_signals():
    post_init.disconnect(
        post_init_treenode, dispatch_uid='post_init_treenode')
    post_migrate.disconnect(
        post_migrate_treenode, dispatch_uid='post_migrate_treenode')
    post_save.disconnect(
        post_save_treenode, dispatch_uid='post_save_treenode')
    post_delete.disconnect(
        post_delete_treenode, dispatch_uid='post_delete_treenode')


class no_signals():
    def __enter__(self):
        disconnect_signals()
        return None
    def __exit__(self, type_, value, traceback):
        connect_signals()
