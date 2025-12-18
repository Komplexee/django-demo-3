from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Lists all tables in the public schema of the database.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            self.stdout.write(self.style.SUCCESS('Tables in the database:'))
            for table in tables:
                self.stdout.write(table)
