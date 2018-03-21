from django.urls import path
from apps.documents import views

from apps.core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
urlpatterns = router.urls
urlpatterns += [
	path('users/create', views.CreateUserView.as_view(), name='users>create')
]