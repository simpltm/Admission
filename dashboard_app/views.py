from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from programs_app.models import StudyProgram
from .forms import StudyProgramForm
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    """Представление для панели управления администратора"""
    education_form_filter = request.GET.get('education_form', '')
    programs = StudyProgram.objects.all().order_by('-id')
    if education_form_filter:
        programs = programs.filter(education_form=education_form_filter)
    form = StudyProgramForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard_app/dashboard.html', {
        'form': form,
        'programs': programs,
        'education_form_filter': education_form_filter,
        'education_form_choices': StudyProgram._meta.get_field('education_form').choices,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
@xframe_options_exempt
def edit_program(request, pk):
    program = get_object_or_404(StudyProgram, pk=pk)
    if request.method == 'POST':
        form = StudyProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    else:
        form = StudyProgramForm(instance=program)
    return render(request, 'dashboard_app/edit_program_form.html', {'form': form, 'program': program})

@login_required
@user_passes_test(lambda u: u.is_staff)
@xframe_options_exempt
def delete_program(request, pk):
    program = get_object_or_404(StudyProgram, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('dashboard:dashboard')
    return render(request, 'dashboard_app/delete_program_confirm.html', {'program': program})
