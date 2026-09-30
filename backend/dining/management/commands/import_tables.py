import csv
from django.core.management.base import BaseCommand
from dining.models import Table

class Command(BaseCommand):
    help = 'Import tables from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import tables from')

    def handle(self, *args, **kwargs):
        csv_file=kwargs.get('csv_file')
        if not csv_file:
            self.stdout.write(self.style.ERROR('Please provide a CSV file path'))
            return

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
               table, created = Table.objects.get_or_create(
                    table_number=row["table_number"],
                    defaults={
                        "capacity": row["capacity"],
                        "status": row["status"],
                        "is_active": row["is_active"],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported tables from "%s"' % csv_file))