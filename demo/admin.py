from django.contrib import admin
from .models import Profile, Item, Trade, ReviewForItem, ReviewForTrade, ChatRoom, Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(Trade)
admin.site.register(ReviewForItem)
admin.site.register(ReviewForTrade)
admin.site.register(ChatRoom)
admin.site.register(Message)
