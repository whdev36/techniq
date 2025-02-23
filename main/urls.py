from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('courses/', views.course_list, name='courses'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:id>/', views.lesson_detail, name='lesson_detail'),
]