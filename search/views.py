from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from .models import Hotels
from .serializers import HotelSerializer
from django.db.models import Q
from functools import reduce
from operator import or_



@api_view(['POST'])
@parser_classes([JSONParser])
# @permission_classes([IsAuthenticated])
def hotelsearch_view(request, *args, **kwargs):
    search_data = request.data['searchstring'].split(',')   #name, locality, country
    search_data.append(request.data['searchstring'])
    search_data = [elem for elem in search_data if elem != ""]
    query = reduce(or_, (Q(name__icontains=sd)|Q(locality__icontains=sd)|Q(country__icontains=sd) for sd in search_data))
    qs = Hotels.objects.filter(query)

    # qs = Hotels.objects.all()
    
    if not qs.exists():
        return Response({},status=status.HTTP_404_NOT_FOUND)
    serializer = HotelSerializer(qs,many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)