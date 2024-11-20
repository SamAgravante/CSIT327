from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django import forms
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .forms import CustomUserCreationForm, WatchlistForm, PriceHistoryForm
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

# Home view
def home_view(request):
    return render(request, 'home_page.html')

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
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login_page.html')



# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# User List View (Read)
def user_list_view(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'user_list.html', {'users': users})

# Update User View (Update)
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

# Delete User View (Delete)
def delete_user_view(request, pk):
    user = get_object_or_404(User, UserID=pk)  # Fetch user by primary key (ID)
    if request.method == 'POST':
        user.delete()  # Delete user on POST request
        messages.success(request, 'User deleted successfully.')
        return redirect('user_list')  # Redirect to user list after deletion
    
    return render(request, 'delete_user.html', {'user': user})

# Change Password View
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


# Watchlist Views

@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(UserID=request.user)
    return render(request, 'watchlist.html', {'watchlist_items': watchlist_items})

@login_required
def add_watchlist_view(request):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist_item = form.save(commit=False)
            watchlist_item.UserID = request.user  # Set the user
            watchlist_item.save()
            return redirect('watchlist')
    else:
        form = WatchlistForm()
    return render(request, 'add_watchlist.html', {'form': form})

@login_required
def update_watchlist_view(request, pk):
    watchlist_item = get_object_or_404(Watchlist, pk=pk)
    if request.method == 'POST':
        form = WatchlistForm(request.POST, instance=watchlist_item)
        if form.is_valid():
            form.save()
            return redirect('watchlist')
    else:
        form = WatchlistForm(instance=watchlist_item)
    return render(request, 'update_watchlist.html', {'form': form})

@login_required
def delete_watchlist_view(request, pk):
    watchlist_item = get_object_or_404(Watchlist, pk=pk)
    if request.method == 'POST':
        watchlist_item.delete()
        return redirect('watchlist')
    return render(request, 'delete_watchlist.html', {'watchlist_item': watchlist_item})

# PriceHistory Views

@login_required
def price_history_view(request):
    price_history_items = PriceHistory.objects.all()
    return render(request, 'price_history.html', {'price_history_items': price_history_items})

@login_required
def add_price_history_view(request):
    if request.method == 'POST':
        form = PriceHistoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('price_history')
    else:
        form = PriceHistoryForm()
    return render(request, 'add_price_history.html', {'form': form})

@login_required
def update_price_history_view(request, pk):
    price_history_item = get_object_or_404(PriceHistory, pk=pk)
    if request.method == 'POST':
        form = PriceHistoryForm(request.POST, instance=price_history_item)
        if form.is_valid():
            form.save()
            return redirect('price_history')
    else:
        form = PriceHistoryForm(instance=price_history_item)
    return render(request, 'update_price_history.html', {'form': form})

@login_required
def delete_price_history_view(request, pk):
    price_history_item = get_object_or_404(PriceHistory, pk=pk)
    if request.method == 'POST':
        price_history_item.delete()
        return redirect('price_history')
    return render(request, 'delete_price_history.html', {'price_history_item': price_history_item})


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

def update_post(request, id):
    forum = get_object_or_404(Forums, id=id)
    if request.method == 'POST':
        forum.title = request.POST['title']
        forum.content = request.POST['content']
        forum.save()
        return redirect('forums')
    return render(request, 'update_post.html', {'forum': forum})

def delete_post(request, id):
    forum = Forums.objects.get(id=id)
    forum.delete()
    return redirect('forums')