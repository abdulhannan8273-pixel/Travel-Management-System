from decimal import Decimal

from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.accounts.models import User
from apps.destinations.models import Destination
from apps.hotels.models import Hotel, Room
from apps.flights.models import Flight, FlightBooking
from apps.bookings.models import Booking
from apps.packages.models import Package
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

    # Combined count across both booking types — the plan asks for one
    # "Total Bookings" figure, not separate destination/flight numbers.
    total_bookings = Booking.objects.count() + FlightBooking.objects.count()

    # Now computed from REAL booking data, since Booking has a `package`
    # field — not just is_featured/rating like Package's own /popular/ action.
    popular_packages = list(
        Package.objects.annotate(booking_count=Count("bookings"))
        .filter(booking_count__gt=0)
        .order_by("-booking_count")[:5]
        .values("id", "name", "booking_count")
    )

    recent_bookings = list(
        Booking.objects.select_related("user", "destination", "package")
        .order_by("-created_at")[:10]
        .values(
            "id", "user__email", "destination__name", "package__name",
            "status", "total_price", "created_at",
        )
    )

    pending_payments = Payment.objects.filter(payment_status="pending").count()

    data = {
        "total_users": User.objects.count(),
        "total_destinations": Destination.objects.count(),
        "total_hotels": Hotel.objects.count(),
        "total_rooms": Room.objects.count(),
        "total_flights": Flight.objects.count(),
        "total_bookings": total_bookings,
        "total_payments": Payment.objects.count(),
        "total_reports": Report.objects.count(),
        "total_revenue": total_revenue,
        "pending_payments": pending_payments,
        "popular_packages": popular_packages,
        "recent_bookings": recent_bookings,
    }

    return Response(data)