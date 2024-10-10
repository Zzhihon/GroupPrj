from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Item, Trade, ReviewForTrade, ReviewForItem,Message


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields ='__all__'
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('owner', 'id',)

class ReviewForTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewForTrade
        exclude = ('owner', 'id')

class TradeSerializer(serializers.ModelSerializer):
    seller = ProfileSerializer(many=False)
    buyer = ProfileSerializer(many=False)
    item = ItemSerializer(many=False)
    review = ReviewForTradeSerializer(many=False)
    class Meta:
        model = Trade
        fields = '__all__'

    
class MessageSerializer(serializers.ModelSerializer):
    """消息记录序列化模型"""
    trade = TradeSerializer(many=False)
    sender = ProfileSerializer(many=False)
    
    class Meta:
        model = Message
        fields = ('trade','sender','content')

        
