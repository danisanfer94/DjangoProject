from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('index/', views.index,name='index2'),
    path('registre/', views.registre,name='registre'),
    path('login/', views.login,name='login'),
    path('administrador/', views.admin,name='admin')


]
