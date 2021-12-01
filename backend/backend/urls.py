from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('setups/', include('setups.urls')),
    path('tools/', include('tools.urls')),
]
