from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='Setups homepage'),
    path('svr_model/', views.SVRModelView.as_view(), name='SVR Model GET/POST'),
    path('svr_model/fit', views.SVRModelView.fit, name='SVR Model fit'),
    path('svr_model/predict', views.SVRModelView.predict, name='SVR Model predict'),
]