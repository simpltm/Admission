from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

EDUCATION_FORM_CHOICES = [
    ('bachelor_full', 'Очная форма обучения бакалавриат'),
    ('specialist_full', 'Очная форма обучения специалитет'),
    ('master_full', 'Очная форма обучения магистратура'),
    ('master_part', 'Очно-заочная форма обучения магистратура'),
    ('bachelor_part', 'Заочная форма обучения бакалавриат'),
]

class StudyProgram(models.Model):
    """Модель для направления подготовки"""
    name = models.CharField('Название', max_length=200)
    code = models.CharField('Код направления', max_length=20, unique=True)
    description = models.TextField('Описание', blank=True)
    education_form = models.CharField('Форма обучения', max_length=32, choices=EDUCATION_FORM_CHOICES, default='bachelor_full')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"

class Subject(models.Model):
    """Модель для вступительных предметов"""
    name = models.CharField('Название предмета', max_length=100)
    code = models.CharField('Код предмета', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['name']

    def __str__(self):
        return self.name

class ProgramSubject(models.Model):
    """Модель для связи направления подготовки с предметами и минимальными баллами"""
    program = models.ForeignKey(StudyProgram, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    min_score = models.PositiveIntegerField(
        'Минимальный балл',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_required = models.BooleanField('Обязательный предмет', default=True)

    class Meta:
        verbose_name = 'Предмет направления'
        verbose_name_plural = 'Предметы направлений'
        unique_together = ['program', 'subject']
        ordering = ['program', 'subject']

    def __str__(self):
        return f"{self.program.code} - {self.subject.name} (мин. {self.min_score} баллов)"
