from django.urls import path
from .views import profile_view, set_searches

urlpatterns = [
    path('set/searches/', set_searches),
    path('', profile_view),
    
]