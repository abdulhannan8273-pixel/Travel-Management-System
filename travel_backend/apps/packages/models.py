from django.db import models
from django.utils.text import slugify
from apps.destinations.models import Destination


class Package(models.Model):
    Destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    overview = models.CharField(max_length=500, blank=True, help_text="Short summary shown in listings/search results.")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Optional sale price. Leave blank if there's no discount.",
    )
    duration = models.PositiveIntegerField(help_text="Duration in days")
    max_persons = models.PositiveIntegerField(default=1)
    cover_image = models.ImageField(upload_to="packages/", blank=True, null=True)

    itinerary = models.TextField(blank=True, help_text="Day-by-day plan")
    included = models.TextField(blank=True, help_text="One item per line")
    excluded = models.TextField(blank=True, help_text="One item per line")
    cancellation_policy = models.TextField(blank=True)
    terms = models.TextField(blank=True, help_text="Terms & conditions for this package.")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "packages"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Package.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="packages/gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "package_images"
        ordering = ["id"]

    def __str__(self):
        return f"{self.package.name} Image"


class PackageVideo(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="videos")
    video_url = models.URLField(help_text="YouTube/Vimeo link or direct video file URL.")
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "package_videos"
        ordering = ["id"]

    def __str__(self):
        return f"{self.package.name} Video"