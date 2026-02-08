from django.contrib import admin
from .models import MedicalRecord, Vaccination

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'record_type', 'title', 'record_date', 'veterinarian']
    list_filter = ['record_type', 'record_date', 'patient']
    search_fields = ['patient__name', 'title', 'diagnosis']
    date_hierarchy = 'record_date'
    ordering = ['-record_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('patient', 'appointment', 'veterinarian', 'record_type', 'title')
        }),
        ('Медицинская информация', {
            'fields': ('description', 'symptoms', 'diagnosis', 'treatment', 'prescription')
        }),
        ('Показатели', {
            'fields': ('temperature', 'weight', 'heart_rate'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('record_date',),
        }),
        ('Дополнительно', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'veterinarian')

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'vaccine_type', 'vaccine_name', 'administration_date', 'is_due']
    list_filter = ['vaccine_type', 'administration_date']
    search_fields = ['patient__name', 'vaccine_name', 'batch_number']
    date_hierarchy = 'administration_date'
    
    def is_due(self, obj):
        return obj.is_due
    is_due.boolean = True
    is_due.short_description = 'Пора делать?'