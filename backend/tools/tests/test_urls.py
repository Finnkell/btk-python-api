from django.http import response
from django.test import TestCase, Client
from django.urls import reverse, resolve

from tools.views import HomeView, MarkowitzView

class TestToolsURL(TestCase):
  def setUp(self):
    self.root_url = reverse('Tools homepage')
    self.markowitz_url = reverse('Tools Markowitz')

  def test_root_URL(self):
    self.assertEquals(resolve(self.root_url).func.view_class, HomeView)

  def test_markowitz_URL(self):
    self.assertEquals(resolve(self.markowitz_url).func.view_class, MarkowitzView)