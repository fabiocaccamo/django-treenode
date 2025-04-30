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
