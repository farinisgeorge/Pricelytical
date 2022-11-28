from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


User = settings.AUTH_USER_MODEL
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user')
    location = models.CharField(max_length=220, null=True, blank=True)
    hotelBased_searches = models.IntegerField(default=10, null=True, blank=True)
    last_hotelBased_purchase = models.DateTimeField(null=True, blank=True)
    perimeterBased_searches = models.IntegerField(default=10, null=True, blank=True)
    last_perimeterBased_purchase = models.DateTimeField(null=True, blank=True)


def user_did_save(sender, instance, created,*args,**kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save,sender=User)