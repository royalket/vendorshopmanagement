from django.db import models
from accounts.models import Vendor

class Shop(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']