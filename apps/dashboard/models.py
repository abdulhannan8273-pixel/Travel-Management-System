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


successful_payments = Payment.objects.filter(
    payment_status="success"
).count()




pending_payments = Payment.objects.filter(
    payment_status="pending"
).count()




failed_payments = Payment.objects.filter(
    payment_status="failed"
).count()



refunded_payments = Payment.objects.filter(
    payment_status="refunded"
).count()




active_flights = Flight.objects.filter(
    is_active=True
).count()




confirmed_bookings = Booking.objects.filter(
    status="confirmed"
).count()



cancelled_bookings = Booking.objects.filter(
    status="cancelled"
).count()




confirmed_flight_bookings = FlightBooking.objects.filter(
    booking_status="confirmed"
).count()

dashboard_metrics = {
    "successful_payments": successful_payments,
    "pending_payments": pending_payments,
    "failed_payments": failed_payments,
    "refunded_payments": refunded_payments,
    "active_flights": active_flights,
    "confirmed_bookings": confirmed_bookings,
    "cancelled_bookings": cancelled_bookings,
    "confirmed_flight_bookings": confirmed_flight_bookings,
}
