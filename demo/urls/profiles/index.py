from django.urls import path, include
from demo.views import getprofiles

urlpatterns = [
    path('getprofiles/', getprofiles.as_view(), name="getprofiles"),

]