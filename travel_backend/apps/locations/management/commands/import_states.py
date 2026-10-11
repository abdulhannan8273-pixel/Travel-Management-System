from apps.locations.models import Country, State
import csv
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import states from CSV" 

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(__file__)
                    )
                )
            )
        )

        file_path = os.path.join(base_dir, "data", "states.csv")

        self.stdout.write(f"Reading file: {file_path}")

        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            self.stdout.write(f"Headers: {reader.fieldnames}")

            for row in reader:
                try:
                    country = Country.objects.get(code=row["country_code"])

                    state, created = State.objects.get_or_create(
                        country=country,
                        code=row["code"],
                        defaults={"name": row["name"]}
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"State added: {state.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"State already exists: {state.name}"))

                except Country.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Country not found: {row['country_code']}"))
       
