from rest_framework import serializers
from .models import Analysis, HotelBased, PerimeterBased
from django.conf import settings


class AnalysisSerializer(serializers.ModelSerializer):
    # user_email = serializers.CharField(source='user.email')
    # user = AnalysisSerializerIn()
    class Meta:
        model = Analysis
        fields = ['id','name','date_created','rooms','adults','children','checkin_date','checkout_date','hotelBased','perimeterBased']



class HotelBasedSerializer(serializers.ModelSerializer):
    analysis_details = AnalysisSerializer()

    class Meta:
        model = HotelBased
        fields = ['analysis_details','hotels','plotdata']

    def create(self, validated_data):
        
        request = self.context['request']
        analysis_data = request.data.get('analysis_details')
        analysisnew = Analysis.objects.create(**analysis_data,user=request.user)
        
        
        passed_data=validated_data
        passed_data["analysis_details"]=analysisnew
        HotelBased.objects.create(**passed_data)
        return passed_data




class PerimeterBasedSerializer(serializers.ModelSerializer):
    analysis_details = AnalysisSerializer()
    class Meta:
        model = PerimeterBased
        fields = ['analysis_details','startpoint_lat','startpoint_lon','perimeter','stars_min','stars_max','cust_rating_min','cust_rating_max','plotdata']

    def create(self, validated_data):
        
        request = self.context['request']
        analysis_data = request.data.get('analysis_details')
        analysisnew = Analysis.objects.create(**analysis_data,user=request.user)
        
        
        passed_data=validated_data
        passed_data["analysis_details"]=analysisnew
        PerimeterBased.objects.create(**passed_data)
        return passed_data