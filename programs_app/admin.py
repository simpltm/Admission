from django.contrib import admin
from .models import StudyProgram, Subject, ProgramSubject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

class ProgramSubjectInline(admin.TabularInline):
    model = ProgramSubject
    extra = 1
    min_num = 1

@admin.register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProgramSubjectInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'description')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
