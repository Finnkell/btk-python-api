from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.decorators import api_view

import json
import joblib

import numpy as np
import pandas as pd

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

            body = json.loads(request.body)

            asset_name = body['name']
            start_date = body['start_date']
            end_date = body['end_date']
            train_size = body['train_size']
            test_size = body['test_size']
            deploy_size = body['deploy_size']

            dataframe = pd.read_csv(
                f'D:/Dados historicos-NOVO/Bovespa_02012017_30062021/ohlc/OHLC_{asset_name}_BOV_T.csv', sep=',')

            if __model.strategy_run(asset_name, dataframe, start_date, end_date, train_size, test_size, deploy_size):
                model_summary = joblib.load(
                    f'static/saved_models/{asset_name}/SVR_summary.pkl')

                return JsonResponse({'model_trained': True})

            return JsonResponse({'model_trained': False})

    @api_view(['GET'])
    def predict(request):

        if request.method == 'GET':
            body = json.loads(request.body)

            asset_name = body['name']
            data_to_predict = body['data']

            load_model = joblib.load(
                f'static/saved_models/{asset_name}/SVR.pkl')

            y_pred = load_model.predict(np.array([data_to_predict]))

            return JsonResponse({'prediction': y_pred[0]})

    def get(self, request):
        body = json.loads(request.body)
        asset_name = body['name']

        model_summary = joblib.load(
            f'static/saved_models/{asset_name}/SVR_summary.pkl')

        return JsonResponse({'summary': model_summary})
