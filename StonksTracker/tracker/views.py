from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forums
from .models import Watchlist
import requests # type: ignore
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def forum(request):
    forums = Forums.objects.all()
    return render(request, 'forums.html', {'forums': forums})

def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user if request.user.is_authenticated else None  # Set to None if not logged in
        Forums.objects.create(title=title, content=content, user=user)
        return redirect('forums')
    return render(request, 'create_post.html')

def delete_post(request, id):
    forum = Forums.objects.get(id=id)
    forum.delete()
    return redirect('forums')

def items_list(request):
    api_url = "https://www.steamwebapi.com/steam/api/items"
    params = {
        'key': 'WH1SLQ1PX2CHGLK0',
        'max': 1000,
        'sort_by': 'priceRealAz',
        'price_min': 0.001,
        'currency': 'PHP'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        items = response.json() 
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        items = [] 

    return render(request, 'item_list.html', {'items': items})

def add_to_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')

        if not Watchlist.objects.filter(item_id=item_id).exists():
            Watchlist.objects.create(
                item_id=item_id,
                name=name,
                price=price,
                image_url=image_url
            )
            return JsonResponse({'success': True, 'message': 'Item added to watchlist!'})
        else:
            return JsonResponse({'success': False, 'message': 'Item already in watchlist!'})

    return JsonResponse({'success': False, 'message': 'Invalid request!'})

def delete_from_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        Watchlist.objects.filter(item_id=item_id).delete()
    return redirect('watchlist')

def watchlist(request):
    items = Watchlist.objects.all()
    return render(request, 'watchlist.html', {'items': items})