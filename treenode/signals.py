from inspect import isabstract, isclass

from django.db import connections
from django.db.models.signals import post_delete, post_init, post_migrate, post_save

from treenode.memory import set_ref


def __table_exists(table_name: str, connection_name: str) -> bool:
    return table_name in connections[connection_name].introspection.table_names()


def __is_treenode_model(sender):
    from .models import TreeNodeModel

    return (
        isclass(sender)
        and issubclass(sender, TreeNodeModel)
        and sender != TreeNodeModel
        and not isabstract(sender)
    )


def __get_treenode_fields_snapshot(instance):
    return {
        "tn_parent_id": instance.tn_parent_id,
        "tn_priority": instance.tn_priority,
        "display_text": instance.get_display_text(),
    }


def __has_treenode_fields_changed(sender, instance, update_fields):
    if update_fields is not None:
        structural_fields = {"tn_parent", "tn_parent_id", "tn_priority"}
        display_field = getattr(sender, "treenode_display_field", None)
        if display_field:
            structural_fields.add(display_field)
        return bool(structural_fields.intersection(update_fields))
    fields_snapshot = getattr(instance, "_tn_snapshot", None)
    if fields_snapshot is None:
        return True
    return fields_snapshot != __get_treenode_fields_snapshot(instance)


def post_init_treenode(sender, instance, **kwargs):
    if not __is_treenode_model(sender):
        return
    set_ref(sender, instance)
    instance._tn_snapshot = __get_treenode_fields_snapshot(instance)


def post_migrate_treenode(sender, **kwargs):
    for sender_model in list(sender.get_models()):
        if __is_treenode_model(sender_model) and __table_exists(
            table_name=sender_model._meta.db_table, connection_name=kwargs["using"]
        ):
            sender_model.update_tree()


def post_save_treenode(sender, instance, created, **kwargs):
    if not __is_treenode_model(sender):
        return
    set_ref(sender, instance)

    if not created:
        update_fields = kwargs.get("update_fields")
        if not __has_treenode_fields_changed(sender, instance, update_fields):
            return

    sender.update_tree()
    instance._tn_snapshot = __get_treenode_fields_snapshot(instance)


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
