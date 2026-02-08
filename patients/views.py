from django.shortcuts import render, redirect
from django.views import View
from .models import Patient
from django.views.generic import ListView
from django.views.generic import TemplateView
from medical_cards.models import Vaccination
from django.utils import timezone

class HomeView(TemplateView):
    """The main page"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from patients.models import Patient
        from appointments.models import Appointment
        
        context['total_patients'] = Patient.objects.count()
        
        #today entrys
        today = timezone.now().date()
        context['today_appointments'] = Appointment.objects.filter(
            appointment_date__date=today,
            status__in=['scheduled', 'confirmed']
        ).count()
        
        # upcoming entrys
        context['upcoming_appointments'] = Appointment.objects.filter(
            appointment_date__gt=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).select_related('patient', 'veterinarian')[:5]
        
        # Vaccine
        context['total_vaccinations'] = Vaccination.objects.count()
        
        from django.db.models import Count
        context['patients_by_type'] = Patient.objects.values(
            'animal_type'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        return context

class AddPatientView(View):

    """Veb-forms for new patient adding"""

    def get(self, request):
        """Show empty form"""
        return render(request, 'patients/add_patient.html')
    
    def post(self, request):
        """Work with form"""
        try:
            patient = Patient.objects.create(
                name = request.POST.get('name'),
                animal_type = request.POST.get('animal_type'),
                breed=request.POST.get('breed', ''),
                age = int(request.POST.get('age', 0)),
                owner_name = request.POST.get('owner_name'),
                owner_phone = request.POST.get('owner_phone'),
            )

            return render(request, 'patients/add_patient.html', {
                'success': True,
                'patient_id': patient.id
            })
        except Exception as e:
            return render(request, 'patients/add_patient.html', {
                'error': f'Ошибка: {str(e)}'
            })

class PatientListView(ListView):
    """Patient list"""
    model=Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']