from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

import json


# Create your views here.
class HomeView(APIView):
    def get(self, request):
        return Response({'ok': 200})


class MarkowitzView(APIView):
    def get(self, request):
        return Response({'ok': 200})
