from django.urls import path, include
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api-token-auth', views.obtain_auth_token),
  path('api-auth', include('rest_framework.urls')),
  path('', include('apps.documents.urls')),
]
