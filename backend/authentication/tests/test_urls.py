from django.http import response
from django.test import TestCase, Client
from django.urls import reverse, resolve

from authentication.views import UserAuthentication, UserAccountCRUD, UserInfoCRUD

class TestAuthenticationURLs(TestCase):
  def setUp(self):
    self.root_url = reverse('auth homepage')
    self.login_url = reverse('auth login')
    self.register_url = reverse('auth register')
    self.user_info_url = reverse('auth user info')

  def test_root_url_GET(self):
    self.assertEquals(resolve(self.root_url).func.view_class, UserAuthentication)

  def test_login_url_GET(self):
    self.assertEquals(resolve(self.login_url).func, UserAuthentication.login)

  def test_register_url_GET(self):
    self.assertEquals(resolve(self.register_url).func.view_class, UserAccountCRUD.Create)
    
  def test_user_info_url_GET(self):
    self.assertEquals(resolve(self.user_info_url).func.view_class, UserInfoCRUD.Create)

  
    

