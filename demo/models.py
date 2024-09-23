from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

import uuid

# Create your models here.

class Profile(models.Model):
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
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    item = models.CharField(max_length=50, null=True, blank=True)
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
        return str(self.item)
    
class Review(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
   
    def __str__(self):
        result = f"{self.owner.username} comment"
        return result

class Trade(models.Model):
    States = (
        ('Code_0', '交易中'),
        ('Code_1', '交易成功'),
        ('Code_2', '交易取消'),
        ('Code_3', '等待交易'),
    )
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    review = models.OneToOneField(Review, on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.CharField(max_length=50, null=True, blank=True)
    state = models.IntegerChoices
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50, default='Code_3', choices=States)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  
    def __str__(self):
        return self.state


    

