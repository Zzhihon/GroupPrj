from django.urls import path
from demo.views import getprofile, GetTrade, GetReview
from demo import views

urlpatterns = [
    path('getprofile/', getprofile.as_view(), name="getprofiles"),
    path('gettrade/', GetTrade.as_view(), name='gettrade'),
    path('getReview/', GetReview.as_view(), name="getreview"),
    path('test/', views.index, name="test"),
]