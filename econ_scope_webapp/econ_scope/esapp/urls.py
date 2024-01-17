from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.home, name='es-home'),
    path('about/', views.about, name='es-about'),
]

