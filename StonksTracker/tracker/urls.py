from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('forums/', views.forum, name='forums'),
    path('forums/create/', views.create_post, name='create_post'),
    path('forums/delete/<int:id>/', views.delete_post, name='delete_post'),
]