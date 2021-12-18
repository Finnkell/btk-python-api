from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import yfinance as yf

from .markowitz import markowits


# Create your views here.
class HomeView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class MarkowitzView(APIView):
    def get(self, request):
        body_data = json.dumps(request.data)
        body_data = json.loads(body_data)
        
        try:
            start_date = body_data['start_date']
            end_date = body_data['end_date']
            assets_list = body_data['assets']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df_symbols = yf.download(assets_list, start=f'{str(start_date)}-01-01', end=f'{str(end_date)}-12-31', progress=False)['Close']
            df_symbols.dropna(axis=0, inplace=True)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        markowits(df_symbols)
        
        return Response({'ok': 200})
