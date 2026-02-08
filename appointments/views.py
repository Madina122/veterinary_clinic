from django.shortcuts import render
from django.views import View
from django.utils import timezone
from datetime import datetime, timedelta
from patients.models import Patient
from .models import Veterinarian, Appointment
from django.shortcuts import render, get_object_or_404


class BookAppointmentView(View):
    """Appoint form"""
    def get(self, request):
        """Show form"""
        today = timezone.now().date()
        
        patients = Patient.objects.all().order_by('name')
        veterinarians = Veterinarian.objects.filter(is_active=True).order_by('last_name')
        
        return render(request, 'appointments/book_appointment.html', {
            'patients': patients,
            'veterinarians': veterinarians,
            'today': today.strftime('%Y-%m-%d')
        })
    
    def post(self, request):
        """Zapis"""
        try:
            # Get info
            patient_id = request.POST.get('patient_id')
            veterinarian_id = request.POST.get('veterinarian_id')
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            reason = request.POST.get('reason', '')
            
            appointment_datetime = datetime.strptime(
                f"{date_str} {time_str}", 
                "%Y-%m-%d %H:%M"
            )
            
            # Create an antry
            appointment = Appointment.objects.create(
                patient_id=patient_id,
                veterinarian_id=veterinarian_id,
                appointment_date=appointment_datetime,
                reason=reason,
                status='scheduled'
            )
            
            return render(request, 'appointments/book_appointment.html', {
                'success': True,
                'appointment_id': appointment.id,
                'patients': Patient.objects.all(),
                'veterinarians': Veterinarian.objects.filter(is_active=True),
                'today': timezone.now().date().strftime('%Y-%m-%d')
            })
            
        except Exception as e:
            return render(request, 'appointments/book_appointment.html', {
                'error': str(e),
                'patients': Patient.objects.all(),
                'veterinarians': Veterinarian.objects.filter(is_active=True),
                'today': timezone.now().date().strftime('%Y-%m-%d')
            })

def appointment_detail(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment
    })