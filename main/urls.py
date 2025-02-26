from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # 🔐 User authentication
    # 🔑 Optimize login and logout processes
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # 📝 Create a registration page
    path('register/', views.register_user, name='register'),
]