import json
from django.core.management.base import BaseCommand
from propalyze.models import Property, HistoricalPrice, LocalityRating, PropertyPhoto, LocalityPhoto


class Command(BaseCommand):
    help = "Insert properties from a cleaned JSON file into the database (one-time load)"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        file_path = options["json_file"]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file: {e}"))
            return

        for item in data:
            # Create property
            property_obj = Property.objects.create(
                property_id=item["property_id"],
                name=item.get("name"),
                bhk=item.get("bhk"),
                property_type=item.get("property_type"),
                developer=item.get("developer"),
                project=item.get("project"),
                floor_current=item.get("floor_current"),
                floor_total=item.get("floor_total"),
                transaction_type=item.get("transaction_type"),
                facing=item.get("facing"),
                furnished_status=item.get("furnished_status"),
                ownership_type=item.get("ownership_type"),
                description=item.get("description"),
                latitude=item.get("latitude"),
                longitude=item.get("longitude"),
                locality=item.get("locality"),
                region=item.get("region"),
                super_built_up_area=item.get("super_built_up_area"),
                carpet_area=item.get("carpet_area"),
                total_area=item.get("total_area"),
                price_per_sqft=item.get("price_per_sqft"),
                price_in_inr=item.get("price_in_inr"),
                property_yield=item.get("property_yield"),
                status=item.get("status"),
                parking_count=item.get("parking_count"),
                parking_type=item.get("parking_type"),
                property_url=item.get("property_url"),
            )

            # Historical Prices
            for hp in item.get("historical_prices", []):
                HistoricalPrice.objects.create(
                    property=property_obj,
                    month=hp["month"],
                    price=hp["price"]
                )

            # Locality Rating
            if "locality_rating" in item:
                LocalityRating.objects.create(
                    property=property_obj,
                    connectivity=item["locality_rating"].get("connectivity"),
                    safety=item["locality_rating"].get("safety"),
                    traffic=item["locality_rating"].get("traffic"),
                    environment=item["locality_rating"].get("environment"),
                    market=item["locality_rating"].get("market"),
                    area_description=item["locality_rating"].get("area_description"),
                )

            # Property Photos
            for url in item.get("photos", []):
                PropertyPhoto.objects.create(property=property_obj, image_url=url)

            # Locality Photos
            for url in item.get("locality_photos", []):
                LocalityPhoto.objects.create(property=property_obj, image_url=url)

            self.stdout.write(self.style.SUCCESS(f"Inserted {property_obj.name}"))
