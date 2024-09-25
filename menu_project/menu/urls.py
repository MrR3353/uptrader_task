from django.urls import path
from . import views

urlpatterns = [
    path('<path:url>/', views.dynamic_view, name='dynamic_view'),  # Для всех остальных страниц
    path('', views.dynamic_view, name='home'),  # Для главной страницы "/"
]