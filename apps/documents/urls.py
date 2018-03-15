from django.conf.urls import url
from apps.documents import views

urlpatterns = [
    url(r'^documents/$', views.DocumentsList.as_view()),
]
