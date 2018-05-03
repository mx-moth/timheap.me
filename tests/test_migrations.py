from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class TestMigrations(TestCase):
    def test_no_missing_migrations(self):
        command = [
            'makemigrations',
            '--check',
            '--dry-run',
            '--no-color',
            '--name=missing_migration',
        ]
        try:
            out = StringIO()
            call_command(*command, stdout=out)
        except SystemExit:
            out.seek(0)
            self.fail(msg='Missing migrations:\n\n' + out.read())
