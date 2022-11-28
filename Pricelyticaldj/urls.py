"""Pricelyticaldj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from analysis.views import view_analysis_list
from Pricelyticaldj.views import send_mail_view

urlpatterns = [
    #html pages
    path('admin/', admin.site.urls),
    path('api/analysis/', include('analysis.urls')),
    path('accounts/', include('accounts.urls')),
    path('profile/', include('profiles.urls')),
    path('contact/', send_mail_view),
    path('api/search/', include('search.urls')),
    path('',view_analysis_list),

    
]
