from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from programs_app.models import StudyProgram, Subject, EDUCATION_FORM_CHOICES

class ProgramPreference(models.Model):
    """Модель для предпочтений по направлениям подготовки"""
    application = models.ForeignKey(
        'Application',
        on_delete=models.CASCADE,
        related_name='program_preferences',
        verbose_name='Заявление'
    )
    program = models.ForeignKey(
        StudyProgram,
        on_delete=models.PROTECT,
        related_name='preferences',
        verbose_name='Направление подготовки'
    )
    priority = models.PositiveIntegerField(
        'Приоритет',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Приоритет выбора (от 1 до 5)'
    )

    class Meta:
        verbose_name = 'Предпочтение по направлению'
        verbose_name_plural = 'Предпочтения по направлениям'
        ordering = ['application', 'priority']
        unique_together = ['application', 'priority']
        constraints = [
            models.UniqueConstraint(
                fields=['application', 'program'],
                name='unique_program_per_application'
            )
        ]

    def __str__(self):
        return f"{self.application} - {self.program} (приоритет {self.priority})"

class Application(models.Model):
    """Модель для заявления абитуриента"""
    # STATUS_CHOICES = [ ... ]  # Remove this

    # Основная информация
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Абитуриент'
    )

    # Личные данные
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    middle_name = models.CharField('Отчество', max_length=100, blank=True)
    passport_id = models.CharField('Номер паспорта', max_length=20, unique=True)
    birth_date = models.DateField('Дата рождения')
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField('Email')
    education_form = models.CharField('Форма обучения', max_length=32, choices=EDUCATION_FORM_CHOICES, default='bachelor_full')

    # Документы
    passport_scan = models.FileField('Скан паспорта', upload_to='passports/', blank=True, null=True)
    notarized_passport_scan = models.FileField('Нотариальный перевод ID карты/паспорта', upload_to='notarized_passports/', blank=True, null=True)
    education_document = models.FileField('Документ об образовании', upload_to='education/')
    photo = models.ImageField('Фотография', upload_to='photos/')

    # Баллы
    total_score = models.PositiveIntegerField(
        'Общий балл',
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        null=True,
        blank=True
    )

    # Метаданные
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    submitted_at = models.DateTimeField('Дата подачи', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявление {self.applicant.get_full_name()}"

    def get_full_name(self):
        """Возвращает полное имя абитуриента"""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    @property
    def selected_program(self):
        """Возвращает выбранное направление с наивысшим приоритетом"""
        return self.program_preferences.order_by('priority').first()

class SubjectScore(models.Model):
    """Модель для хранения баллов по предметам"""
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Заявление'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='Предмет'
    )
    score = models.PositiveIntegerField(
        'Балл',
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = 'Балл по предмету'
        verbose_name_plural = 'Баллы по предметам'
        unique_together = ['application', 'subject']
        ordering = ['subject']

    def __str__(self):
        return f"{self.application.get_full_name()} - {self.subject.name}: {self.score}"

    def save(self, *args, **kwargs):
        """Переопределяем метод save для обновления общего балла"""
        super().save(*args, **kwargs)
        self.update_total_score()

    def update_total_score(self):
        """Обновляет общий балл заявления"""
        total = sum(score.score for score in self.application.scores.all())
        self.application.total_score = total
        self.application.save()

class ApplicationPhoto(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField('Rasm', upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'
        ordering = ['uploaded_at']

    def __str__(self):
        return f"{self.application} - {self.image.name}"

Subject.objects.get_or_create(name='Русский язык')
Subject.objects.get_or_create(name='Химия')

print(list(Subject.objects.values_list('name', flat=True)))
