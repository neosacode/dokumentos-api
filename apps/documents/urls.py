from apps.documents import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, base_name='documents')
urlpatterns = router.urls
