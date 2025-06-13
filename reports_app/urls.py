from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports, name='reports'),
    path('download/all/', views.download_all_excel, name='download_all'),
    path('download/excel/<int:applicant_id>/', views.download_applicant_excel, name='download_excel'),
    path('download/pdf/<int:applicant_id>/', views.download_applicant_pdf, name='download_pdf'),
    path('download/passport/<int:applicant_id>/', views.download_passport_scan, name='download_passport'),
    path('download/education/<int:applicant_id>/', views.download_education_document, name='download_education'),
    path('download/zip/<int:applicant_id>/', views.download_zip, name='download_zip'),
    # Здесь будут маршруты для отчётов
] 