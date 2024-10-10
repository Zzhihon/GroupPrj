from django.urls import path
from demo.views import getprofile, TradeView,TradePostView, GetReview,SearchUserView
from demo import views

urlpatterns = [
    path('getprofile/', getprofile.as_view(), name="getprofiles"),
    path('getprofile/<str:pk1>/',SearchUserView.as_view(), name='searchuser'),
    path('gettrade/<str:pk1>/<str:pk2>/', TradeView.as_view(), name='gettrade'),
    path('posttrade/', TradePostView.as_view()),
    path('getReview/', GetReview.as_view(), name="getreview"),
    path("itempage/", views.ItemPage),
    path('test/', views.index, name="test"),
]
