from django.contrib import admin
from .models import User, Watchlist, Forums

admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Forums)
