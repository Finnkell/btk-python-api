from django.shortcuts import render

from asgiref.sync import sync_to_async

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.decorators import api_view

import json
import joblib

import numpy as np
import pandas as pd
import yfinance as yf

from .ai_models.strategies.svr_model import SVRStrategyModel


# Create your views here.
class HomeView(APIView):
    def get(self, request):
        return Response({'ok': 200})


class SVRModelView(APIView):

    @api_view(['GET'])
    def fit(request):
        if request.method == 'GET':

            __model = SVRStrategyModel()

            body_data = json.dumps(request.data)
            body = json.loads(body_data)

            asset_name = body['name']
            start_date = body['start_date']
            end_date = body['end_date']
            train_size = body['train_size']
            test_size = body['test_size']
            deploy_size = body['deploy_size']

            # dataframe = pd.read_csv(
            #     f'D:/Dados historicos-NOVO/Bovespa_02012017_30062021/ohlc/OHLC_{asset_name}_BOV_T.csv', sep=',')

            try:
                dataframe = yf.download(asset_name + '.SA')
            except Exception:
                return JsonResponse({'error': 'Download error', 'response': 500})

            try:
                if __model.strategy_run(asset_name, dataframe, start_date, end_date, train_size, test_size, deploy_size):
                    return JsonResponse({'model_trained': True})
            except Exception:
                return JsonResponse({'model_trained': False, 'error': 'Strategy run error', 'response': 500})

            return JsonResponse({'model_trained': False})

    @api_view(['GET'])
    def predict(request):
        if request.method == 'GET':
            body_data = json.dumps(request.data)
            body = json.loads(body_data)

            asset_name = body['name']
            data_to_predict = body['data']

            load_model = joblib.load(
                f'static/saved_models/{asset_name}/SVR.pkl')

            y_pred = load_model.predict(np.array([data_to_predict]))

            return JsonResponse({'prediction': y_pred[0]})

    def get(self, request):
        body_data = json.dumps(request.data)
        body_data = json.loads(body_data)
        asset_name = body_data['name']

        model_summary = joblib.load(
            f'static/saved_models/{asset_name}/SVR_summary.pkl')

        return JsonResponse({'summary': model_summary})
