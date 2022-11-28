from django.contrib import admin

from .models import Hotels

class HotelsAdmin(admin.ModelAdmin):
    list_display = ['__str__','id','hotel_id','name','locality','country','details']
    search_fields = ['id','hotel_id','name','locality','country','details']
    class Meta:
        model = Hotels
        
admin.site.register(Hotels, HotelsAdmin)