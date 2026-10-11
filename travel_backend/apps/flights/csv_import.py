import pandas as pd
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response

from .models import Flight, Airline, Airport

def import_airlines(file):
    try:
        df = pd.read_csv(file)

        required_columns = ["name", "code", "country"]

        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        airlines = []

        for _, row in df.iterrows():

            if Airline.objects.filter(code=row["code"]).exists():
                continue

            airlines.append(
                Airline(
                    name=row["name"],
                    code=row["code"],
                    country=row["country"],
                    is_active=True,
                )
            )

        Airline.objects.bulk_create(airlines)

        return Response(
            {
                "success": True,
                "message": f"{len(airlines)} airlines imported successfully."
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
    
def import_airports(file):
    try:
        # Read CSV
        df = pd.read_csv(file)

        # Required columns
        required_columns = [
            "name",
            "code",
            "city",
            "country",
        ]

        # Validate columns
        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        airports = []

        for _, row in df.iterrows():

            # Skip duplicate airport code
            if Airport.objects.filter(code=row["code"]).exists():
                continue

            airports.append(
                Airport(
                    name=row["name"],
                    code=row["code"],
                    city=row["city"],
                    country=row["country"],
                )
            )

        Airport.objects.bulk_create(airports)

        return Response(
            {
                "success": True,
                "message": f"{len(airports)} airports imported successfully."
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
    


    
def import_flights(file):
    try:
        # Read CSV
        df = pd.read_csv(file)

        # Required Columns
        required_columns = [
            "flight_number",
            "airline_code",
            "source_airport",
            "destination_airport",
            "departure_time",
            "arrival_time",
            "flight_class",
            "price",
            "total_seats",
            "status",
        ]

        # Validate Columns
        for column in required_columns:
            if column not in df.columns:
                return Response(
                    {
                        "success": False,
                        "message": f"Missing column: {column}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        flights = []

        for _, row in df.iterrows():
            airline = Airline.objects.filter(
                code=row["airline_code"]
            ).first()

            source_airport = Airport.objects.filter(
                code=row["source_airport"]
            ).first()

            destination_airport = Airport.objects.filter(
                code=row["destination_airport"]
            ).first()

            if not airline or not source_airport or not destination_airport:
                continue

            if Flight.objects.filter(
                flight_number=row["flight_number"]
            ).exists():
                continue

            departure_time = datetime.strptime(
                row["departure_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            arrival_time = datetime.strptime(
                row["arrival_time"],
                "%Y-%m-%d %H:%M:%S"
            )

            duration = arrival_time - departure_time

            flights.append(
                Flight(
                    flight_number=row["flight_number"],
                    airline=airline,
                    source_airport=source_airport,
                    destination_airport=destination_airport,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    duration=duration,
                    flight_class=row["flight_class"],
                    price=row["price"],
                    total_seats=int(row["total_seats"]),
                    available_seats=int(row["total_seats"]),
                    status=row["status"],
                    is_active=True,
                )
            )

        if not flights:
            return Response(
                {
                    "success": False,
                    "message": "No valid flights found to import."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        Flight.objects.bulk_create(flights)

        return Response(
            {
                "success": True,
                "message": f"{len(flights)} flights imported successfully."
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