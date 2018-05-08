# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
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

        treenode_accordion = True
        form = TreeNodeForm

    admin.site.register(MyModel, MyModelAdmin)
    """

    form = TreeNodeForm
    treenode_accordion = False
    list_per_page = 1000

    def get_list_display(self, request):
        base_list_display = super(TreeNodeModelAdmin, self).get_list_display(request)
        def treenode_field_display(obj):
            return self.__get_treenode_field_display(
                obj, accordion=self.treenode_accordion, style='')
        treenode_field_display.short_description = self.model._meta.verbose_name
        treenode_field_display.allow_tags = True
        if len(base_list_display) == 1 and base_list_display[0] == '__str__':
            return (treenode_field_display, )
        else:
            return (treenode_field_display, ) + base_list_display
        return base_list_display

    def get_list_filter(self, request):
        return None

    def __get_treenode_field_display(self, obj, accordion=True, style=''):
        parents_count = obj.tn_parents_count
        parent_pk = ''
        if parents_count:
            parents_pks_list = split_pks(obj.tn_parents_pks)
            parent_pk = parents_pks_list[-1]
        tabs = ('&mdash; ' * parents_count)
        tabs_class = 'treenode-tabs' if tabs else ''
        model_package = '%s.%s' % (obj.__module__, obj.__class__.__name__, )
        return mark_safe(''\
            '<span class="treenode" style="%s"'\
                    ' data-treenode-type="%s"'\
                    ' data-treenode-pk="%s"'\
                    ' data-treenode-accordion="%s"'\
                    ' data-treenode-depth="%s"'\
                    ' data-treenode-level="%s"'\
                    ' data-treenode-parent="%s">'\
                '<span class="%s">%s</span> %s'\
            '</span>' % (style,
                model_package.lower().replace('.', '_'),
                str(obj.pk),
                str(int(accordion)),
                str(obj.tn_depth),
                str(obj.tn_level),
                str(parent_pk),
                tabs_class, tabs, obj.get_display(indent=False), ))

    class Media:
        css = {'all':(static('/treenode/css/treenode.css'),)}
        js = [static('/treenode/js/treenode.js')]
