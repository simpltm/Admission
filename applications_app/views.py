from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
from .models import Application, SubjectScore, ProgramPreference
from .forms import ApplicationForm, SubjectScoreFormSet, ProgramPreferenceFormSet
from programs_app.models import StudyProgram, Subject

class ApplicationListView(LoginRequiredMixin, ListView):
    """Представление для списка заявлений"""
    model = Application
    template_name = 'applications_app/application_list.html'
    context_object_name = 'applications'
    paginate_by = 10

    def get_queryset(self):
        """Фильтрация заявлений в зависимости от роли пользователя"""
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(applicant=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['total_applications'] = Application.objects.count()
        return context

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Представление для просмотра заявления"""
    model = Application
    template_name = 'applications_app/application_detail.html'
    context_object_name = 'application'

    def test_func(self):
        """Проверка прав доступа"""
        application = self.get_object()
        return self.request.user.is_staff or application.applicant == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scores'] = self.object.scores.all()
        context['program_preferences'] = self.object.program_preferences.all().order_by('priority')
        return context

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания заявления"""
    model = Application
    form_class = ApplicationForm
    template_name = 'applications_app/application_form.html'
    success_url = reverse_lazy('applications:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['preferences_formset'] = ProgramPreferenceFormSet(self.request.POST)
        else:
            context['preferences_formset'] = ProgramPreferenceFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preferences_formset = context['preferences_formset']
        if preferences_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.applicant = self.request.user
            self.object.save()
            preferences_formset.instance = self.object
            preferences_formset.save()
            messages.success(self.request, 'Заявление успешно создано')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление для редактирования заявления"""
    model = Application
    form_class = ApplicationForm
    template_name = 'applications_app/application_form.html'

    def test_func(self):
        application = self.get_object()
        return self.request.user.is_staff or (
            application.applicant == self.request.user and
            application.status in ['draft', 'rejected']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['preferences_formset'] = ProgramPreferenceFormSet(self.request.POST, instance=self.object)
        else:
            context['preferences_formset'] = ProgramPreferenceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preferences_formset = context['preferences_formset']
        if preferences_formset.is_valid():
            self.object = form.save()
            preferences_formset.instance = self.object
            preferences_formset.save()
            messages.success(self.request, 'Заявление успешно обновлено')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('applications:application_detail', kwargs={'pk': self.object.pk})

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление для удаления заявления"""
    model = Application
    template_name = 'applications_app/application_confirm_delete.html'
    success_url = reverse_lazy('applications:application_list')

    def test_func(self):
        """Проверка прав доступа"""
        application = self.get_object()
        return self.request.user.is_staff or (
            application.applicant == self.request.user and
            application.status in ['draft', 'rejected']
        )

@login_required
def submit_application(request, pk):
    """Представление для подачи заявления"""
    application = get_object_or_404(Application, pk=pk)
    
    if application.applicant != request.user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для выполнения этого действия')
        return redirect('applications:application_list')
    
    if application.status not in ['draft', 'rejected']:
        messages.error(request, 'Это заявление уже подано')
        return redirect('applications:application_detail', pk=pk)
    
    if not application.scores.exists():
        messages.error(request, 'Необходимо указать баллы по предметам')
        return redirect('applications:application_update', pk=pk)
    
    application.status = 'submitted'
    application.submitted_at = timezone.now()
    application.save()
    
    messages.success(request, 'Заявление успешно подано')
    return redirect('applications:application_detail', pk=pk)

# @login_required
# def generate_pdf(request, pk):
#     """Представление для генерации PDF-версии заявления"""
#     application = get_object_or_404(Application, pk=pk)
#     if application.applicant != request.user and not request.user.is_staff:
#         messages.error(request, 'У вас нет прав для выполнения этого действия')
#         return redirect('application_list')
#     html_string = render_to_string('applications_app/application_pdf.html', {
#         'application': application,
#         'scores': application.scores.all(),
#     })
#     html = HTML(string=html_string)
#     pdf = html.write_pdf()
#     filename = f'application_{application.pk}_{application.get_full_name()}.pdf'
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response
