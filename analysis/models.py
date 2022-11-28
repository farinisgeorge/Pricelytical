from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
User=settings.AUTH_USER_MODEL


class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    date_created = models.DateTimeField(auto_now_add=True)
    rooms = models.IntegerField(default=0)
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    hotelBased = models.BooleanField()
    perimeterBased = models.BooleanField()


class HotelBased(models.Model):
    analysis_details = models.ForeignKey(Analysis,on_delete=models.CASCADE)
    hotels = JSONField()
    plotdata = JSONField(blank=True, null=True)

class PerimeterBased(models.Model):
    analysis_details = models.ForeignKey(Analysis,on_delete=models.CASCADE)
    startpoint_lat = models.FloatField()
    startpoint_lon = models.FloatField()
    perimeter = models.FloatField()
    stars_min = models.FloatField()
    stars_max = models.FloatField()
    cust_rating_min = models.FloatField()
    cust_rating_max = models.FloatField()
    plotdata = JSONField(blank=True, null=True)


