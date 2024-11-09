from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    UserID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = "tracker_user"

    def __str__(self):
        return self.username


class Watchlist(models.Model):
    WatchlistID = models.AutoField(primary_key=True)  # Automatically incrementing primary key
    UserID = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # One-to-one relationship with User model

    class Meta:
        db_table = 'tracker_watchlists'  # Use lowercase and plural form for consistency

    def __str__(self):
        return f"Watchlist ID: {self.WatchlistID} for User: {self.UserID.username}"

class PriceHistory(models.Model):
    historyID = models.AutoField(primary_key=True)  # Automatically incrementing primary key
    itemName = models.CharField(max_length=100, default="Unknown Item")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created

    class Meta:
        db_table = "tracker_pricehistory"  # Use lowercase and plural form for consistency

    def __str__(self):
        return f"PriceHistory ID: {self.historyID}, Item: {self.itemName}, Price: {self.price}"
    
class Forums(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastEdited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank
    class Meta:
        db_table = 'tracker_forums'
    def __str__(self):
        return self.title