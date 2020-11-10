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

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone','email', 'avatar')
        read_only_fields = ('email', )
        # exclude = ('password',)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        return instance