import csv
from django.core.management.base import BaseCommand
from menu.models import MenuCategory

class Command(BaseCommand):
    help = 'Import menu categories from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import menu categories from')

    def handle(self, *args, **kwargs):
        csv_file=kwargs.get('csv_file')
        if not csv_file:
            self.stdout.write(self.style.ERROR('Please provide a CSV file path'))
            return

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category, created = MenuCategory.objects.get_or_create(
                  name=row['name'],
                  display_order=row['display_order'],
                  is_active=row['is_active'].lower() == "true"
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported menu categories from "%s"' % csv_file))