from django import forms
from .models import StudyProgram

class StudyProgramForm(forms.ModelForm):
    class Meta:
        model = StudyProgram
        fields = [
            'name',
            'code',
            'description',
            'education_form',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        } 