from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='login'),
    path('all/users/', views.get_all_user, name='get_all_users'),
    path('delete/user/<str:email>/', views.delete_user, name='delete_user'),
]
