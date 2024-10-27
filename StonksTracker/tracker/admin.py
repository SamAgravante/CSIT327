from django.contrib import admin
from .models import User, Watchlist, Forums, PriceHistory

admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Forums)
admin.site.register(PriceHistory)
