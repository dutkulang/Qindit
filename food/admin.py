from django.contrib import admin
from food.models import Restaurant, MenuItem, Order, OrderItem

admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)
