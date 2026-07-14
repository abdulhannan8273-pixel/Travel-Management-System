from decimal import Decimal

from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.accounts.models import User
from apps.destinations.models import Destination
from apps.hotels.models import Hotel, Room
from apps.flights.models import Flight, FlightBooking
from apps.bookings.models import Booking
from apps.payments.models import Payment
from apps.reports.models import Report


@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    total_revenue = (
        Payment.objects.filter(
            payment_status="success"
        ).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0.00")
    )

    data = {
        "total_users": User.objects.count(),
        "total_destinations": Destination.objects.count(),
        "total_hotels": Hotel.objects.count(),
        "total_rooms": Room.objects.count(),
        "total_flights": Flight.objects.count(),
        "total_flight_bookings": FlightBooking.objects.count(),
        "total_hotel_bookings": Booking.objects.count(),
        "total_payments": Payment.objects.count(),
        "total_reports": Report.objects.count(),
        "total_revenue": total_revenue,
    }

    return Response(data)