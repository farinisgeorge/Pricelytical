from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

@api_view(['POST'])
@parser_classes([JSONParser])
# TODO get email variables in safe place
def send_mail_view(request,*args,**kwargs):
    mail_data = request.data  #name, locality, country
    send_mail(
    "(" + mail_data['fullname']+") " + mail_data['subject'],
    mail_data['message'],
    mail_data['from_mail'],
    ['gefofar@gmail.com'],
    fail_silently=False,
)
    return Response(status=status.HTTP_200_OK)