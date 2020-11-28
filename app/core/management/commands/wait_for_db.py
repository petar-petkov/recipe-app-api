import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to pause execution until database is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        count = 0
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('[{sec}]Waiting for database...'.format(sec=str(count)))
                count += 1
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))
