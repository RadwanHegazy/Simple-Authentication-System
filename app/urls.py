from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('',views.Profile,name='profile'),

    path('register/',views.UserRegister.as_view(),name='register'),
    path('login/',views.login,name='login')

]