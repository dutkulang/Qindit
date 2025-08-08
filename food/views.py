from django.shortcuts import render
from . import models


def index(request):
    context = {
        'restaurants': models.Restaurant.objects.all()
    }
    
    return render(request, 'main.html', context)


def foodItems(request):
    context = {
        "foodItems": models.MenuItem.objects.all()
    }
    return render(request, 'foods.html', context )

def foodItem(request, itemId):
    context= {
        'food': models.MenuItem.objects.filter(pk=itemId).first()
    }
    return render(request, 'food.html', context)