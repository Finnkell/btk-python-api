from django.http import response
import requests
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
import json

class TestSetupsViews(TestCase):
  def setUp(self):
    self.root_url = reverse('Setups homepage')
    self.svr_model_url = reverse('SVR Model GET/POST')
    self.svr_model_fit_url = reverse('SVR Model fit')
    self.svr_model_predict_url = reverse('SVR Model predict')

  def test_root_url_GET(self):
    response = self.client.get(self.root_url)
    self.assertEquals(response.status_code, 200)

  def test_svr_model_url_GET(self):
    response = requests.get(
      'https://btk-ai-app.herokuapp.com/setups/svr_model/',
      json = {
        'name': "PETR4"
      }
    )
    self.assertEquals(response.status_code, 200)

  def test_svr_model_fit_url_GET(self):
    response = requests.get(
      'http://localhost:8000'+self.svr_model_fit_url,
      json = {
        'name': "PETR4",
        'start_date': '2020-01-01',
        'end_date': '2020-12-31',
        'train_size': 0.6,
        'test_size': 0.3,
        'deploy_size': 0.1
      }
    )
    
    self.assertEquals(response.status_code, 200)