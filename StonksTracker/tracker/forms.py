from django import forms
from .models import User, Watchlist, PriceHistory  # Use your custom user model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['UserID']  # Adjust the fields as needed

class PriceHistoryForm(forms.ModelForm):
    class Meta:
        model = PriceHistory
        fields = ['itemName', 'price']  # Exclude 'timestamp'
