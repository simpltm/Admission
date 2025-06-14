from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from applications_app.models import Application, SubjectScore, ProgramPreference, ApplicationPhoto
from programs_app.models import StudyProgram
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import HttpResponse, FileResponse
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import os
from django.core.paginator import Paginator
from reportlab.lib import colors
from reportlab.platypus import Image
import xlsxwriter
import zipfile

# Create your views here.

class ReportsView(LoginRequiredMixin, TemplateView):
    """Базовое представление для отчётов"""
    template_name = 'reports_app/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем параметры поиска и фильтрации
        search_query = self.request.GET.get('search', '')
        program_filter = self.request.GET.get('program', '')
        score_filter = self.request.GET.get('score', '')
        
        # Базовый запрос
        applicants = Application.objects.all().prefetch_related('program_preferences__program')
        
        # Применяем поиск
        if search_query:
            applicants = applicants.filter(
                Q(last_name__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        # Применяем фильтр по программе
        if program_filter:
            applicants = applicants.filter(program_preferences__program__name=program_filter)
        
        # Применяем фильтр по баллам
        if score_filter:
            applicants = applicants.filter(total_score__gte=float(score_filter))
        
        # Получаем список программ для фильтра
        programs = Application.objects.values_list('program_preferences__program__name', flat=True).distinct()
        
        # Пагинация
        paginator = Paginator(applicants, 10)  # 10 абитуриентов на страницу
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'applications': page_obj,
            'programs': programs,
            'search_query': search_query,
            'program_filter': program_filter,
            'score_filter': score_filter,
        })
        return context

@login_required
def reports(request):
    # Qidiruv va filtr
    search_query = request.GET.get('search', '')
    program_filter = request.GET.get('program', '')

    # Barcha arizalar
    applications = Application.objects.all().prefetch_related('program_preferences__program')

    # Qidiruv bo'yicha filter
    if search_query:
        applications = applications.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(middle_name__icontains=search_query)
        )
    # Yo'nalish bo'yicha filter
    if program_filter:
        applications = applications.filter(program_preferences__program__id=program_filter)

    # Statistika
    stats = {
        'total': Application.objects.count(),
        'programs': Application.objects.values('program_preferences__program').distinct().count(),
    }
    # Barcha yo'nalishlar
    programs = StudyProgram.objects.all()

    context = {
        'applications': applications,
        'stats': stats,
        'programs': programs,
        'search_query': search_query,
        'program_filter': program_filter,
    }
    return render(request, 'reports_app/reports.html', context)

@login_required
def download_all_excel(request):
    """Скачать данные всех абитуриентов в Excel"""
    # Получаем параметры фильтрации
    search_query = request.GET.get('search', '')
    program_filter = request.GET.get('program', '')
    score_filter = request.GET.get('score', '')
    
    # Базовый запрос
    applicants = Application.objects.all().prefetch_related('program_preferences__program')
    
    # Применяем фильтры
    if search_query:
        applicants = applicants.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    if program_filter:
        applicants = applicants.filter(program_preferences__program__name=program_filter)
    if score_filter:
        applicants = applicants.filter(total_score__gte=float(score_filter))
    
    # Создаем DataFrame с данными
    data = []
    EDUCATION_FORM_LABELS = {
        'bachelor_full': 'Очная форма обучения бакалавриат',
        'specialist_full': 'Очная форма обучения специалитет',
        'master_full': 'Очная форма обучения магистратура',
        'master_part': 'Очно-заочная форма обучения магистратура',
        'bachelor_part': 'Заочная форма обучения бакалавриат',
    }
    for applicant in applicants:
        data.append({
            'ФИО': f"{applicant.last_name} {applicant.first_name} {applicant.middle_name}",
            'Дата рождения': applicant.birth_date,
            'Email': applicant.email,
            'Telefon': applicant.phone,
            'Форма обучения': EDUCATION_FORM_LABELS.get(applicant.education_form, applicant.education_form),
            'Yo\'nalishlar': ', '.join([p.program.name for p in applicant.program_preferences.all()]),
        })
    
    df = pd.DataFrame(data)
    
    # Создаем Excel файл
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Абитуриенты', index=False)
        
        # Получаем объект рабочего листа
        worksheet = writer.sheets['Абитуриенты']
        
        # Настраиваем ширину столбцов
        for idx, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.set_column(idx, idx, max_length + 2)
    
    output.seek(0)
    
    # Отправляем файл
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=all_applicants.xlsx'
    return response

