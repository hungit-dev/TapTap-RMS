import csv
from django.core.management.base import BaseCommand
from menu.models import MenuCategory, MenuItem

class Command(BaseCommand):
    help = 'Import menu items from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import menu items from')

    def handle(self, *args, **kwargs):
        csv_file=kwargs.get('csv_file')
        if not csv_file:
            self.stdout.write(self.style.ERROR('Please provide a CSV file path'))
            return

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = MenuCategory.objects.get(name=row["category"])
                item, created = MenuItem.objects.get_or_create(
                    category=category,
                    name=row["name"],
                    description=row["description"],
                    price=row["price"],
                    image_url=row["image_url"] or None,
                    is_available=row["is_available"].lower() == "true",
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported menu categories from "%s"' % csv_file))