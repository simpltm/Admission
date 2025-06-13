from django.apps import AppConfig
from django.db import OperationalError


class ApplicationsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications_app'

    def ready(self):
        try:
            from .models import Subject
            Subject.objects.get_or_create(name='Русский язык')
        except OperationalError:
            # Ma'lumotlar bazasi jadvallari yaratilmaganda xatolikni e'tiborsiz qoldirish
            pass
