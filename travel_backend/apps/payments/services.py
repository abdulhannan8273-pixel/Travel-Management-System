"""
Shared payment status-transition logic.

Both the manual PaymentViewSet actions (success/failed/refund) and the
Razorpay webhook call these same functions, so the booking-confirmation
and notification logic only lives in one place.
"""
from django.utils import timezone
from apps.notifications.models import Notification


def mark_payment_success(payment, razorpay_payment_id=None):
    """Returns True if the payment was moved to 'success', False if it already was."""
    if payment.payment_status == "success":
        return False

    payment.payment_status = "success"
    payment.paid_at = timezone.now()
    update_fields = ["payment_status", "paid_at"]

    if razorpay_payment_id:
        payment.razorpay_payment_id = razorpay_payment_id
        update_fields.append("razorpay_payment_id")

    payment.save(update_fields=update_fields)

    if payment.destination_booking:
        payment.destination_booking.status = "confirmed"
        payment.destination_booking.save(update_fields=["status"])

    if payment.flight_booking:
        payment.flight_booking.booking_status = "confirmed"
        payment.flight_booking.payment_status = True
        payment.flight_booking.save(update_fields=["booking_status", "payment_status"])

    Notification.objects.create(
        user=payment.user,
        title="Payment Successful",
        message=f"Your payment ({payment.transaction_id}) was completed successfully.",
    )
    return True


def mark_payment_failed(payment):
    """Returns True if the payment was moved to 'failed', False if it already was."""
    if payment.payment_status == "failed":
        return False

    payment.payment_status = "failed"
    payment.save(update_fields=["payment_status"])

    if payment.flight_booking:
        payment.flight_booking.booking_status = "cancelled"
        payment.flight_booking.payment_status = False
        payment.flight_booking.save(update_fields=["booking_status", "payment_status"])

    Notification.objects.create(
        user=payment.user,
        title="Payment Failed",
        message=f"Your payment ({payment.transaction_id}) has failed.",
    )
    return True


def mark_payment_refunded(payment):
    """Returns True if the payment was moved to 'refunded', False if it wasn't eligible."""
    if payment.payment_status != "success":
        return False

    payment.payment_status = "refunded"
    payment.paid_at = None
    payment.save(update_fields=["payment_status", "paid_at"])

    if payment.destination_booking:
        payment.destination_booking.status = "cancelled"
        payment.destination_booking.save(update_fields=["status"])

    if payment.flight_booking:
        flight_booking = payment.flight_booking
        flight_booking.booking_status = "cancelled"
        flight_booking.payment_status = False
        flight_booking.flight.available_seats += flight_booking.passengers
        flight_booking.flight.save(update_fields=["available_seats"])
        flight_booking.save(update_fields=["booking_status", "payment_status"])

    Notification.objects.create(
        user=payment.user,
        title="Payment Refunded",
        message=f"Your payment ({payment.transaction_id}) has been refunded.",
    )
    return True