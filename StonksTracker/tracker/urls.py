from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forums/', views.forum, name='forums'),
    path('forums/create/', views.create_post, name='create_post'),
    path('forums/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('itemslist/', views.items_list, name='items_list'),
    path('add-to-watchlist/<str:item_id>/', views.add_to_watchlist, name='add-to-watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
]