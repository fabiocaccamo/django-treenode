# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe


class TreeNodeModelAdmin(admin.ModelAdmin):

    def get_treenode_display(self, obj, text, style='', accordion=True):
        parents_count = obj.parents_count
        parent_pk = ''
        if parents_count:
            parents_pks_list = obj.split_pks(obj.parents_pks)
            parent_pk = parents_pks_list[-1]
        tabs = ('&mdash; ' * parents_count)
        tabs_class = 'treenode-tabs' if tabs else ''
        return mark_safe(''\
            '<span class="treenode" style="%s"'\
                    ' data-treenode="%s"'\
                    ' data-treenode-accordion="%s"'\
                    ' data-treenode-depth="%s"'\
                    ' data-treenode-level="%s"'\
                    ' data-treenode-parent="%s">'\
                '<span class="%s">%s</span> %s'\
            '</span>' % (style,
                str(obj.pk),
                str(int(accordion)),
                str(obj.depth),
                str(obj.level),
                str(parent_pk),
                tabs_class, tabs, text, ))

    class Media:
        css = {'all':(static('/treenode/css/treenode.css'),)}
        js = [static('/treenode/js/treenode.js')]
