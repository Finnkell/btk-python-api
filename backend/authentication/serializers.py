from rest_framework import serializers
from .models import *

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('city','state', 'street', 'neighbourhood', 'age')

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('cpf','password', 'username', 'email', 'phone', 'user_info')
        extra_kwargs = {'password': {'write_only': True}}