from rest_framework import serializers
from .models import User

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar', )

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance



class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'phone','email', 'avatar', 'posts')
        read_only_fields = ('email', 'posts' )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.phone = validated_data.get('avatar', instance.avatar)

        instance.save()
        return instance