from rest_framework import serializers
from .models import *

from django.contrib.auth import models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('city', 'state', 'street', 'neighbourhood', 'age')


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('cpf', 'password', 'username', 'email', 'phone', 'user_info')
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #     user = models.User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )

    #     user.set_password(validated_data['password'])
    #     user.save()

    #     return use
