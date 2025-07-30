from django.db import models
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Restaurant(models.Model):
    """
    Represents a restaurant from which food can be ordered.
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'restaurant_owner'}, # Ensures only restaurant owners can be assigned as owners
        related_name='owned_restaurants',
        help_text="The user who owns this restaurant."
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the restaurant."
    )
    description = models.TextField(
        blank=True,
        help_text="A brief description of the restaurant."
    )
    address = models.TextField(
        help_text="Physical address of the restaurant."
    )
    phone_number = models.CharField(
        max_length=15,
        help_text="Contact phone number for the restaurant."
    )
    # ImageField uses Pillow internally for image processing (e.g., validation, storage).
    # When an image is uploaded, Pillow helps handle its format and basic manipulations.
    image = models.ImageField(
        upload_to='restaurant_images/', # Images will be stored in 'media/restaurant_images/'
        blank=True,
        null=True,
        help_text="Logo or main image of the restaurant."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the restaurant is currently active and accepting orders."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the restaurant was added."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the restaurant details were last updated."
    )

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ['name'] # Default ordering for restaurants

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """
    Represents a food item available on a restaurant's menu.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items',
        help_text="The restaurant this menu item belongs to."
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the menu item."
    )
    description = models.TextField(
        blank=True,
        help_text="A brief description of the menu item."
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)], # Ensures price is not negative
        help_text="Price of the menu item."
    )
    # ImageField for menu item photos, also leveraging Pillow.
    image = models.ImageField(
        upload_to='menu_item_images/', # Images will be stored in 'media/menu_item_images/'
        blank=True,
        null=True,
        help_text="Image of the menu item."
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Indicates if the menu item is currently available."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the menu item was added."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the menu item details were last updated."
    )

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['name'] # Default ordering for menu items

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

# Order Model: Represents a customer's order.
class Order(models.Model):
    """
    Represents a customer's food order.
    """
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted by Restaurant'),
        ('preparing', 'Preparing Food'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        limit_choices_to={'user_type': 'customer'},
        help_text="The customer who placed the order."
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurant_orders',
        help_text="The restaurant from which the order was placed."
    )
    delivery_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # If delivery person is deleted, orders remain but delivery_person field becomes NULL
        null=True,
        blank=True,
        related_name='assigned_deliveries',
        limit_choices_to={'user_type': 'delivery_person'},
        help_text="The delivery person assigned to this order."
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total amount of the order, including taxes and delivery fees."
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order."
    )
    delivery_address = models.TextField(
        help_text="The address where the order needs to be delivered."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the order was placed."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the order status was last updated."
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at'] # Order by most recent first

    def __str__(self):
        return f"Order #{self.id} - {self.status} - {self.customer.username}"

# OrderItem Model: Represents individual items within an order.
class OrderItem(models.Model):
    """
    Represents a single item within an order, linking to a MenuItem.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The order this item belongs to."
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        help_text="The menu item ordered."
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], # Ensures at least one item is ordered
        help_text="Quantity of the menu item ordered."
    )
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price of the item at the time the order was placed (to handle price changes)."
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'menu_item') # A specific menu item can only appear once per order

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"

