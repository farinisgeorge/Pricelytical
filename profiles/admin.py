from django.contrib import admin

from .models import Profile


class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['__str__','user']
    search_fields = ['id','user__username','user__email','location','hotelBased_searches','last_hotelBased_purchase','perimeterBased_searches','last_hotelBased_purchase']
    class Meta:
        model = Profile

admin.site.register(Profile, ProfilesAdmin)

