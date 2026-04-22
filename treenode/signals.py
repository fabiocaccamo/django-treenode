from inspect import isabstract, isclass
import weakref

from django.db import connections
from django.db.models.signals import post_delete, post_init, post_migrate, post_save

from treenode.memory import set_ref

# Sentinel that distinguishes "no snapshot captured" from any real tuple value.
_NO_SNAPSHOT = object()

# Maps each live model instance to its structural-field snapshot captured at
# post_init time.  Using a WeakKeyDictionary avoids polluting model instances
# with extra attributes and ensures entries are freed when an instance is GC'd.
_snapshots: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()


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
        and not isabstract(sender)
    )


def __structural_snapshot(sender, instance):
    """Return a tuple of all field values that, when changed, require update_tree."""
    display_field = getattr(sender, "treenode_display_field", None)
    return (
        instance.tn_parent_id,
        instance.tn_priority,
        getattr(instance, display_field, None) if display_field else None,
    )


def post_init_treenode(sender, instance, **kwargs):
    if not __is_treenode_model(sender):
        return
    set_ref(sender, instance)
    # 1B: capture structural field values at load/init time so that
    # post_save_treenode can compare and skip update_tree when nothing that
    # affects the tree structure or ordering has changed.
    # Unsaved instances (pk=None) are unhashable and are always treated as
    # creates in post_save, so there is no point snapshotting them here.
    if instance.pk:
        _snapshots[instance] = __structural_snapshot(sender, instance)


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
        # 1A: if the caller explicitly passed update_fields and none of the
        # listed fields affect tree structure or ordering, skip update_tree.
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            structural_fields = {"tn_parent", "tn_parent_id", "tn_priority"}
            display_field = getattr(sender, "treenode_display_field", None)
            if display_field:
                structural_fields.add(display_field)
            if not structural_fields.intersection(update_fields):
                return
        else:
            # 1B: no update_fields passed (full save); compare the snapshot
            # captured at post_init time with the current values and skip
            # update_tree when nothing structural has changed.
            snapshot = _snapshots.get(instance, _NO_SNAPSHOT)
            if snapshot is not _NO_SNAPSHOT:
                if snapshot == __structural_snapshot(sender, instance):
                    return

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
