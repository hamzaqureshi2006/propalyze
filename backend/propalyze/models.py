from django.db import models

# Create your models here.
# app/models.py
from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    property_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    bhk = models.IntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=100, null=True, blank=True)  # Apartment, Villa, etc.
    developer = models.CharField(max_length=255, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    floor_current = models.IntegerField(null=True, blank=True)
    floor_total = models.IntegerField(null=True, blank=True)
    transaction_type = models.CharField(max_length=50, null=True, blank=True)  # New/Resale
    facing = models.CharField(max_length=50, null=True, blank=True)
    furnished_status = models.CharField(max_length=50, null=True, blank=True)
    ownership_type = models.CharField(max_length=50, null=True, blank=True)  # Freehold, Leasehold
    description = models.TextField(null=True, blank=True)

    # Location
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)

    # Sizes and Prices
    super_built_up_area = models.FloatField(null=True, blank=True)
    carpet_area = models.FloatField(null=True, blank=True)
    total_area = models.FloatField(null=True, blank=True)
    price_per_sqft = models.FloatField(null=True, blank=True)
    price_in_inr = models.FloatField(null=True, blank=True)
    property_yield = models.FloatField(null=True, blank=True)

    # Other details
    status = models.CharField(max_length=100, null=True, blank=True)  # Ready to move, Under construction
    parking_count = models.IntegerField(null=True, blank=True)
    parking_type = models.CharField(max_length=50, null=True, blank=True)
    property_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.locality})"


class HistoricalPrice(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="historical_prices")
    month = models.CharField(max_length=20)  # e.g. "Aug'24"
    price = models.FloatField()

    def __str__(self):
        return f"{self.property.name} - {self.month}"


class LocalityRating(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="locality_rating")
    connectivity = models.FloatField(null=True, blank=True)
    safety = models.FloatField(null=True, blank=True)
    traffic = models.FloatField(null=True, blank=True)
    environment = models.FloatField(null=True, blank=True)
    market = models.FloatField(null=True, blank=True)
    area_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Locality Rating for {self.property.name}"


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="photos")
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return f"Photo of {self.property.name}"


class LocalityPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="locality_photos")
    image_url = models.URLField(max_length=500)

    def __str__(self):
        return f"Locality photo of {self.property.locality}"


class SavedProperty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_properties")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.property.name}"
