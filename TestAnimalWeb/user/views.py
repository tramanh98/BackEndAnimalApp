from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User
from .serializers import UserSerializer, AvatarSerializer
from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, )
from rest_framework.decorators import api_view
from rest_framework import serializers

from rest_framework.authtoken.models import Token

class MyProfile(APIView):

    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(seft, request, *args, **kwargs):    # lấy thông tin cá nhân ( first name, last name, email, phone)
        print(request.user.id)
        user = get_object_or_404(User, pk = request.user.id)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @csrf_exempt
    def put(seft, request, *args, **kwargs):
        profile = get_object_or_404(User, pk = request.user.id)
        data = request.data.get('userprofile')
        serializer = UserSerializer(instance=profile, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile_saved = serializer.save()
        return Response({"success": "Success", "data" : serializer.data})



class AvatarUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def put(seft, request, *args, **kwargs):
        userObj = get_object_or_404(User, pk = request.user.id)
        data = request.data.get('avatar')
        print(data)
        serializer = AvatarSerializer(instance=userObj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile_saved = serializer.save()
        return Response({"success": "Success", "data" : serializer.data})


class ProfileUpdateDeleteAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView): 
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self): 
        query = User.objects.filter(pk = self.request.user.id)
        return query
