from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forums
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
    # API endpoint
    api_url = "https://www.steamwebapi.com/steam/api/items"
    params = {
        'key': 'WH1SLQ1PX2CHGLK0',  # Replace with your actual API key
        'max': 200,
        'price_min': 0.001,
        'currency': 'PHP'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        items = response.json()  # Adjust key if needed based on API response structure
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        items = []  # Fallback to an empty list if there's an error

    return render(request, 'item_list.html', {'items': items})
