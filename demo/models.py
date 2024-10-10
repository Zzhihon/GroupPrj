from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

# Create your models here.

class Profile(models.Model):
    """用户信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    student_id = models.IntegerField(validators=[
            MaxValueValidator(1e11),
            MinValueValidator(1e10)
        ], null = True, blank=True)
    student_class = models.CharField(max_length=50, null=True, blank=True)    
    email = models.EmailField(max_length=100, null=True, blank=True)
    contact = models.IntegerField(validators=[
            MaxValueValidator(1e11),
            MinValueValidator(1e10)
        ], null = True, blank=True)    
    facauty = models.CharField(max_length=30, null=True, blank=True)
    dormitory = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return str(self.username)

class Item(models.Model):
    """物品"""
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    count = models.IntegerField(validators=[
            MaxValueValidator(1e6),
            MinValueValidator(1)
        ], default=1, null = True, blank=True)
    price = models.IntegerField(validators=[
            MaxValueValidator(1e6),
            MinValueValidator(1)
        ], default=1, null = True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class ReviewForTrade(models.Model):
    """交易评论"""
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
   
    def __str__(self):
        result = f"{self.owner.username} comment"
        return result


class Trade(models.Model):
    users = User.objects.all()
    Users = tuple((user.username, user.username) for user in users)
    Users += (('', '---------'),)

    """交易实例"""
    States = (
        ('Code_0', '撤销'),
        ('Code_1', '初始化'),
        ('Code_2', '购买'),
        ('Code_3', '出售'),
        ('Code_4', '拒绝'),
        ('Code_5', '完成')
    )
    seller = models.ForeignKey(Profile,related_name='seller', on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(Profile,related_name='buyer', on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    review = models.OneToOneField(ReviewForTrade, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50, default='Code_3', choices=States)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  
    unReciveError = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Seller {self.seller.username}'s {self.item.name} Trade with {self.buyer}-------{self.state}"
    
class ReviewForItem(models.Model):
    """物品留言"""
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
   
    def __str__(self):
        result = f"{self.owner.username} comment"
        return result

class ChatRoom(models.Model):
    """聊天室"""
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    trade = models.OneToOneField(Trade, on_delete=models.CASCADE,related_name="chat_room")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"聊天室({', '.join([user.username for user in self.participants.all()])})"

class Message(models.Model):
    """聊天记录"""
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE,null=True)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)
    content = models.TextField(null=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
