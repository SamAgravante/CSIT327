from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #USERS
    path('users/', views.user_list_view, name='user_list'),  # User list
    path('users/update/<int:pk>/', views.update_user_view, name='update_user'),  # Update user
    path('users/change_password/', views.change_password_view, name='change_password'), # Change Password user
    path('users/delete/<int:pk>/', views.delete_user_view, name='delete_user'),  # Delete user
    #FORUMS
    path('forums/', views.forum, name='forums'),
    path('forums/create/', views.create_post, name='create_post'),
    path('forums/delete/<int:id>/', views.delete_post, name='delete_post'),
    #WATCHLIST
    path('itemslist/', views.items_list, name='items_list'),
    path('add-to-watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('delete-from-watchlist/', views.delete_from_watchlist, name='delete_from_watchlist'),
    path('faq/', views.faq, name='faq'),
]