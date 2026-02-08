from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from patients.models import Patient
from .serializers import PatientSerializer
from appointments.models import Veterinarian, Appointment
from .serializers import VeterinarianSerializer, AppointmentSerializer
from medical_cards.models import MedicalRecord, Vaccination
from .serializers import MedicalRecordSerializer, VaccinationSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """Api for patients work"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Patient statistics"""
        total = Patient.objects.count()
        return Response({
            'total_patients': total,
            'message':'Api работает'
        })
    
class VeterinarianViewSet(viewsets.ModelViewSet):
    """API for veterinarian work"""
    queryset = Veterinarian.objects.filter(is_active=True)
    serializer_class = VeterinarianSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """API for working with appointment"""
    queryset = Appointment.objects.all().order_by('-appointment_date')
    serializer_class = AppointmentSerializer

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appoints"""
        from django.utils import timezone
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gt=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')

        serializer = self.get_serializer(upcoming_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today appoints"""
        from django.utils import timezone
        today = timezone.now().date()

        today_appointments = Appointment.objects.filter(
            appointment_date__date=today
        ).order_by('appointment_date')

        serializer = self.get_serializer(today_appointments, many=True)
        return Response(serializer.data)



class MedicalRecordViewSet(viewsets.ModelViewSet):
    """API for med cards working"""
    serializer_class = MedicalRecordSerializer
    queryset = MedicalRecord.objects.all().select_related('patient', 'veterinarian')
    
    def get_queryset(self):
        """filter by patient_id"""
        queryset = MedicalRecord.objects.all().select_related('patient', 'veterinarian')
        
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset.order_by('-record_date')
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        """Get common patient entry"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'Необходим параметр patient_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = MedicalRecord.objects.filter(patient_id=patient_id).order_by('-record_date')
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        records = MedicalRecord.objects.all().select_related('patient', 'veterinarian')[:10]
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

class VaccinationViewSet(viewsets.ModelViewSet):
    """API for vaccine working"""
    queryset = Vaccination.objects.all().select_related('patient', 'veterinarian')
    serializer_class = VaccinationSerializer
    
    @action(detail=False, methods=['get'])
    def due(self, request):
        from django.utils import timezone
        due_vaccinations = Vaccination.objects.filter(
            next_vaccination_date__lte=timezone.now().date()
        ).order_by('next_vaccination_date')
        
        serializer = self.get_serializer(due_vaccinations, many=True)
        return Response(serializer.data)