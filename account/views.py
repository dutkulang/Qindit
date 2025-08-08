from food.models import Restaurant, MenuItem, Order, OrderItem
from account.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Import the models defined above
# from .models import Restaurant, MenuItem, Order, OrderItem, User
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

def restaurant_list(request):
    """
    View to display a list of all active restaurants.
    This would be the main landing page for customers.
    """
    # Fetch all active restaurants from the database
    restaurants = Restaurant.objects.filter(is_active=True).order_by('name')
    context = {
        'restaurants': restaurants,
        'page_title': 'Restaurants Near You'
    }
    # Render the 'restaurant_list.html' template with the fetched data
    return render(request, 'restaurant_app/restaurant_list.html', context)

def menu_detail(request, restaurant_id):
    """
    View to display the menu items for a specific restaurant.
    """
    # Get the restaurant object or return a 404 error if not found
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    # Fetch all available menu items for the selected restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True).order_by('name')
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'page_title': f"{restaurant.name} Menu"
    }
    # Render the 'menu_detail.html' template with the restaurant and menu data
    return render(request, 'restaurant_app/menu_detail.html', context)

def signup_view(request):
    """
    View for user registration.
    Handles both displaying the form (GET) and processing it (POST).
    """
    if request.method == 'POST':
        # Use the custom form with your custom User model
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user
            user = form.save()
            # Set the user type to 'customer' by default
            user.user_type = 'customer'
            user.save()
            # Log in the user after successful registration
            login(request, user)
            # Redirect to the restaurant list page
            return redirect('homepage')
    else:
        # Display an empty form on GET request
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
def login_view(request):
    """
    View for user login.
    Handles both displaying the form (GET) and processing it (POST).
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to the restaurant list page
                return redirect('homepage')
    else:
        # Display an empty form on GET request
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    # Redirect to the restaurant list page after logout
    return redirect('homepage')


