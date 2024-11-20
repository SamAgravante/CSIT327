from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Forums
from .models import Watchlist
import requests # type: ignore
from django.shortcuts import redirect
from django.contrib import messages


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django import forms
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .forms import CustomUserCreationForm
from .models import User, Watchlist, PriceHistory, Forums # Ensure you import necessary models

# Custom UserCreationForm to include email
class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Hash the password
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None  # Disable password field in the update form

    class Meta:
        model = User
        fields = ('username', 'email')  # Only allow updating username and email


# Register view (Sign-up)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup_page.html', {'form': form})

# Login view


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)  # Authenticate using email
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login_page.html')



# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')




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
        'sort_by': 'name',
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
            messages.success(request, 'Item added to watchlist!')
        else:
            messages.error(request, 'Item already in watchlist!')

    return redirect('items_list')


def delete_from_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        Watchlist.objects.filter(item_id=item_id).delete()
    return redirect('watchlist')


def watchlist(request):
    items = Watchlist.objects.all()
    return render(request, 'watchlist.html', {'items': items})

def faq(request):
    return render(request, 'faq.html')