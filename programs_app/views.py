from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import StudyProgram
from .forms import StudyProgramForm
from django.views.generic import ListView

# Create your views here.

class ProgramCreateView(CreateView):
    model = StudyProgram
    form_class = StudyProgramForm
    template_name = 'programs_app/program_form.html'
    success_url = reverse_lazy('programs_app:program_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

class ProgramUpdateView(UpdateView):
    model = StudyProgram
    form_class = StudyProgramForm
    template_name = 'programs_app/program_form.html'
    success_url = reverse_lazy('programs_app:program_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

class ProgramListView(ListView):
    model = StudyProgram
    template_name = 'programs_app/program_list.html'
    context_object_name = 'programs'
