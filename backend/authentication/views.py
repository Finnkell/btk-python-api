from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
from django.http import HttpRequest

from django.contrib import auth
from django.contrib.auth import login as auth_login

import json

from rest_framework import serializers
from rest_framework import permissions
from rest_framework import generics
from rest_framework import filters
from rest_framework import status

from authentication.models import UserAccount, UserInfo
from authentication.serializers import UserAccountSerializer, UserInfoSerializer


class UserInfoCRUD:
    class Create(generics.CreateAPIView):
        queryset = UserInfo.objects.all()
        serializer_class = UserInfoSerializer

        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)


class UserAccountCRUD:
    class Create(generics.CreateAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer
        permission_classes = (permissions.AllowAny, )

        def post(self, request, *args, **kwargs):
            password = str(request.data['password'])

            auth.models.User.objects.create_user(
                username=str(request.data['username']), email=request.data['email'], password=password)

            return self.create(request, *args, **kwargs)

    class Update(generics.UpdateAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer
        permission_classes = (permissions.AllowAny, )

    # class Delete(generics.DeleteAPIView):
    #     queryset = UserAccount.objects.all()
    #     serializer_class = UserAccountSerializer
    #     permission_classes = (permissions.AllowAny, )

    # class List(generics.ListAPIView):
    #     serializer_class = UserAccountSerializer

    #     def get_queryset(self):
    #         queryset = UserAccount.objects.all()
    #         cpf = self.request.query_params.get('cpf')
    #         # password = self.request.query_params.get('password')

    #         print(cpf)
    #         # print(password)

    #         if cpf is not None:
    #             queryset = queryset.filter(cpf=cpf)

    #         return queryset

        # search_fields = ['cpf']
        # filter_backends = (filters.SearchFilter,)
        # queryset = UserAccount.objects.all()
        # serializer_class = UserAccountSerializer


class UserAuthentication(APIView):
    def get(self, request):
        return Response({'ok': 200})

    @api_view(['GET', 'POST'])
    def login(request):
        if request.method == 'GET':
            return Response(status=status.HTTP_200_OK)

        if request.method == 'POST':
            body_data = json.dumps(request.data)
            body_data = json.loads(body_data)

            cpf, password = str(body_data['cpf']), str(body_data['password'])

            try:
                user = UserAccount.objects.get(pk=cpf)
            except Snippet.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            user = auth.authenticate(
                request, username=user, password=int(password))

            if user is not None:
                auth_login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
