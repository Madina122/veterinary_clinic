from django.contrib import admin
from .models import Veterinarian, Appointment

@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'specialization', 'experience_years', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['last_name', 'first_name', 'email']
    list_editable = ['is_active']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'veterinarian', 'appointment_date', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'veterinarian']
    search_fields = ['patient__name', 'veterinarian__last_name', 'reason']
    date_hierarchy = 'appointment_date'
    ordering = ['-appointment_date']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('patient', 'veterinarian', 'appointment_date', 'status')
        }),
        ('Медицинская информация', {
            'fields': ('reason', 'diagnosis', 'treatment'),
            'classes': ('collapse',)
        }),
    )