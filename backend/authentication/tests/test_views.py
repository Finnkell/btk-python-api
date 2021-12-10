from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth

from authentication.views import UserAccount

class TestAuthenticationViews(TestCase):
  def setUp(self):
    self.client = Client()
    self.root_url = reverse('auth homepage')
    self.login_url = reverse('auth login')
    self.register_url = reverse('auth register')
    self.user_info_url = reverse('auth user info')

    self.user = UserAccount.objects.create(
      cpf = "51937463060",
      password = "123",
      username = "thisisanusername",
      email = "thisisanemail@gmail.com",
      phone = "42977451163",
      user_info = None
    )

    auth.models.User.objects.create_user(
      username= "thisisanusername", email = "thisisanemail@gmail.com", password = "123")

  def test_root_url_GET(self):
    response = self.client.get(self.root_url)
    self.assertEquals(response.status_code, 200)

  def test_login_url_GET(self):
    response = self.client.get(self.login_url)
    self.assertEquals(response.status_code, 200)

  def test_register_url_GET(self):
    response = self.client.get(self.register_url)
    self.assertEquals(response.status_code, 200)

  def test_user_info_url_GET(self):
    response = self.client.get(self.user_info_url)
    self.assertEquals(response.status_code, 200)
  
  def test_login_url_POST(self):
    response = self.client.post(
      self.login_url,
      {
        "cpf": "51937463060",
        "password": "123"
      }
      ,
      'application/json'
    )

    self.assertEquals(response.status_code, 200)

  def test_register_url_POST(self):
    response = self.client.post(
      self.register_url,
      {
          "cpf": "20906291003",
          "password": "123",
          "username": "supermegausername",
          "email": "supermegaemail@gmail.com",
          "phone": "42944578814",
          "user_info": ""
      }
    )

    self.assertEquals(response.status_code, 201)
  
  def test_user_info_url_POST(self):
    response = self.client.post(
      self.user_info_url,
      {
        "city": "São Paulo",
        "state": "São Paulo",
        "street": "Avenida Faria Lima",
        "neighbourhood": "",
        "age": 20
      }
    )

    self.assertEquals(response.status_code, 201)

