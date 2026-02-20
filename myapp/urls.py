from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    

    path('feedback/', views.feedback_view, name='feedback'),
    path('signup/', views.signup, name='signup'),

    path('about/', views.about, name='about'),

    path('student-login/', views.student_login, name="student_login"),
    path('student-dashboard/', views.student_dashboard, name="student_dashboard"),
    path('submit-status/', views.submit_status, name="submit_status"),
    path('student-status/', views.student_status, name="student_status"),

    path('driver-login/', views.driver_login, name='driver_login'),
    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    path('passenger-list/', views.passenger_list, name='passenger_list'),
    
]
