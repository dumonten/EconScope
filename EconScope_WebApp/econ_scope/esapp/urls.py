from django.contrib import admin
from django.urls import path
from .views import ProductViewSet
from . import views

urlpatterns = [
    path('', ProductViewSet.as_view({
        "get": "home",
        "post": "image",
    })),
    path('internal', ProductViewSet.as_view({
        "post": "internal",
    })),
]


