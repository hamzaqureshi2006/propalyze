from django.contrib import admin
from .models import *
# Register your models here.
for model in [Property, HistoricalPrice, LocalityRating, PropertyPhoto, LocalityPhoto, SavedProperty]:
    admin.site.register(model)