from contextlib import contextmanager
from django.apps import apps
from django.core.management.sql import emit_post_migrate_signal
from django.db import connection, OperationalError, ProgrammingError
from django.test import TestCase

from tests.models import Category

ModelToBeDestroyed = Category

class TreeNodeDropTableTestCase(TestCase):
    @contextmanager
    def assertNotRaises(self, exc_type):
        try:
            yield None
        except exc_type as e:
            raise self.failureException('{} raised'.format(e))

    def test_destroy_model(self):
        table_name = ModelToBeDestroyed._meta.db_table
        app_label = ModelToBeDestroyed._meta.app_label
        app_config = apps.get_app_config(app_label)

        # Drop the table (as if by a `migrate app zero`)
        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE {table_name}')

        # Try to use the model - this should raise an error
        with self.assertRaises((OperationalError, ProgrammingError)):
            list(ModelToBeDestroyed.objects.all())

        # Emit a post_migrate signal as done after migration to zero
        with self.assertNotRaises(OperationalError):
            emit_post_migrate_signal(verbosity=1, interactive=False, db=connection.alias)
