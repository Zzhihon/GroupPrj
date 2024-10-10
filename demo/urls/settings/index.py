from django.urls import path
from demo.views import RegisterView
from demo import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name = 'register'),
    path('login/', views.LoginView, name='login'),
    path('search/', views.SearchView, name='search'),
    ]
