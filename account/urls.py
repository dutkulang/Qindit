from django.urls import path
from . import views # Import the views from the same directory

# Define URL patterns for your application
urlpatterns = [
    # URL for the list of restaurants (e.g., /app/)
    path('', views.restaurant_list, name='restaurant_list'),
    # URL for a specific restaurant's menu (e.g., /app/restaurant/1/menu/)
    path('restaurant/<int:restaurant_id>/menu/', views.menu_detail, name='menu_detail'),

    # New URL patterns for user authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]