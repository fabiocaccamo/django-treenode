from contextlib import contextmanager

from django.core.management.sql import emit_post_migrate_signal
from django.db import OperationalError, ProgrammingError, connection
from django.test import TransactionTestCase

from tests.models import Category

ModelToBeDestroyed = Category


class TreeNodeDropTableTestCase(TransactionTestCase):
    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type as error:
            raise self.failureException(f"{error} raised") from error

    def test_destroy_model(self):
        table_name = ModelToBeDestroyed._meta.db_table

        # drop the table (as if by a `migrate app zero`)
        with connection.cursor() as cursor:
            cursor.execute(f"DROP TABLE {table_name}")

        # try to use the model - this should raise an error
        with self.assertRaises((OperationalError, ProgrammingError)):
            list(ModelToBeDestroyed.objects.all())

        # emit a post_migrate signal as done after migration to zero
        with self.assertNotRaises((OperationalError, ProgrammingError)):
            emit_post_migrate_signal(
                verbosity=1,
                interactive=False,
                db=connection.alias,
            )

        # verify the table is still gone
        with self.assertRaises((OperationalError, ProgrammingError)):
            list(ModelToBeDestroyed.objects.all())


class TreeNodeAbstractProxyTestCase(TransactionTestCase):
    """
    Regression test for issue #215.

    post_migrate_treenode calls update_tree() on every model that passes
    __is_treenode_model().  That check uses only isclass() / issubclass() and
    therefore also matches proxy models that are Python ABCs (i.e. they carry
    unimplemented @abstractmethod declarations).  When the underlying table is
    non-empty, Django tries to materialise rows as instances of the abstract
    class, which raises TypeError.

    This test verifies the inspect.isabstract() guard in
    __is_treenode_model(): without that guard, post_migrate_treenode would
    still call update_tree() for abstract proxy models and raise TypeError.
    """

    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type as error:
            raise self.failureException(f"{error} raised") from error

    def test_post_migrate_does_not_raise_for_abstract_proxy_model(self):
        # Populate the underlying table so that update_tree() actually tries
        # to materialise model instances (empty querysets never trigger the bug).
        Category.objects.create(name="root")

        # Emitting post_migrate must not raise TypeError for abstract proxy
        # models registered in the app.  Without the fix this will fail with:
        #   TypeError: Can't instantiate abstract class AbstractCategoryProxy
        #   without an implementation for abstract method 'my_method'
        with self.assertNotRaises(TypeError):
            emit_post_migrate_signal(
                verbosity=0,
                interactive=False,
                db=connection.alias,
            )
