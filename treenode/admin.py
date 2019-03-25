# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import TreeNodeForm
from .utils import split_pks


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

    TREENODE_DISPLAY_MODE_ACCORDION = 'accordion'
    TREENODE_DISPLAY_MODE_BREADCRUMBS = 'breadcrumbs'
    TREENODE_DISPLAY_MODE_INDENTATION = 'indentation'

    treenode_display_mode = TREENODE_DISPLAY_MODE_INDENTATION

    form = TreeNodeForm
    list_per_page = 1000

    def get_list_display(self, request):
        base_list_display = super(TreeNodeModelAdmin, self).get_list_display(request)
        base_list_display = list(base_list_display)

        def treenode_field_display(obj):
            return self._get_treenode_field_display(request, obj)

        treenode_field_display.short_description = self.model._meta.verbose_name
        treenode_field_display.allow_tags = True

        if len(base_list_display) == 1 and base_list_display[0] == '__str__':
            return (treenode_field_display, )
        else:
            treenode_display_field = getattr(self.model, 'treenode_display_field')
            if len(base_list_display) >= 1 and base_list_display[0] == treenode_display_field:
                base_list_display.pop(0)
            return (treenode_field_display, ) + tuple(base_list_display)

        return base_list_display

    def _get_treenode_display_mode(self, request, obj):
        return self.treenode_display_mode

    def _get_treenode_field_display(self, request, obj):
        display_mode = self._get_treenode_display_mode(request, obj)
        if display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION:
            querystring = (request.GET.urlencode() or '')
            if len(querystring) < 3:
                # querystring exists but probably it's just 'q='
                return self._get_treenode_field_display_with_accordion(obj)
            return self._get_treenode_field_display_with_breadcrumbs(obj)
        elif display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS:
            return self._get_treenode_field_display_with_breadcrumbs(obj)
        elif display_mode == TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION:
            return self._get_treenode_field_display_with_indentation(obj)
        else:
            return self._get_treenode_field_display_with_breadcrumbs(obj)

    def _get_treenode_field_display_with_accordion(self, obj):
        tn_namespace = '%s.%s' % (obj.__module__, obj.__class__.__name__, )
        tn_namespace_key = tn_namespace.lower().replace('.', '_')
        return mark_safe(''\
            '<span class="treenode"'\
                    ' data-treenode-type="%s"'\
                    ' data-treenode-pk="%s"'\
                    ' data-treenode-accordion="1"'\
                    ' data-treenode-depth="%s"'\
                    ' data-treenode-level="%s"'\
                    ' data-treenode-parent="%s">%s</span>' % (
                tn_namespace_key,
                str(obj.pk),
                str(obj.tn_depth),
                str(obj.tn_level),
                str(obj.tn_parent_id or ''),
                obj.get_display(indent=False), ))

    def _get_treenode_field_display_with_breadcrumbs(self, obj):
        obj_display = ''
        for obj_ancestor in obj.get_ancestors():
            obj_ancestor_display = obj_ancestor.get_display(indent=False)
            obj_display += '<span class="treenode-breadcrumbs">%s</span>' % (obj_ancestor_display, )
        obj_display += obj.get_display(indent=False)
        return mark_safe('<span class="treenode">%s</span>' % (obj_display, ))

    def _get_treenode_field_display_with_indentation(self, obj):
        obj_display = '<span class="treenode-indentation">&mdash;</span>' * obj.ancestors_count
        obj_display += obj.get_display(indent=False)
        return mark_safe('<span class="treenode">%s</span>' % (obj_display, ))

    class Media:
        css = {'all':('treenode/css/treenode.css',)}
        js = ['treenode/js/treenode.js']
