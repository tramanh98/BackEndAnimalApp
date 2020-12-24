from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer, AvatarSerializer, CustomRegisterSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, )

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
        data = request.data.get('profileUpdate')
        serializer = UserSerializer(instance=profile, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile_saved = serializer.save()
        return Response(serializer.data)



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
        return Response(serializer.data)


# class ProfileUpdateDeleteAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView): 
#     permission_classes = (IsAuthenticated,)
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get_queryset(self): 
#         query = User.objects.filter(pk = self.request.user.id)
#         return query
