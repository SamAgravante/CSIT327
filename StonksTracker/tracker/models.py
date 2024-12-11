from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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
    item_id = models.CharField(max_length=100, unique=True, null=True)  # ItemID from API
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Average price from API
    image_url = models.URLField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='watchlists', null=True, blank=True
    )

    def price_deviation_percentage(self):
        if self.price and self.price_avg and self.price_avg != 0:
            deviation = ((self.price - self.price_avg) / self.price_avg) * 100
            return round(deviation, 2)
        return None

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Forums(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastEdited = models.DateTimeField(auto_now=True)
    isEdited = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='forums', null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} by {self.user.username}"

