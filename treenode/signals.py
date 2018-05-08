# -*- coding: utf-8 -*-

from django.db.models.signals import (
    post_delete, post_init, post_save, )

from .memory import set_ref


def __is_treenode_signal(instance):
    from .models import TreeNodeModel
    return isinstance(instance, TreeNodeModel) and \
            instance.__class__ != TreeNodeModel


def post_init_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(instance):
        return
    set_ref(sender, instance)


def post_save_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(instance):
        return
    set_ref(sender, instance)
    sender.update_tree()


def post_delete_treenode(sender, instance, **kwargs):
    if not __is_treenode_signal(instance):
        return
    sender.update_tree()


def connect_signals():
    post_init.connect(
        post_init_treenode, dispatch_uid='post_init_treenode')
    post_save.connect(
        post_save_treenode, dispatch_uid='post_save_treenode')
    post_delete.connect(
        post_delete_treenode, dispatch_uid='post_delete_treenode')


def disconnect_signals():
    post_init.disconnect(
        post_init_treenode, dispatch_uid='post_init_treenode')
    post_save.disconnect(
        post_save_treenode, dispatch_uid='post_save_treenode')
    post_delete.disconnect(
        post_delete_treenode, dispatch_uid='post_delete_treenode')


class no_signals():
    def __enter__(self):
        disconnect_signals()
        return None
    def __exit__(self, type, value, traceback):
        connect_signals()