@login_required
def download_applicant_excel(request, applicant_id):
    """Скачать данные абитуриента в Excel"""
    applicant = Application.objects.select_related('applicant').get(id=applicant_id)
    EDUCATION_FORM_LABELS = {
        'bachelor_full': 'Очная форма обучения бакалавриат',
        'specialist_full': 'Очная форма обучения специалитет',
        'master_full': 'Очная форма обучения магистратура',
        'master_part': 'Очно-заочная форма обучения магистратура',
        'bachelor_part': 'Заочная форма обучения бакалавриат',
    }
    data = {
        'ФИО': [f"{applicant.last_name} {applicant.first_name} {applicant.middle_name}"],
        'Дата рождения': [applicant.birth_date],
        'Email': [applicant.email],
        'Телефон': [applicant.phone],
        'Форма обучения': [EDUCATION_FORM_LABELS.get(applicant.education_form, applicant.education_form)],
        'Программы': [', '.join([p.program.name for p in applicant.program_preferences.all()])],
    }
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Данные абитуриента', index=False)
    output.seek(0)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    full_name = f"{applicant.last_name}_{applicant.first_name}_{applicant.middle_name}".replace(' ', '_')
    filename = f"{full_name}_{timestamp}.xlsx"
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

@login_required
def download_applicant_pdf(request, applicant_id):
    """Скачать все изображения (паспорт, диплом, фото) абитуриента в PDF, только изображения на отдельных страницах"""
    applicant = Application.objects.get(id=applicant_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    # 1. Паспорт
    if applicant.passport_scan and applicant.passport_scan.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        p.drawImage(applicant.passport_scan.path, 100, 200, width=300, height=400, preserveAspectRatio=True, anchor='c', mask='auto')
        p.showPage()
    # 2. Диплом
    if applicant.education_document and applicant.education_document.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        p.drawImage(applicant.education_document.path, 100, 200, width=300, height=400, preserveAspectRatio=True, anchor='c', mask='auto')
        p.showPage()
    # 3. Barcha rasmlar (yangi va eski)
    photos = list(applicant.photos.all())
    if not photos and applicant.photo:
        class TempPhoto:
            image = applicant.photo
        photos = [TempPhoto()]
    if photos:
        for photo in photos:
            if photo.image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                p.drawImage(photo.image.path, 100, 200, width=300, height=400, preserveAspectRatio=True, anchor='c', mask='auto')
                p.showPage()
    p.save()
    buffer.seek(0)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    full_name = f"{applicant.last_name}_{applicant.first_name}_{applicant.middle_name}".replace(' ', '_')
    filename = f"{full_name}_{timestamp}_all_images.pdf"
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

@login_required
def download_passport_scan(request, applicant_id):
    applicant = Application.objects.get(id=applicant_id)
    if not applicant.passport_scan:
        return HttpResponse('Fayl topilmadi', status=404)
    response = FileResponse(applicant.passport_scan.open('rb'), as_attachment=True, filename=f'passport_scan_{applicant_id}{applicant.passport_scan.name[-4:]}')
    return response

@login_required
def download_education_document(request, applicant_id):
    applicant = Application.objects.get(id=applicant_id)
    if not applicant.education_document:
        return HttpResponse('Fayl topilmadi', status=404)
    response = FileResponse(applicant.education_document.open('rb'), as_attachment=True, filename=f'education_document_{applicant_id}{applicant.education_document.name[-4:]}')
    return response

@login_required
def download_zip(request, applicant_id):
    """Pasport, diplom va fotografiyani ZIP fayl ko'rinishida yuklab olish"""
    applicant = Application.objects.get(id=applicant_id)
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Pasport
        if applicant.passport_scan and applicant.passport_scan.path:
            zip_file.write(applicant.passport_scan.path, arcname='passport' + applicant.passport_scan.name[-4:])
        # Diplom
        if applicant.education_document and applicant.education_document.path:
            zip_file.write(applicant.education_document.path, arcname='diplom' + applicant.education_document.name[-4:])
        # Foto
        if applicant.photo and applicant.photo.path:
            zip_file.write(applicant.photo.path, arcname='photo' + applicant.photo.name[-4:])
        # Notarial tarjima
        if applicant.notarized_passport_scan and applicant.notarized_passport_scan.path:
            zip_file.write(applicant.notarized_passport_scan.path, arcname='notarial_tarjima' + applicant.notarized_passport_scan.name[-4:])
    buffer.seek(0)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    full_name = f"{applicant.last_name}_{applicant.first_name}_{applicant.middle_name}".replace(' ', '_')
    filename = f"{full_name}_{timestamp}_files.zip"
    response = HttpResponse(buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
