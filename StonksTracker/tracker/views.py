from django.utils import timezone
import requests # type: ignore

from django.contrib import messages
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseForbidden
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


@login_required
def update_account_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully.')
            return redirect('account_settings')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'account_settings.html', {'form': form})


@login_required
def user_list_view(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'user_list.html', {'users': users})


@login_required
def update_user_view(request, pk):
    user = get_object_or_404(User, UserID=pk)  # Fetch user by primary key (ID)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')  # Redirect to user list after update
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'update_user.html', {'form': form})


@login_required
def delete_user_view(request, pk):
    user = get_object_or_404(User, UserID=pk)  # Fetch user by primary key (ID)
    if request.method == 'POST':
        user.delete()  # Delete user on POST request
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')  # Redirect to user list after deletion
    
    return render(request, 'delete_user.html', {'user': user})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! Keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')  # Redirect to home or any other page
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})



@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def forum(request):
    forums = Forums.objects.all()
    return render(request, 'forums.html', {'forums': forums})


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user if request.user.is_authenticated else None  # Set to None if not logged in
        Forums.objects.create(title=title, content=content, user=user)
        return redirect('forums')
    return render(request, 'create_post.html')


@login_required
def delete_post(request, id):
    forum = Forums.objects.get(id=id)
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    forum.delete()
    return redirect('forums')


@login_required
def items_list(request):
    api_url = "https://www.steamwebapi.com/steam/api/items"
    params = {
        'key': 'B3Z3J3HCPM0WWKCA',
        'max': 50,
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

@login_required
def add_to_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url')

        if not Watchlist.objects.filter(item_id=item_id, user=request.user).exists():
            Watchlist.objects.create(
                item_id=item_id,
                name=name,
                price=price,
                image_url=image_url,
                user=request.user  # Associate with logged-in user
            )
            messages.success(request, 'Item added to watchlist!')
        else:
            messages.error(request, 'Item already in your watchlist!')

    return redirect('items_list')

@login_required
def delete_from_watchlist(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        Watchlist.objects.filter(item_id=item_id).delete()
    return redirect('watchlist')


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user)
    api_url = "https://www.steamwebapi.com/steam/api/items"
    api_key = 'B3Z3J3HCPM0WWKCA'  # Replace with your actual API key

    for item in items:
        params = {'key': api_key, 'item_id': item.item_id, 'currency': 'PHP'}
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error for HTTP codes >= 400

            # Parse the API response
            data = response.json()

            # Check if the response is a list
            if isinstance(data, list):
                # Assuming the first item in the list contains the desired data
                data = data[0] if data else {}

            # Extract the latest price
            price = data.get('pricelatest', 0) if isinstance(data, dict) else 0

            # Save to PriceHistory if price data is valid
            if price > 0:
                PriceHistory.objects.create(
                    itemName=item.name,
                    price=price,
                    timestamp=timezone.now()
                )
        except requests.RequestException as e:
            print(f"Error fetching data for item {item.name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for item {item.name}: {e}")

    return render(request, 'watchlist.html', {'items': items})

@login_required
def faq(request):
    return render(request, 'faq.html')

@login_required
def edit_post(request, id):
    forum = get_object_or_404(Forums, id=id)
    
    # Ensure only the post creator can edit
    if forum.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    
    if request.method == 'POST':
        forum.title = request.POST['title']
        forum.content = request.POST['content']
        forum.isEdited = True
        forum.dateCreated = timezone.now()  # Update the created timestamp
        forum.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('forums')
    
    # Populate form with existing post data
    return render(request, 'edit_post.html', {
        'forum': forum
    })

#debug
@login_required
def landing_page(request):
    return render(request, 'landing.html')

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, UserID=pk)
    return render(request, 'user_detail.html', {'user': user})

@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, UserID=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User profile updated successfully.')
            return redirect('user_detail', pk=user.UserID)
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, UserID=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('index')
    return render(request, 'delete_user.html', {'user': user})