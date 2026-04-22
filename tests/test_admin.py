from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles import finders
from django.test import RequestFactory, TestCase

from tests.models import Category
from treenode.admin import TreeNodeModelAdmin


@admin.register(Category)
class CategoryAdmin(TreeNodeModelAdmin):
    pass


class TreeNodeAdminTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertStaticFile(self, path):
        result = finders.find(path)
        self.assertTrue(result is not None)

    def test_staticfiles(self):
        if "treenode" not in settings.INSTALLED_APPS:
            return
        self.assertStaticFile("treenode/css/treenode.css")
        self.assertStaticFile("treenode/js/treenode.js")


class TreeNodeAdminDisplayTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.site = admin.AdminSite()
        self.model_admin = CategoryAdmin(Category, self.site)
        # Create a parent with a name containing HTML special characters
        self.parent = Category.objects.create(name="Root &amp; <Parent>")
        self.child = Category.objects.create(name='Child "Node"', tn_parent=self.parent)

    def _get_request(self, querystring=""):
        return self.factory.get("/admin/tests/category/", querystring)

    def test_accordion_escapes_pk_in_attributes(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_accordion(self.child)
        )
        # data-treenode-pk must contain the raw pk value (integer), not unescaped HTML
        self.assertIn(f'data-treenode-pk="{self.child.pk}"', html)
        self.assertIn(f'data-treenode-parent="{self.parent.pk}"', html)

    def test_accordion_escapes_parent_id_absent_for_root(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_accordion(self.parent)
        )
        # Root node has no parent; data-treenode-parent should be empty string
        self.assertIn('data-treenode-parent=""', html)

    def test_accordion_contains_treenode_span(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_accordion(self.child)
        )
        self.assertIn('class="treenode"', html)
        self.assertIn('data-treenode-accordion="1"', html)

    def test_accordion_display_text_is_not_double_escaped(self):
        # get_display() already applies conditional_escape; mark_safe wraps it so
        # format_html should not escape it again.
        html = str(
            self.model_admin._get_treenode_field_display_with_accordion(self.child)
        )
        # The name 'Child "Node"' gets HTML-escaped once by get_display() →
        # 'Child &quot;Node&quot;'; it must NOT appear as &amp;quot; (double-escaped).
        self.assertNotIn("&amp;quot;", html)
        self.assertIn("&quot;Node&quot;", html)

    def test_breadcrumbs_contains_ancestor_spans(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_breadcrumbs(self.child)
        )
        self.assertIn('class="treenode-breadcrumbs"', html)
        self.assertIn('class="treenode"', html)

    def test_breadcrumbs_root_has_no_breadcrumb_spans(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_breadcrumbs(self.parent)
        )
        # Root node has no ancestors, so no breadcrumb spans
        self.assertNotIn('class="treenode-breadcrumbs"', html)

    def test_breadcrumbs_display_text_is_not_double_escaped(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_breadcrumbs(self.child)
        )
        self.assertNotIn("&amp;quot;", html)
        self.assertIn("&quot;Node&quot;", html)

    def test_indentation_wraps_in_treenode_span(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_indentation(self.child)
        )
        self.assertIn('class="treenode"', html)

    def test_indentation_adds_mdash_per_depth(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_indentation(self.child)
        )
        # child is 1 level deep → one indentation span
        self.assertIn('class="treenode-indentation"', html)

    def test_indentation_root_has_no_indentation_span(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_indentation(self.parent)
        )
        self.assertNotIn('class="treenode-indentation"', html)

    def test_indentation_display_text_is_not_double_escaped(self):
        html = str(
            self.model_admin._get_treenode_field_display_with_indentation(self.child)
        )
        self.assertNotIn("&amp;quot;", html)
        self.assertIn("&quot;Node&quot;", html)

    def test_get_treenode_field_display_routes_accordion(self):
        self.model_admin.treenode_display_mode = (
            TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
        )
        request = self._get_request()
        html = str(self.model_admin._get_treenode_field_display(request, self.child))
        self.assertIn('data-treenode-accordion="1"', html)

    def test_get_treenode_field_display_routes_breadcrumbs(self):
        self.model_admin.treenode_display_mode = (
            TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
        )
        request = self._get_request()
        html = str(self.model_admin._get_treenode_field_display(request, self.child))
        self.assertIn('class="treenode-breadcrumbs"', html)

    def test_get_treenode_field_display_routes_indentation(self):
        self.model_admin.treenode_display_mode = (
            TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION
        )
        request = self._get_request()
        html = str(self.model_admin._get_treenode_field_display(request, self.child))
        self.assertIn('class="treenode-indentation"', html)

    def test_get_treenode_field_display_fallback_with_querystring(self):
        # When querystring is long enough, _use_treenode_display_mode returns False
        # and the default (breadcrumbs) display is used regardless of mode setting.
        self.model_admin.treenode_display_mode = (
            TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
        )
        request = self._get_request({"q": "search_term"})
        html = str(self.model_admin._get_treenode_field_display(request, self.child))
        # Should fall back to breadcrumbs (default) display
        self.assertNotIn('data-treenode-accordion="1"', html)
