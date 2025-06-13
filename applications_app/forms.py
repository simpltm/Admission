from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Application, SubjectScore, ProgramPreference
from programs_app.models import StudyProgram, Subject
from django.forms.models import inlineformset_factory

class ProgramPreferenceForm(forms.ModelForm):
    """Форма для выбора направления подготовки"""
    class Meta:
        model = ProgramPreference
        fields = ['program', 'priority']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        program = cleaned_data.get('program')
        return cleaned_data

ProgramPreferenceFormSet = inlineformset_factory(
    Application,
    ProgramPreference,
    form=ProgramPreferenceForm,
    extra=5,
    max_num=5,
    min_num=1,
    can_delete=True,
    validate_min=True,
    validate_max=True
)

class ApplicationForm(forms.ModelForm):
    """Форма для создания и редактирования заявления"""
    class Meta:
        model = Application
        fields = [
            'first_name', 'last_name', 'middle_name',
            'passport_id', 'birth_date', 'phone', 'email', 'passport_scan',
            'notarized_passport_scan',
            'education_document', 'photo', 'education_form'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap ко всем полям
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.Select, forms.CheckboxInput)):
                field.widget.attrs.update({'class': 'form-control'})

    def clean_passport_id(self):
        """Проверка уникальности номера паспорта"""
        passport_id = self.cleaned_data['passport_id']
        if Application.objects.filter(passport_id=passport_id).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError('Заявление с таким номером паспорта уже существует')
        return passport_id

class SubjectScoreForm(forms.ModelForm):
    """Форма для ввода баллов по предметам"""
    class Meta:
        model = SubjectScore
        fields = ['subject', 'score']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }

SubjectScoreFormSet = inlineformset_factory(
    Application,
    SubjectScore,
    form=SubjectScoreForm,
    extra=2,
    can_delete=False,
) 