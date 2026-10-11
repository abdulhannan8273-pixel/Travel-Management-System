"""
Read-only, admin-only analytics endpoints.

Unlike the Report model (a manually-created record a user writes, e.g.
"Q3 performance notes"), these compute real numbers from live data every
time they're called — matching the plan's "Revenue / Booking / User /
Package Report" idea.
"""
from datetime import datetime

from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth

from apps.payments.models import Payment
from apps.bookings.models import Booking
from apps.flights.models import FlightBooking
from apps.accounts.models import User
from apps.packages.models import Package


def _parse_date_range(request):
    """?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD, both optional."""
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    start = None
    end = None
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    return start, end


def build_revenue_report(request):
    start, end = _parse_date_range(request)

    payments = Payment.objects.filter(payment_status="success")
    if start:
        payments = payments.filter(paid_at__date__gte=start)
    if end:
        payments = payments.filter(paid_at__date__lte=end)

    total_revenue = payments.aggregate(total=Sum("amount"))["total"] or 0

    by_payment_method = list(
        payments.values("payment_method")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    by_booking_type = {
        "destination_bookings": payments.filter(destination_booking__isnull=False).aggregate(
            total=Sum("amount"), count=Count("id")
        ),
        "flight_bookings": payments.filter(flight_booking__isnull=False).aggregate(
            total=Sum("amount"), count=Count("id")
        ),
    }

    monthly_trend = list(
        payments.annotate(month=TruncMonth("paid_at"))
        .values("month")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("month")
    )

    return {
        "total_revenue": total_revenue,
        "total_transactions": payments.count(),
        "by_payment_method": by_payment_method,
        "by_booking_type": by_booking_type,
        "monthly_trend": monthly_trend,
        "date_range": {"start": start, "end": end},
    }


def build_booking_report(request):
    start, end = _parse_date_range(request)

    destination_bookings = Booking.objects.all()
    flight_bookings = FlightBooking.objects.all()
    if start:
        destination_bookings = destination_bookings.filter(created_at__date__gte=start)
        flight_bookings = flight_bookings.filter(created_at__date__gte=start)
    if end:
        destination_bookings = destination_bookings.filter(created_at__date__lte=end)
        flight_bookings = flight_bookings.filter(created_at__date__lte=end)

    by_status = list(
        destination_bookings.values("status").annotate(count=Count("id")).order_by("-count")
    )
    by_flight_status = list(
        flight_bookings.values("booking_status").annotate(count=Count("id")).order_by("-count")
    )

    top_destinations = list(
        destination_bookings.values("destination__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    monthly_trend = list(
        destination_bookings.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    return {
        "total_destination_bookings": destination_bookings.count(),
        "total_flight_bookings": flight_bookings.count(),
        "destination_bookings_by_status": by_status,
        "flight_bookings_by_status": by_flight_status,
        "top_destinations": top_destinations,
        "monthly_trend": monthly_trend,
        "date_range": {"start": start, "end": end},
    }


def build_user_report(request):
    start, end = _parse_date_range(request)

    users = User.objects.all()
    new_users = users
    if start:
        new_users = new_users.filter(created_at__date__gte=start)
    if end:
        new_users = new_users.filter(created_at__date__lte=end)

    monthly_trend = list(
        users.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    return {
        "total_users": users.count(),
        "verified_users": users.filter(is_email_verified=True).count(),
        "unverified_users": users.filter(is_email_verified=False).count(),
        "new_users_in_range": new_users.count(),
        "monthly_trend": monthly_trend,
        "date_range": {"start": start, "end": end},
    }


def build_package_report(request):
    """
    Note: Bookings/Payments currently link to Destination, not Package, so
    per-package revenue or booking counts aren't available yet. This report
    is limited to package catalog stats until that link exists.
    """
    packages = Package.objects.select_related("Destination")

    by_destination = list(
        packages.values("Destination__name")
        .annotate(count=Count("id"), avg_price=Avg("price"))
        .order_by("-count")
    )

    return {
        "total_packages": packages.count(),
        "active_packages": packages.filter(is_active=True).count(),
        "featured_packages": packages.filter(is_featured=True).count(),
        "average_price": packages.aggregate(avg=Avg("price"))["avg"],
        "average_rating": packages.aggregate(avg=Avg("rating"))["avg"],
        "by_destination": by_destination,
        "note": "Per-package booking/revenue stats require linking Bookings to Package, which doesn't exist yet.",
    }