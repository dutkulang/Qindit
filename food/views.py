from django.shortcuts import render
from . import models
from django.db.models import Q

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

def search_results(request):
    query = request.GET.get('q')
    if query:
        results = models.MenuItem.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )  # Search in title or content fields
    else:
        results = models.MenuItem.objects.none()  # Or all() if you want defaults
    return render(request, 'search-result.html', {'foods': results, 'query': query})