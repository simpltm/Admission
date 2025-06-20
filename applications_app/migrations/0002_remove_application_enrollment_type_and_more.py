# Generated by Django 5.0.2 on 2025-06-12 08:30

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications_app', '0001_initial'),
        ('programs_app', '0002_studyprogram_education_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='enrollment_type',
        ),
        migrations.RemoveField(
            model_name='application',
            name='program',
        ),
        migrations.CreateModel(
            name='ProgramPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.PositiveIntegerField(help_text='Приоритет выбора (от 1 до 5)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Приоритет')),
                ('enrollment_type', models.CharField(choices=[('budget', 'Бюджет'), ('contract', 'Контракт')], default='budget', max_length=10, verbose_name='Тип приёма')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_preferences', to='applications_app.application', verbose_name='Заявление')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='preferences', to='programs_app.studyprogram', verbose_name='Направление подготовки')),
            ],
            options={
                'verbose_name': 'Предпочтение по направлению',
                'verbose_name_plural': 'Предпочтения по направлениям',
                'ordering': ['application', 'priority'],
            },
        ),
        migrations.AddConstraint(
            model_name='programpreference',
            constraint=models.UniqueConstraint(fields=('application', 'program'), name='unique_program_per_application'),
        ),
        migrations.AlterUniqueTogether(
            name='programpreference',
            unique_together={('application', 'priority')},
        ),
    ]
