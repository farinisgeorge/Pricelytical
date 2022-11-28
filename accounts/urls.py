from django.urls import path, include
from .views import current_user, UserList, logout_view
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [

    #Need to include Authentication token in headers
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('current-user/', current_user),
    path('signup/', UserList.as_view()),
    path('logout/', logout_view),

]