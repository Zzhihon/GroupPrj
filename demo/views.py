from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from demo.models import Profile, Item, Trade, Review
from demo.serializers import ProfileSerializer, TradeSerializer, ItemSerializer, ReviewSerializer

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
        
class GetTrade(APIView):
    permission_classes = ([IsAuthenticated])
    
    def get(self, request, format=None):
        user = request.user
        profile = user.profile
        trade = Trade.objects.get(seller=profile)
        serializer = TradeSerializer(trade, many=False)
        return Response(serializer.data)
        
class GetReview(APIView):
    permission_classes = ([IsAuthenticated])
    
    def get(self, request, format=None):
        user = request.user
        profile = user.profile
        review = Review.objects.get(owner=profile)
        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data)
        

    

def index(request):
    data = request.GET
    context = {
        'theme': data.get('theme', "qweasd"),
        'refresh': data.get('refresh', "qweasd"),
        'data': data,
    }

    return render(request, "demo/web.html", context)



