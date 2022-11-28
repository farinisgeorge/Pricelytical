from rest_framework import serializers
from .models import Hotels

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotels
        fields = ['id','hotel_id','name','locality','country','details']
