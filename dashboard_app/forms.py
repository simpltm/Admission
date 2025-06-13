from django import forms
from programs_app.models import StudyProgram
from django.forms import inlineformset_factory
class StudyProgramForm(forms.ModelForm):
    class Meta:
        model = StudyProgram
        fields = ['name', 'code', 'description', 'education_form']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        } 
        
