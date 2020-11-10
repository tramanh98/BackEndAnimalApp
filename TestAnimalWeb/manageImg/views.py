from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
from django.contrib.auth import decorators, authenticate, login
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from .models import Image
from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, )

from django.views.decorators.csrf import csrf_exempt
from .serializers import PhotoSerializer
from rest_framework import generics

from rest_framework import parsers
from django.http import QueryDict

from django.http import Http404
from rest_framework.views import APIView

# Create your views here.
class PhotoUploadView(APIView): # upload ảnh bài đăng 
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = PhotoSerializer(data= request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhotoDelete(generics.DestroyAPIView): # Xóa ảnh (nếu có) của bài đăng khi update
    serializer_class = PhotoSerializer
    def get_queryset(self):
        img_query = Image.objects.get(pk = pk)
        return img_query