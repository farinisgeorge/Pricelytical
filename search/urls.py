from django.urls import path
from .views import hotelsearch_view

urlpatterns = [
    path('hotel/', hotelsearch_view),
]