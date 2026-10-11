from decimal import Decimal
import pandas as pd

from rest_framework import status
from rest_framework.response import Response

from apps.locations.models import Country, State, City
from .models import Destination


def import_destinations(file):
    try:
        df = pd.read_csv(file)

        required_columns = [
            "name",
            "country_code",
            "state_code",
            "city_name",
            "description",
            "price",
        ]

        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        destinations = []

        for _, row in df.iterrows():

            try:
                country = Country.objects.get(code=row["country_code"])
                state = State.objects.get(
                    code=row["state_code"],
                    country=country,
                )
                city = City.objects.get(
                    name=row["city_name"],
                    state=state,
                )

            except (Country.DoesNotExist,
                    State.DoesNotExist,
                    City.DoesNotExist):
                continue

            if Destination.objects.filter(
                name=row["name"],
                city=city,
            ).exists():
                continue

            destinations.append(
                Destination(
                    name=row["name"],
                    country=country,
                    state=state,
                    city=city,
                    description=row["description"],
                    price=Decimal(row["price"]),
                    rating=Decimal(row.get("rating", 0)),
                    best_time_to_visit=row.get("best_time_to_visit", ""),
                    is_featured=bool(row.get("is_featured", False)),
                    weather=row.get("weather", ""),
                    latitude=row.get("latitude"),
                    longitude=row.get("longitude"),
                    currency=row.get("currency", ""),
                    language=row.get("language", ""),
                    timezone=row.get("timezone", ""),
                    popular_attractions=row.get("popular_attractions", ""),
                    travel_tips=row.get("travel_tips", ""),
                    average_budget=row.get("average_budget"),
                    is_active=True,
                )
            )

        Destination.objects.bulk_create(destinations)

        return Response(
            {
                "success": True,
                "message": f"{len(destinations)} destinations imported successfully."
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )