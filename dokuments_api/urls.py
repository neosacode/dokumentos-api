from django.urls import path, include
from django.contrib import admin

urlpatterns = [
  path('admin/', admin.site.urls),
  path(r'^api-auth/', include('rest_framework.urls')),
  path('', include('apps.documents.urls')),
]
