from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forums/', views.forum, name='forums'),
    path('forums/create/', views.create_post, name='create_post'),
    path('forums/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('itemslist/', views.items_list, name='items_list'),
    path('add-to-watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('delete-from-watchlist/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('faq/', views.faq, name='faq'),
]