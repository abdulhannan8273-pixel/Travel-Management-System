from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]

    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)

    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Caps the discount for percentage coupons. Leave blank for no cap.",
    )
    min_booking_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    usage_limit = models.PositiveIntegerField(
        null=True, blank=True, help_text="Leave blank for unlimited use."
    )
    used_count = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "coupons"
        ordering = ["-created_at"]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.upper().strip()
        super().save(*args, **kwargs)

    def is_valid_now(self):
        now = timezone.now()
        if not self.is_active:
            return False, "This coupon is not active."
        if now < self.valid_from:
            return False, "This coupon is not active yet."
        if now > self.valid_until:
            return False, "This coupon has expired."
        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return False, "This coupon has reached its usage limit."
        return True, ""

    def calculate_discount(self, amount):
        if amount < self.min_booking_amount:
            return None, f"Minimum booking amount for this coupon is {self.min_booking_amount}."

        if self.discount_type == "percentage":
            discount = (amount * self.discount_value) / 100
            if self.max_discount_amount is not None:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value

        discount = min(discount, amount)
        return discount, ""