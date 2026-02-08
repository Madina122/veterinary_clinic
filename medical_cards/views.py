from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from datetime import datetime
from patients.models import Patient
from appointments.models import Veterinarian
from .models import MedicalRecord, Vaccination

class PatientMedicalCardView(View):
    """View patient med card"""
    
    def get(self, request, patient_id):
        """Show"""
        patient = get_object_or_404(Patient, id=patient_id)
        
        medical_records = MedicalRecord.objects.filter(
            patient=patient
        ).select_related('veterinarian').order_by('-record_date')
        
        vaccinations = Vaccination.objects.filter(
            patient=patient
        ).select_related('veterinarian').order_by('-administration_date')
        
        upcoming_vaccinations = [
            v for v in vaccinations 
            if v.next_vaccination_date and v.next_vaccination_date >= timezone.now().date()
        ]
        
        return render(request, 'medical_cards/patient_medical_card.html', {
            'patient': patient,
            'medical_records': medical_records,
            'vaccinations': vaccinations,
            'upcoming_vaccinations': upcoming_vaccinations,
        })

class AddMedicalRecordView(View):
    """Adding med record"""
    
    def post(self, request, patient_id):
        try:
            patient = get_object_or_404(Patient, id=patient_id)
            
            record = MedicalRecord.objects.create(
                patient=patient,
                record_type=request.POST.get('record_type'),
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                temperature=request.POST.get('temperature') or None,
                weight=request.POST.get('weight') or None,
                record_date=datetime.fromisoformat(request.POST.get('record_date')),
                notes=request.POST.get('notes', '')
            )
            
            return redirect(f'/medical/{patient_id}/?success=true&record_id={record.id}')
            
        except Exception as e:
            return redirect(f'/medical/{patient_id}/?error={str(e)}')