from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth import models

import json

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import generics

from authentication.models import UserAccount, UserInfo
from authentication.serializers import UserAccountSerializer, UserInfoSerializer

class UserInfoCRUD:
    class Create(generics.CreateAPIView):
        queryset = UserInfo.objects.all()
        serializer_class = UserInfoSerializer

class UserAccountCRUD:
    class Create(generics.CreateAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer
        permission_classes = (permissions.AllowAny, )
        
    class Update(generics.UpdateAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer
        permission_classes = (permissions.AllowAny, )
        
    # class Delete(generics.DeleteAPIView):
    #     queryset = UserAccount.objects.all()
    #     serializer_class = UserAccountSerializer
    #     permission_classes = (permissions.AllowAny, )
    
    class List(generics.ListAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer

# Create your views here.
class UserAuthentication(APIView):
    def get(self, request):
        return Response({'ok': 200})
    
    @api_view(['GET', 'POST'])
    def login(request):
        if request.method == 'POST':
            body_data = json.loads(request.body)
            
            user = auth.authenticate(username=body_data["username"], password=body_data["password"])
            
            if user != None:            
                auth.login(request, user)
                
                return JsonResponse({"status": 200})
            else:
                return JsonResponse({"status": 500})