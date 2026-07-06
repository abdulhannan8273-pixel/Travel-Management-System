from apps.locations.models import Country
import csv
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import countries from CSV"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        file_path = os.path.join(base_dir, "data", "countries.csv")

        self.stdout.write(f"Reading file: {file_path}")

        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            self.stdout.write(f"Headers: {reader.fieldnames}")

            for row in reader:
                country, created = Country.objects.get_or_create(
                    code=row["code"],
                    defaults={"name": row["name"]},
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Country added: {country.name}"))
                else:
                    self.stdout.write(f"Country already exists: {country.name}")