from django.urls import path
from base import views

urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.registeruser, name='register'),
    path('profile/<str:pk>', views.userprofile, name='profile'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('room/<int:pk>/', views.room, name='room'),
    path('create/', views.createroom, name='create'),
    path('update/<int:pk>', views.updateroom, name='update'),
    path('delete/<int:pk>', views.deleteroom, name='delete'),
    path('del-msg/<int:pk>', views.delete_message, name='delete_message'),
    path('updateuser/', views.updateuser, name='updateuser'),
    path('topic/', views.topic, name='topic'),
    path('activity/', views.activity, name='activity')
]
