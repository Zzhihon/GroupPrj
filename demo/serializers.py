from rest_framework import serializers
from .models import Profile, Item, Trade, Review

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('id',)
        
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('owner', 'id',)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('owner', 'id')

class TradeSerializer(serializers.ModelSerializer):
    seller = ProfileSerializer(many=False)
    item = ItemSerializer(many=False)
    review = ReviewSerializer(many=False)
    class Meta:
        model = Trade
        fields = '__all__'
        
