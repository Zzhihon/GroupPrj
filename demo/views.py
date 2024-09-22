from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from demo.models import Profile
from demo.serializers import ProfileSerializer

# Create your views here.
class getprofiles(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request, format=None):
        user = request.user
        profile = Profile.objects.get(user=user)
        return Response({
            'result': "success",
            'username': profile.username,
            'email': profile.email,
        })


class RegisterView(APIView):
    def post(self, request, format=None):
        data = request.POST
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        password_confirm = data.get("password_confirm", "").strip()
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
        Profile.objects.create(user=user, email="")
        return Response({
            'result': "success",
            'username': username
        })





