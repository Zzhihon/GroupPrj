from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from demo.models import Profile, Item, Trade, ReviewForItem, ReviewForTrade
from demo.serializers import ProfileSerializer, TradeSerializer, ItemSerializer, ReviewForTradeSerializer

# Create your views here.
class getprofile(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, format=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class RegisterView(APIView):
    def post(self, request, format=None):
        data = request.POST
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        password_confirm = data.get("password_confirm", "").strip()
        email = data.get("email", "").strip()
        contact = data.get("contact", None)
        student_id = data.get("studen_id", None)
        student_class = data.get("student_class", "").strip()
        facauty = data.get("faculty", "").strip()
        dormitory = data.get("domitory", "").strip()   
        if not username or not password:
            return Response({
                'result': "用户名和密码不能为空"
            })
        if password != password_confirm:
            return Response({
                'result': "两个密码不一致",
            })
        if User.objects.filter(username=username).exists():
            return Response({
                'result': "用户名已存在"
            })
        user = User(username=username)
        user.set_password(password)
        user.save()

        profile = Profile.objects.create(user=user, username= username, email=email,
                    student_id = student_id, student_class = student_class,
                    facauty = facauty, dormitory = dormitory
                    )
        serializer = ProfileSerializer(profile, many=False)
        return Response({
            'result': "success",
            'username': profile.username,
            'profile': serializer.data

        })
        
class TradeView(APIView):
    permission_classes = ([IsAuthenticated])
    
    def get(self, request, pk1, pk2, format=None):
        user = request.user
        profile = user.profile
        trades = profile.seller.all()
        ztrade = None
        for trade in trades:
            if trade.buyer.username == pk1 and trade.item.name == pk2:
                ztrade = trade
        serializer = TradeSerializer(ztrade, many=False)
        return Response(serializer.data)


class TradePostView(APIView):

    def post(self, request, format=None):
        data = request.POST
        seller = data.get("seller", "").strip()
        buyer = data.get("buyer", "").strip()
        item = data.get("item", "").strip()
        seller = Profile.objects.get(username=seller)
        buyer = Profile.objects.get(username=buyer)
        item = Item.objects.get(name=item)
        trade = Trade.objects.create(seller=seller, buyer=buyer, item=item)
        serializer =  TradeSerializer(trade, many=False)
        return Response({
            'code': 'success',
        })
  

        
class GetReview(APIView):
    permission_classes = ([IsAuthenticated])
    
    def get(self, request, format=None):
        user = request.user
        profile = user.profile
        review = ReviewForTrade.objects.get(owner=profile)
        serializer = ReviewForTradeSerializer(review, many=False)
        return Response(serializer.data)
        
def LoginView(request):
    return render(request, 'login.html')

def index(request):
    users = User.objects.all()
    nested_tuple = tuple((user.username, user.username) for user in users)
    nested_tuple +=(('default', 'default'),)
    context = {
        'user': nested_tuple,
    }

    return render(request, "demo/web.html", context)

def SearchView(request):
    return render(request, 'search.html')


class SearchUserView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, pk, format=None):
        user_me = request.user
        users = User.objects.all()
        for user in users:
            if user.username == pk:
                return Response({
                    'user_me': user_me.profile,
                    'user_ant': user.profile
                })

def ItemPage(request):
    return render(request, 'item.html')





