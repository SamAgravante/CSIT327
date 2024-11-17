from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=100, unique=True, null=True)  # ItemID from API
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Forums(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastEdited = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank

    def __str__(self):
        return self.title

class PriceHistory(models.Model):
    itemName = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.itemName} - {self.price}"

