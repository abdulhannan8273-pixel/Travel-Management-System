from apps.locations.models import Country, State, City
from apps.destinations.models import Destination
import csv
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import destinations from CSV"

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

        file_path = os.path.join(base_dir, "data", "destinations.csv")

        self.stdout.write(f"Reading file: {file_path}")

        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            self.stdout.write(f"Headers: {reader.fieldnames}")

            for row in reader:
                try:
                    country = Country.objects.get(code=row["country_code"])
                    state = State.objects.get(code=row["state_code"])
                    city = City.objects.get(name=row["city"])

                    destination, created = Destination.objects.get_or_create(
                        country=country,
                        state=state,
                        city=city,
                        name=row["name"],
                        defaults={
                            "description": row["description"],
                            "price": row["price"],
                            "rating": row["rating"],
                            "best_time_to_visit": row["best_time_to_visit"]
                        },
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f"Added: {destination.name}")
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"Already Exists: {destination.name}")
                        )
                
                except Country.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Country not found: {row['country_code']}")
                    )

                except State.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"State not found: {row['state_code']}")
                    )
                except City.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"City not found: {row['city']}")
                    )