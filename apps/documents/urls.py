from django.urls import path
from apps.documents import views

urlpatterns = [
    path('documents/', views.DocumentsList.as_view()),
    path('documents/<pk>', views.DocumentDetail.as_view()),
]
