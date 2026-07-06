from apps.locations.models import State,City
import csv
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import cities from CSV"

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

        file_path = os.path.join(base_dir, "data", "cities.csv")

        self.stdout.write(f"Reading file: {file_path}")

        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    state = State.objects.get(code=row["state_code"])

                    city, created = City.objects.get_or_create(state=state,name=row["name"])

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Added:{city.name}")
                        )

                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Already Exists: {city.name}")
                        )
                except State.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"State not found:{row['state_code']}")
                    )