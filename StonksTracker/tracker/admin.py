from django.contrib import admin
from .models import User, Watchlist, Forums, PriceHistory

admin.site.register(Watchlist)
admin.site.register(PriceHistory)
admin.site.register(Forums)
admin.site.register(User)