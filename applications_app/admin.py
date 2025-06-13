from django.contrib import admin
from django.utils.html import format_html
from .models import Application, SubjectScore, ProgramPreference

class SubjectScoreInline(admin.TabularInline):
    model = SubjectScore
    extra = 1
    min_num = 1

class ProgramPreferenceInline(admin.TabularInline):
    model = ProgramPreference
    extra = 1
    min_num = 1
    max_num = 5

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_program', 'total_score', 'created_at', 'submitted_at', 'get_documents')
    list_filter = ('program_preferences__program', 'created_at', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'middle_name', 'passport_id', 'email')
    readonly_fields = ('created_at', 'updated_at', 'submitted_at', 'total_score')
    inlines = [ProgramPreferenceInline, SubjectScoreInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('applicant',)
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'middle_name', 'passport_id',
                      'birth_date', 'phone', 'email')
        }),
        ('Документы', {
            'fields': ('passport_scan', 'education_document', 'photo')
        }),
        ('Баллы', {
            'fields': ('total_score',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'last_name'

    def get_program(self, obj):
        preference = obj.program_preferences.order_by('priority').first()
        return preference.program if preference else '-'
    get_program.short_description = 'Направление подготовки'
    get_program.admin_order_field = 'program_preferences__program'

    def get_documents(self, obj):
        docs = []
        if obj.passport_scan:
            docs.append('<a href="{}" target="_blank">Паспорт</a>'.format(obj.passport_scan.url))
        if obj.education_document:
            docs.append('<a href="{}" target="_blank">Образование</a>'.format(obj.education_document.url))
        if obj.photo:
            docs.append('<a href="{}" target="_blank">Фото</a>'.format(obj.photo.url))
        return format_html(' | '.join(docs))
    get_documents.short_description = 'Документы'

    def save_model(self, request, obj, form, change):
        if not change:  # Если это новое заявление
            obj.applicant = request.user
        if obj.status == 'submitted' and not obj.submitted_at:
            from django.utils import timezone
            obj.submitted_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(SubjectScore)
class SubjectScoreAdmin(admin.ModelAdmin):
    list_display = ('application', 'subject', 'score')
    list_filter = ('subject',)
    search_fields = ('application__first_name', 'application__last_name', 'subject__name')
    raw_id_fields = ('application', 'subject')

@admin.register(ProgramPreference)
class ProgramPreferenceAdmin(admin.ModelAdmin):
    list_display = ('application', 'program', 'priority')
    list_filter = ('program',)
    search_fields = ('application__first_name', 'application__last_name', 'program__name')
    raw_id_fields = ('application', 'program')
