from django.db import models

class Hotels(models.Model):
    hotel_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    details = models.CharField(blank=True, null=True,max_length=255)

    def __str__(self):
        return '%s, %s, %s' %(self.name, self.locality, self.country)