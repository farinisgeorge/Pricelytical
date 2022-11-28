from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from .models import Analysis, HotelBased, PerimeterBased
from profiles.models import Profile
from .serializers import AnalysisSerializer, HotelBasedSerializer, PerimeterBasedSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_analysis_list(request, *args, **kwargs):
    qs=Analysis.objects.filter(user=request.user).order_by('-id')
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    serializer = AnalysisSerializer(qs,many=True)
    data= serializer.data
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_hotelBased_analysis(request, analysis_id, *args, **kwargs):
    qs=HotelBased.objects.filter(analysis_details__id=analysis_id)
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    serializer = HotelBasedSerializer(qs,many=True)
    data= serializer.data
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_perimeterBased_analysis(request, analysis_id, *args, **kwargs):
    qs=PerimeterBased.objects.filter(analysis_details__id=analysis_id)
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    serializer = PerimeterBasedSerializer(qs,many=True)
    data= serializer.data
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def create_Analysis_hotelbased(request, *args, **kwargs):
    data=request.data
    data.update({
        'plotdata' : [
        {
            "title" : "Average Price for every search engine.",
            "Text"  : "The average price for the given hotels, in each search engine.",
            "data"     : [{'x':'Booking.com', 'y':128}, {'x':'Agoda.com', 'y':130} , {'x':'AirBnB', 'y':120}, {'x':'Trip.com', 'y':150}, {'x':'Expedia', 'y':140}],
        },
        {
            "title" : "Maximum and Minimum price.",
            "Text"  : "Maximum and Minimum price of every search engine.",
            "x"     : ['Booking.com', 'Agoda.com', 'AirBnB', 'Trip.com', 'Expedia'],
            "y1"     : [162, 160, 140, 200, 260],
            "y2"     : [110, 100, 100, 100, 150],
        },
        {
            "title" : "Average hotel price",
            "Text"  : "Average hotel price for all of the search engines.",
            "x"     : ['Hotel 1', 'Hotel 2', 'Hotel 3', 'Hotel 4', 'Hotel 5'],
            "y"     : [130, 160, 190, 145, 200],
            
        },
        {
            "title" : "Hotel price.",
            "Text"  : "Hotel price for all of the search engines",
            "x"     : ['Booking.com', 'Agoda.com', 'AirBnB', 'Trip.com', 'Expedia'],
            "h1"     : [130, 140, 135, 156, 200],
            "h2"     : [146, 158, 149, 200, 210],
            "h3"     : [110, 100, 156, 170, 160],
            "h4"     : [120, 125, 110, 160, 140],
        },
    ]})

    
    qs = Profile.objects.get(user=request.user)
    if qs and qs.hotelBased_searches > 0:
        qs.hotelBased_searches = qs.hotelBased_searches - 1
        qs.save()
        serializer = HotelBasedSerializer(data=data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def create_Analysis_perimeterbased(request, *args, **kwargs):
    data = request.data
    data.update({
        'plotdata' : [
        {
            "title" : "Average Price for every search engine.",
            "Text"  : "The average price for the given hotels, in each search engine.",
            "x"     : [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6],
            "se1"     : [128, 130, 120, 150, 140, 130, 120, 120, 125, 160, 180, 200],
            "se2"     : [140, 145, 147, 150, 130, 120, 100, 140, 137, 135, 150, 210],
            "se3"     : [150, 147, 100, 105, 110, 115, 150, 130, 180, 190, 140, 100],
        },
        {
            "title" : "Maximum and Minimum price.",
            "Text"  : "Maximum and Minimum price of every search engine.",
            "x"     : ['Booking.com', 'Agoda.com', 'AirBnB', 'Trip.com', 'Expedia'],
            "y1"     : [162, 160, 140, 200, 260],
            "y2"     : [110, 100, 100, 100, 150],
        },
        {
            "title" : "Prices for Booking.com",
            "Text"  : "Prices for the given perimeter in Booking.com",
            "x"     : [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6],
            "hotels"     : [{'hotel' : 'Hotel 1', 'dist' : 1.2, 'price' : 156},
                            {'hotel' : 'Hotel 2', 'dist' : 3, 'price' : 170},
                            {'hotel' : 'Hotel 3', 'dist' : 3.8, 'price' : 174},
                            {'hotel' : 'Hotel 4', 'dist' : 5.2, 'price' : 178}],
        },
        {
            "title" : "Prices for Agoda.com",
            "Text"  : "Prices for the given perimeter in Booking.com",
            "x"     : [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6],
            "hotels"     : [{'hotel' : 'Hotel 1', 'dist' : 1.2, 'price' : 156},
                            {'hotel' : 'Hotel 2', 'dist' : 3, 'price' : 170},
                            {'hotel' : 'Hotel 3', 'dist' : 3.8, 'price' : 174},
                            {'hotel' : 'Hotel 4', 'dist' : 5.2, 'price' : 178}],
        },
        {
            "title" : "Prices for Expedia.com",
            "Text"  : "Prices for the given perimeter in Booking.com",
            "x"     : [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6],
            "hotels"     : [{'hotel' : 'Hotel 1', 'dist' : 1.2, 'price' : 156},
                            {'hotel' : 'Hotel 2', 'dist' : 3, 'price' : 170},
                            {'hotel' : 'Hotel 3', 'dist' : 3.8, 'price' : 174},
                            {'hotel' : 'Hotel 4', 'dist' : 5.2, 'price' : 178}],
        },
        {
            "title" : "Average Price.",
            "Text"  : "The average price for the given hotels, based on the distance.",
            "x"     : [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6],
            "y"     : [128, 130, 120, 150, 140, 130, 120, 120, 125, 160, 180, 200],
            
        },
    ]})
    
    qs = Profile.objects.get(user=request.user)
    if qs and qs.perimeterBased_searches > 0:
        qs.perimeterBased_searches = qs.perimeterBased_searches - 1
        qs.save()
        serializer = PerimeterBasedSerializer(data=data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({},status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def delete_analysis(request, *args, **kwargs):
    data = request.data
    qs=Analysis.objects.filter(user=request.user,id=data['id'])
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    qs.delete()
    return Response(status=status.HTTP_200_OK)

