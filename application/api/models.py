from django.db import models

# Create your models here.
class IPLocation(models.Model):
    ip_network = models.CharField(max_length=50, primary_key=True, unique=True) 
    latitude = models.DecimalField(max_digits=6, decimal_places=2)
    longitude = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.ip_network