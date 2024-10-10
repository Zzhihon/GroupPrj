from django.urls import path, include


urlpatterns = [
    path('profiles/', include('demo.urls.profiles.index')),
    path('', include('demo.urls.settings.index')),

]
