from rest_framework import serializers
from patients.models import Patient
from appointments.models import Veterinarian, Appointment
from medical_cards.models import MedicalRecord, Vaccination


class PatientSerializer(serializers.ModelSerializer):
    animal_type_display = serializers.CharField(
        source='get_animal_type_display',
        read_only=True
    )

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'animal_type', 'animal_type_display',
            'breed', 'age', 'owner_name', 'owner_phone', 'created_at'
        ]
        read_only_fields = ['created_at']

class VeterinarianSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(
        source = 'get_specialization_display',
        read_only= True
    )

    class Meta:
        model = Veterinarian
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'specialization', 'specialization_display',
            'phone', 'email', 'experience_years', 'is_active'
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source = 'patient.name', read_only=True)
    veterinarian_name = serializers.CharField(source='veterinarian.full_name', read_only = True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields=[
            'id', 'patient', 'patient_name', 'veterinarian', 'veterinarian_name',
            'appointment_date', 'reason', 'diagnosis', 'treatment',
            'status', 'status_display', 'created_at', 'updated_at',
            'is_upcoming', 'duration_minutes'
        ]
        read_only_fields = ['created_at', 'updated_at']


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    veterinarian_name = serializers.CharField(source='veterinarian.full_name', read_only=True)
    record_type_display = serializers.CharField(source='get_record_type_display', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'appointment', 'veterinarian', 'veterinarian_name',
            'record_type', 'record_type_display', 'title', 'description',
            'symptoms', 'diagnosis', 'treatment', 'prescription',
            'temperature', 'weight', 'heart_rate',
            'record_date', 'created_at', 'notes'
        ]
        read_only_fields = ['created_at']

class VaccinationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    veterinarian_name = serializers.CharField(source='veterinarian.full_name', read_only=True)
    vaccine_type_display = serializers.CharField(source='get_vaccine_type_display', read_only=True)
    is_due = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Vaccination
        fields = [
            'id', 'patient', 'patient_name', 'vaccine_type', 'vaccine_type_display',
            'vaccine_name', 'administration_date', 'next_vaccination_date',
            'batch_number', 'veterinarian', 'veterinarian_name',
            'notes', 'is_due'
        ]