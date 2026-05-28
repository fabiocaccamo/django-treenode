from django import forms

from treenode.utils import split_pks


class TreeNodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "tn_parent" not in self.fields:
            return
        exclude_pks = []
        obj = self.instance
        if obj.pk:
            exclude_pks += [obj.pk]
            exclude_pks += split_pks(obj.tn_descendants_pks)
        manager = obj.__class__.objects
        self.fields["tn_parent"].queryset = manager.prefetch_related(
            "tn_children"
        ).exclude(pk__in=exclude_pks)
