from django.urls import path
from . import views
from .view import hr_view, payroll

urlpatterns = [
    # system
    path('register/user/', views.register_user, name='login'),
    path('all/users/', views.get_all_user, name='get_all_users'),
    path('delete/user/<str:id>/', views.delete_user, name='delete_user'),
    path('get/user/<str:id>/', views.get_user, name='delete_user'),
    path('update/user/<str:id>/', views.get_user, name='delete_user'),
    
    # hr module
    path('register/employee/', hr_view.register_employee, name='register_employee'),
    path('all/employees/', hr_view.get_all_employees, name='get_all_users'),
    
    # payroll module
    path('all/payslips/', payroll.get_all_employees_payslips, name='get_all_users'),
]
