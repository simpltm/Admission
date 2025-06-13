from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('program/<int:pk>/edit/', views.edit_program, name='edit_program'),
    path('program/<int:pk>/delete/', views.delete_program, name='delete_program'),
] 