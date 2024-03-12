from django.contrib import admin
from django.utils.safestring import mark_safe

from treenode.forms import TreeNodeForm


class TreeNodeModelAdmin(admin.ModelAdmin):
    """
    Usage:

    from django.contrib import admin
    from treenode.admin import TreeNodeModelAdmin
    from treenode.forms import TreeNodeForm
    from .models import MyModel


    class MyModelAdmin(TreeNodeModelAdmin):

        treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
        # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
        # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION

        form = TreeNodeForm

    admin.site.register(MyModel, MyModelAdmin)
    """

    TREENODE_DISPLAY_MODE_ACCORDION = "accordion"
    TREENODE_DISPLAY_MODE_BREADCRUMBS = "breadcrumbs"
    TREENODE_DISPLAY_MODE_INDENTATION = "indentation"

    treenode_display_mode = TREENODE_DISPLAY_MODE_INDENTATION

    form = TreeNodeForm
    list_per_page = 1000
    ordering = ("tn_order",)

    def get_list_display(self, request):
        base_list_display = super().get_list_display(request)
        base_list_display = list(base_list_display)

        def treenode_field_display(obj):
            return self._get_treenode_field_display(request, obj)

        treenode_field_display.short_description = self.model._meta.verbose_name

        if len(base_list_display) == 1 and base_list_display[0] == "__str__":
            return (treenode_field_display,)
        else:
            treenode_display_field = self.model.treenode_display_field
            if (
                len(base_list_display) >= 1
                and base_list_display[0] == treenode_display_field
            ):
                base_list_display.pop(0)
            return (treenode_field_display,) + tuple(base_list_display)

        return base_list_display

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related("tn_parent")
        return qs

    def _use_treenode_display_mode(self, request, obj):
        querystring = request.GET.urlencode() or ""
        return len(querystring) <= 2

    def _get_treenode_display_mode(self, request, obj):
        return self.treenode_display_mode

    def _get_treenode_field_default_display(self, obj):
        return self._get_treenode_field_display_with_breadcrumbs(obj)

    def _get_treenode_field_display(self, request, obj):
        if not self._use_treenode_display_mode(request, obj):
            return self._get_treenode_field_default_display(obj)
        display_mode = self._get_treenode_display_mode(request, obj)
        if display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION:
            return self._get_treenode_field_display_with_accordion(obj)
        elif display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS:
            return self._get_treenode_field_display_with_breadcrumbs(obj)
        elif display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION:
            return self._get_treenode_field_display_with_indentation(obj)
        else:
            return self._get_treenode_field_default_display(obj)

    def _get_treenode_field_display_with_accordion(self, obj):
        tn_namespace = f"{obj.__module__}.{obj.__class__.__name__}"
        tn_namespace_key = tn_namespace.lower().replace(".", "_")
        obj_parent_id = obj.tn_parent_id if obj.tn_parent_id else ""
        obj_display = obj.get_display(indent=False)
        return mark_safe(
            f'<span class="treenode"'  # noqa: B907
            f' data-treenode-type="{tn_namespace_key}"'
            f' data-treenode-pk="{obj.pk}"'
            f' data-treenode-accordion="1"'
            f' data-treenode-depth="{obj.tn_depth}"'
            f' data-treenode-level="{obj.tn_level}"'
            f' data-treenode-parent="{obj_parent_id}">{obj_display}</span>'
        )

    def _get_treenode_field_display_with_breadcrumbs(self, obj):
        obj_display = ""
        for obj_ancestor in obj.get_ancestors():
            obj_ancestor_display = obj_ancestor.get_display(indent=False)
            obj_display += (
                f'<span class="treenode-breadcrumbs">{obj_ancestor_display}</span>'
            )

        obj_display += obj.get_display(indent=False)
        return mark_safe(f'<span class="treenode">{obj_display}</span>')

    def _get_treenode_field_display_with_indentation(self, obj):
        obj_display = (
            '<span class="treenode-indentation">&mdash;</span>' * obj.ancestors_count
        )
        obj_display += obj.get_display(indent=False)
        return mark_safe(f'<span class="treenode">{obj_display}</span>')

    class Media:
        css = {"all": ("treenode/css/treenode.css",)}
        js = ["treenode/js/treenode.js"]
