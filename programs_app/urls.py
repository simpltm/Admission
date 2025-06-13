from django.urls import path
from . import views

app_name = 'programs_app'

urlpatterns = [
    path('', views.ProgramListView.as_view(), name='program_list'),
    path('create/', views.ProgramCreateView.as_view(), name='program_create'),
    path('<int:pk>/update/', views.ProgramUpdateView.as_view(), name='program_update'),
] 