from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'animal_type', 'breed', 'age', 'owner_name', 'created_at']
    list_filter = ['animal_type', 'created_at']
    search_fields = ['name', 'owner_name', 'owner_phone']
    ordering = ['-created_at']