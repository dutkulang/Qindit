from django.urls import path
from . import views

urlpatterns = [
    path('', views.foodItems, name="homepage" ),
    path("<int:itemId>", views.foodItem, name="foodItem"),
    path('search/', views.search_results, name='search_results'),
]