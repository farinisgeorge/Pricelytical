from django.urls import path, include
from .views import ( create_Analysis_hotelbased, create_Analysis_perimeterbased,
                      view_hotelBased_analysis,view_perimeterBased_analysis, view_analysis_list,
                      delete_analysis)

urlpatterns = [

     #GET
    path('view-hotelbased/<int:analysis_id>', view_hotelBased_analysis),
    path('view-perimeterbased/<int:analysis_id>', view_hotelBased_analysis),
    path('list/', view_analysis_list),

    #POST
    path('create-analysis-hotelbased/', create_Analysis_hotelbased),
    path('create-analysis-perimeterbased/', create_Analysis_perimeterbased),

    #DELETE
    path('delete/',delete_analysis),
    
]