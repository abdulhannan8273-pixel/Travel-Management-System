from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# HOTEL module----------------------------------------------------------------------------


class Hotel(models.Model):
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.CASCADE,
        related_name="hotels"
    )

    name = models.CharField(max_length=255)

    description = models.TextField()

    address = models.TextField()

    star_rating = models.DecimalField(
         max_digits=2,
        decimal_places=1,
        validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
        ],
)
   

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_rooms = models.PositiveIntegerField()

    available_rooms = models.PositiveIntegerField()

    check_in_time = models.TimeField()

    check_out_time = models.TimeField()

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
    )

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
# ROOM module---------------------------------------------------------------------------------------------------------


class Room(models.Model):
    ROOM_TYPES = [
        ("standard", "Standard"),
        ("deluxe", "Deluxe"),
        ("suite", "Suite"),
    ]

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES
    )

    description = models.TextField(blank=True)

    capacity = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_rooms = models.PositiveIntegerField()

    available_rooms = models.PositiveIntegerField()

    # 👇 Add these fields here
    room_number_prefix = models.CharField(
        max_length=20,
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["room_type"]

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"
    
#Hotel Image Module---------------------------------------------------------------------------------------------------------------
    
class HotelImage(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="hotels/"
    )

    is_cover = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.hotel.name} Image"




# Hotel Amenity module---------------------------------------------------------------------------------------------------------------


class HotelAmenity(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="amenities"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# Hotel Policy module----------------------------------------------------------------------------------------------------------------

class HotelPolicy(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="policies"
    )

    title = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.hotel.name} - {self.title}"