from decimal import Decimal
from django.db import models
from apps.locations.models import Country, State, City
# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="destinations")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="destinations")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destinations")



    description = models.TextField()
    image = models.ImageField(upload_to="destinations/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=Decimal("0.0"))
    best_time_to_visit = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    weather = models.CharField(max_length=100, blank=True, default="")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, default="")
    language = models.CharField(max_length=100, blank=True, default="")
    timezone = models.CharField(max_length=100, blank=True, default="")
    popular_attractions = models.TextField(blank=True, help_text="Separate attractions with commas")
    travel_tips = models.TextField(blank=True)
    average_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    class Meta:
        db_table = "destinations"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="destinations/gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "destination_images"

    def __str__(self):
        return f"{self.destination.name} Image"


class Attraction(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="attractions")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="attraction/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "attractions"

    def __str__(self):
        return self.name