from django.http import response
from django.test import TestCase, Client
from django.urls import reverse, resolve

from setups.views import HomeView, SVRModelView

class TestSetupsURLs(TestCase):
  def setUp(self):
    self.root_url = reverse('Setups homepage')
    self.svr_model_url = reverse('SVR Model GET/POST')
    self.svr_model_fit_url = reverse('SVR Model fit')
    self.svr_model_predict_url = reverse('SVR Model predict')

  def test_root_URL(self):
    self.assertEquals(resolve(self.root_url).func.view_class, HomeView)

  def test_svr_model_URL(self):
    self.assertEquals(resolve(self.svr_model_url).func.view_class, SVRModelView)

  def test_svr_model_fit_URL(self):
    self.assertEquals(resolve(self.svr_model_fit_url).func, SVRModelView.fit)

  def test_svr_model_predict_URL(self):
    self.assertEquals(resolve(self.svr_model_predict_url).func, SVRModelView.predict)
