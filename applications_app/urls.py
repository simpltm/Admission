from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application_list'),
    path('create/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application_update'),
    path('<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
    path('<int:pk>/submit/', views.submit_application, name='application_submit'),
    # path('<int:pk>/pdf/', views.generate_pdf, name='application_pdf'),  # временно отключено
] 