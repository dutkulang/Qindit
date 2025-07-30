from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model to define different types of users in the system.
    """
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant_owner', 'Restaurant Owner'),
        ('delivery_person', 'Delivery Person'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',
        help_text="Defines the role of the user in the application."
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="User's contact phone number."
    )
    address = models.TextField(
        blank=True,
        null=True,
        help_text="User's primary address."
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
