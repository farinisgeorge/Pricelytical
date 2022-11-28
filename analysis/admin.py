from django.contrib import admin

from .models import Analysis, HotelBased, PerimeterBased


class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['__str__','user']
    search_fields = ['id','user__username','user__email', 'name','date_created','rooms','adults','children','checkin_date','checkout_date']
    class Meta:
        model = Analysis

admin.site.register(Analysis, AnalysisAdmin)


class HotelBasedAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['analysis_details','hotels','plotdata']
    class Meta:
        model = HotelBased

admin.site.register(HotelBased, HotelBasedAdmin)


class PerimeterBasedAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['analysis_details','startpoint_lat','startpoint_lon','perimeter','stars_min','stars_max','cust_rating_min','cust_rating_max','plotdata']
    class Meta:
        model = PerimeterBased

admin.site.register(PerimeterBased, PerimeterBasedAdmin)