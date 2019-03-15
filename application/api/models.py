from django.db import models

# Create your models here.
class IPLocation(models.Model):
    ip_network = models.CharField(max_length=50) 
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)