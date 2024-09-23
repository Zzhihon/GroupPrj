from django.contrib import admin
from .models import Profile, Item, Trade, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Trade)
admin.site.register(Review)