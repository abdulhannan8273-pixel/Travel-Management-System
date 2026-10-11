import pandas as pd

from rest_framework import status
from rest_framework.response import Response

from .models import Country, State, City
def import_countries(file):
    try:
        # Read CSV
        df = pd.read_csv(file)

        # Required columns
        required_columns = ["name", "code"]

        # Check columns
        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        countries = []

        for _, row in df.iterrows():

            # Skip duplicate country code
            if Country.objects.filter(code=row["code"]).exists():
                continue

            countries.append(
                Country(
                    name=row["name"],
                    code=row["code"],
                    is_active=True,
                )
            )

        Country.objects.bulk_create(countries)

        return Response(
            {
                "success": True,
                "message": f"{len(countries)} countries imported successfully."
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
    


def import_states(file):
    try:
        df = pd.read_csv(file)

        required_columns = ["country_code", "name", "code"]

        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        states = []

        for _, row in df.iterrows():

            try:
                country = Country.objects.get(code=row["country_code"])
            except Country.DoesNotExist:
                continue

            if State.objects.filter(
                country=country,
                name=row["name"]
            ).exists():
                continue

            states.append(
                State(
                    country=country,
                    name=row["name"],
                    code=row["code"],
                    is_active=True,
                )
            )

        State.objects.bulk_create(states)

        return Response(
            {
                "success": True,
                "message": f"{len(states)} states imported successfully."
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
    

def import_cities(file):
    try:
        df = pd.read_csv(file)

        required_columns = ["state_code", "name"]

        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        cities = []

        for _, row in df.iterrows():

            try:
                state = State.objects.get(code=row["state_code"])
            except State.DoesNotExist:
                continue

            if City.objects.filter(
                state=state,
                name=row["name"]
            ).exists():
                continue

            cities.append(
                City(
                    state=state,
                    name=row["name"],
                    is_active=True,
                )
            )

        City.objects.bulk_create(cities)

        return Response(
            {
                "success": True,
                "message": f"{len(cities)} cities imported successfully."
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