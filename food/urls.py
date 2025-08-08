from django.urls import path
from . import views

urlpatterns = [
    path('', views.foodItems, name="homepage" ),
    path("<int:itemId>", views.foodItem, name="foodItem")
]