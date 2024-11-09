from django.urls import path
from .views import (
    home_view,
    register_view,
    login_view,
    logout_view,
    user_list_view,
    update_user_view,
    delete_user_view,
    change_password_view,
    watchlist_view,
    add_watchlist_view,
    update_watchlist_view,
    delete_watchlist_view,
    price_history_view,
    add_price_history_view,
    update_price_history_view,
    delete_price_history_view,
    forum,
    create_post,
    update_post,
    delete_post,
)
urlpatterns = [
    path('', home_view, name='home'),  # Empty path for root URL
    path('home/', home_view, name='home'),
    path('signup/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', user_list_view, name='user_list'),  # User list
    path('users/update/<int:pk>/', update_user_view, name='update_user'),  # Update user
    path('users/change_password/', change_password_view, name='change_password'), # Change Password user
    path('users/delete/<int:pk>/', delete_user_view, name='delete_user'),  # Delete user
    
     # Watchlist URLs
    path('watchlist/', watchlist_view, name='watchlist'),
    path('watchlist/add/', add_watchlist_view, name='add_watchlist'),
    path('watchlist/update/<int:pk>/', update_watchlist_view, name='update_watchlist'),
    path('watchlist/delete/<int:pk>/', delete_watchlist_view, name='delete_watchlist'),
    
    # Price History URLs
    path('price_history/', price_history_view, name='price_history'),
    path('price_history/add/', add_price_history_view, name='add_price_history'),
    path('price_history/update/<int:pk>/', update_price_history_view, name='update_price_history'),
    path('price_history/delete/<int:pk>/', delete_price_history_view, name='delete_price_history'),
    
    # FORUMS URLs
    path('forums/', forum, name='forums'),
    path('forums/create/', create_post, name='create_post'),
    path('update_post/<int:id>/', update_post, name='update_post'),
    path('forums/delete/<int:id>/', delete_post, name='delete_post'),
]
