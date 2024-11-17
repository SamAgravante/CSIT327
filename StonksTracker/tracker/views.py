from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forums
from .models import Watchlist
import requests # type: ignore

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

def add_to_watchlist(request, item_id):
    api_url = "https://www.steamwebapi.com/steam/api/items"
    params = {
        'key': 'WH1SLQ1PX2CHGLK0',
        'item_id': item_id,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        item_data = response.json()

        if isinstance(item_data, list):
            item_data = item_data[0]
    except requests.RequestException as e:
        print(f"Error fetching item: {e}")
        return redirect('item-list')

    if not request.user.is_authenticated:
        watchlist_items = request.session.get('watchlist', [])
        if not any(item['item_id'] == item_id for item in watchlist_items):
            watchlist_items.append({
                'item_id': item_id,
                'name': item_data['markethashname'],
                'price': item_data['pricelatest'],
                'image_url': item_data['itemimage'],
            })
            request.session['watchlist'] = watchlist_items
    else:
        if not Watchlist.objects.filter(user=request.user, item_id=item_id).exists():
            Watchlist.objects.create(
                user=request.user,
                item_id=item_id,
                name=item_data['markethashname'],
                price=item_data['pricelatest'],
                image_url=item_data['itemimage']
            )
    return redirect('watchlist')

def watchlist(request):
    if request.user.is_authenticated:
        # Authenticated users: Fetch watchlist items from database
        watchlist_items = Watchlist.objects.filter(user=request.user)
    else:
        # Unauthenticated users: Fetch watchlist items from session
        watchlist_items = request.session.get('watchlist', [])
    
    # Handle data format for template
    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})