from rest_framework import serializers
from .models import Image

class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = Image
        fields = ('id','image')