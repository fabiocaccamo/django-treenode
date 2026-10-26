from django.template import Context, Template
from django.test import TestCase
from django.utils.html import conditional_escape

from tests.models import Category


class TreeNodeDisplayTestCase(TestCase):
    def setUp(self):
        self.root = Category.objects.create(name="Root & <Parent>")
        self.child = Category.objects.create(name='Child "Node"', tn_parent=self.root)
        # the tn_ fields are computed by the tree update that runs after insert
        self.root.refresh_from_db()
        self.child.refresh_from_db()

    def tearDown(self):
        pass

    def test_get_display_escapes_the_display_text(self):
        self.assertEqual(
            self.root.get_display(indent=False), "Root &amp; &lt;Parent&gt;"
        )
        self.assertEqual(self.child.get_display(indent=False), "Child &quot;Node&quot;")

    def test_get_display_escapes_the_indentation_mark(self):
        self.assertEqual(self.child.tn_ancestors_count, 1)
        self.assertEqual(
            self.child.get_display(indent=True, mark="<b>"),
            "&lt;b&gt;Child &quot;Node&quot;",
        )

    def test_get_display_keeps_a_plain_text_indentation_mark(self):
        self.assertEqual(self.child.tn_ancestors_count, 1)
        self.assertEqual(
            self.child.get_display(indent=True, mark="- "), "- Child &quot;Node&quot;"
        )

    def test_get_display_is_already_escaped(self):
        # the result is safe HTML, so escaping it again must be a no-op
        display = self.child.get_display()
        self.assertEqual(conditional_escape(display), display)

    def test_str_escapes_the_display_text_only_once(self):
        self.assertNotIn("&amp;amp;", str(self.root))
        self.assertNotIn("&amp;lt;", str(self.root))
        self.assertIn("Root &amp; &lt;Parent&gt;", str(self.root))
        self.assertNotIn("&amp;quot;", str(self.child))
        self.assertIn("Child &quot;Node&quot;", str(self.child))

    def test_template_rendering_escapes_the_display_text_only_once(self):
        rendered = Template("{{ obj }}").render(Context({"obj": self.child}))
        self.assertNotIn("&amp;quot;", rendered)
        self.assertIn("Child &quot;Node&quot;", rendered)

    def test_get_tree_display_escapes_the_display_text_only_once(self):
        tree_display = Category.get_tree_display()
        self.assertNotIn("&amp;amp;", tree_display)
        self.assertNotIn("&amp;quot;", tree_display)
        self.assertIn("Root &amp; &lt;Parent&gt;", tree_display)
        self.assertIn("Child &quot;Node&quot;", tree_display)

    def test_get_descendants_tree_display_escapes_the_display_text_only_once(self):
        descendants_display = self.root.get_descendants_tree_display()
        self.assertNotIn("&amp;quot;", descendants_display)
        self.assertIn("Child &quot;Node&quot;", descendants_display)
