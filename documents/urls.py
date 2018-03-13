from django.conf.urls import url
from documents import views

urlpatterns = [
    url(r'^documents/$', views.DocumentsList.as_view()),
]
