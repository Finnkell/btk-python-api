from django.contrib import admin
from django.urls import path, include

from django.http import Http404


def error_404(request, exception):
    HttpResponse('Error handler content', status=404)


handler404 = error_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('setups/', include('setups.urls')),
    path('tools/', include('tools.urls')),
]
