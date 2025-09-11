from django.db import models


class Address(models.Model):
    gml_id = models.CharField(max_length=255, unique=True)
    street_name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    geometry = models.TextField()  # Store WKT or GeoJSON

    class Meta:
        indexes = [
            models.Index(fields=["street_name", "house_number"]),
            models.Index(fields=["postal_code"]),
            models.Index(fields=["district"]),
        ]

    def __str__(self):
        return f"{self.street_name} {self.house_number}, {self.postal_code} Berlin"
