from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer
import datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request, *args, **kwargs):
    qs=Profile.objects.filter(user=request.user)
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    serializer = ProfileSerializer(qs,many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def set_searches(request, *args, **kwargs):
    qs = Profile.objects.get(user=request.user)
    
    if not qs:
        return Response({},status=status.HTTP_400_BAD_REQUEST)

    qs.hotelBased_searches = qs.hotelBased_searches + request.data['hotelBased_searches']
    qs.last_hotelBased_purchase = datetime.datetime.now().isoformat()
    qs.perimeterBased_searches = qs.perimeterBased_searches + request.data['perimeterBased_searches']
    qs.last_perimeterBased_purchase = datetime.datetime.now().isoformat()
    qs.save()
    return Response({},status=status.HTTP_201_CREATED)
    

