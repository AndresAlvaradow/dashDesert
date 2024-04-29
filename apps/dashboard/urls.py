from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import *
app_name = 'dashboard'
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('login/',LoginView.as_view(template_name ='login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name ='login.html'), name='logout'),
    path('main/', main.as_view(), name='index'),
    path('machine/', views.statistics_machine, name='machine'),
    path('deep/', views.statistics_deep, name='deep'),
    path('admin/', admin.site.urls),
    path('detail/<str:identification>/<str:idScholYear>/', views.detail_views, name="detail_student"),
    path('academic/', views.statistics_academic, name="statistics_academic"),

]