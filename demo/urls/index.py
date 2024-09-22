from django.urls import path, include


urlpatterns = [
    path('profiles/', include('demo.urls.profiles.index')),
    path('authenticate/', include('demo.urls.settings.index')),

]