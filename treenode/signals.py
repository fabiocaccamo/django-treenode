from inspect import isclass

from django.db import connections
from django.db.models.signals import post_delete, post_init, post_migrate, post_save

from treenode.memory import set_ref


def __table_exists(table_name: str, connection_name: str) -> bool:
    return table_name in connections[connection_name].introspection.table_names()


def __is_treenode_model(sender):
    from .models import TreeNodeModel

    # return isinstance(instance, TreeNodeModel) and \
    #         instance.__class__ != TreeNodeModel
    return (
        isclass(sender)
        and issubclass(sender, TreeNodeModel)
        and sender != TreeNodeModel
    )


def post_init_treenode(sender, instance, **kwargs):
    if not __is_treenode_model(sender):
        return
    set_ref(sender, instance)


def post_migrate_treenode(sender, **kwargs):
    for sender_model in sender.get_models():
        if __is_treenode_model(sender_model) and \
             __table_exists(
                 table_name=sender_model._meta.db_table,
                 connection_name=kwargs['using']):
            sender_model.update_tree()


def post_save_treenode(sender, instance, **kwargs):
    if not __is_treenode_model(sender):
        return
    set_ref(sender, instance)
    sender.update_tree()


def post_delete_treenode(sender, instance, **kwargs):
    if not __is_treenode_model(sender):
        return
    sender.update_tree()


def connect_signals():
    post_init.connect(post_init_treenode, dispatch_uid="post_init_treenode")
    post_migrate.connect(post_migrate_treenode, dispatch_uid="post_migrate_treenode")
    post_save.connect(post_save_treenode, dispatch_uid="post_save_treenode")
    post_delete.connect(post_delete_treenode, dispatch_uid="post_delete_treenode")


def disconnect_signals():
    post_init.disconnect(post_init_treenode, dispatch_uid="post_init_treenode")
    post_migrate.disconnect(post_migrate_treenode, dispatch_uid="post_migrate_treenode")
    post_save.disconnect(post_save_treenode, dispatch_uid="post_save_treenode")
    post_delete.disconnect(post_delete_treenode, dispatch_uid="post_delete_treenode")


class no_signals:
    def __enter__(self):
        disconnect_signals()
        return None

    def __exit__(self, type_, value, traceback):
        connect_signals()
