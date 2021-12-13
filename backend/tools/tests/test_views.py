from django.test import TestCase, Client
from django.urls import reverse

class TestToolsViews(TestCase):
  def setUp(self) -> None:
      self.client = Client()
      self.root_url = reverse('Tools homepage')
      self.markowivtz_url = reverse('Tools Markowitz')
        
  def test_root_url_GET(self):
    response = self.client.get(
      self.root_url
    )

    self.assertEquals(response.status_code, 200)
  
  def test_markowitz_url_GET(self):
    response = self.client.get(
      self.markowivtz_url
    )

    self.assertEquals(response.status_code, 200)