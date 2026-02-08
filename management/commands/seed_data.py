
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from patients.models import Patient
from appointments.models import Veterinarian, Appointment
from medical_cards.models import MedicalRecord, Vaccination

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        Patient.objects.all().delete()
        Veterinarian.objects.all().delete()
        
        vets = [
            Veterinarian(
                first_name='Анна',
                last_name='Иванова',
                specialization='surgeon',
                phone='+7 (999) 111-22-33',
                email='anna@vetclinic.ru',
                experience_years=5
            ),
            Veterinarian(
                first_name='Петр',
                last_name='Сидоров',
                specialization='general',
                phone='+7 (999) 222-33-44',
                email='petr@vetclinic.ru',
                experience_years=8
            ),
            Veterinarian(
                first_name='Мария',
                last_name='Петрова',
                specialization='dermatologist',
                phone='+7 (999) 333-44-55',
                email='maria@vetclinic.ru',
                experience_years=3
            ),
        ]
        
        for vet in vets:
            vet.save()
        
        
        patients_data = [
            {
                'name': 'Барсик',
                'animal_type': 'cat',
                'breed': 'Сиамский',
                'age': 3,
                'owner_name': 'Ирина Смирнова',
                'owner_phone': '+7 (999) 444-55-66',
            },
            {
                'name': 'Шарик',
                'animal_type': 'dog',
                'breed': 'Немецкая овчарка',
                'age': 5,
                'owner_name': 'Алексей Козлов',
                'owner_phone': '+7 (999) 555-66-77',
            },
            {
                'name': 'Кеша',
                'animal_type': 'bird',
                'breed': 'Волнистый попугай',
                'age': 2,
                'owner_name': 'Ольга Новикова',
                'owner_phone': '+7 (999) 666-77-88',
            },
            {
                'name': 'Пушистик',
                'animal_type': 'rabbit',
                'breed': 'Карликовый кролик',
                'age': 1,
                'owner_name': 'Дмитрий Волков',
                'owner_phone': '+7 (999) 777-88-99',
            },
            {
                'name': 'Рекс',
                'animal_type': 'dog',
                'breed': 'Лабрадор',
                'age': 4,
                'owner_name': 'Сергей Морозов',
                'owner_phone': '+7 (999) 888-99-00',
            },
        ]
        
        patients = []
        for data in patients_data:
            patient = Patient.objects.create(**data)
            patients.append(patient)
        
        appointments = []
        today = timezone.now()
        
        for i, patient in enumerate(patients):
            vet = vets[i % len(vets)]
            appointment_date = today + timedelta(days=i+1, hours=10)
            
            appointment = Appointment.objects.create(
                patient=patient,
                veterinarian=vet,
                appointment_date=appointment_date,
                reason=f'Плановый осмотр {patient.name}',
                status='scheduled'
            )
            appointments.append(appointment)
        
        medical_records = []
        for i, patient in enumerate(patients):
            vet = vets[i % len(vets)]
            
            record = MedicalRecord.objects.create(
                patient=patient,
                veterinarian=vet,
                record_type='examination',
                title=f'Первичный осмотр {patient.name}',
                description=f'{patient.name} был осмотрен впервые. Общее состояние удовлетворительное.',
                diagnosis='Здоров',
                treatment='Рекомендовано плановое наблюдение',
                temperature=38.5 if patient.animal_type == 'dog' else 38.0,
                weight=patient.age * 2 + 5,
                record_date=today - timedelta(days=30-i)
            )
            medical_records.append(record)
        
        vaccines = []
        for i, patient in enumerate(patients[:3]): 
            vet = vets[i % len(vets)]
            
            vaccine = Vaccination.objects.create(
                patient=patient,
                vaccine_type='rabies' if i == 0 else ('distemper' if i == 1 else 'parvovirus'),
                vaccine_name=f'Вакцина {"А" if i == 0 else "Б" if i == 1 else "В"}',
                administration_date=today - timedelta(days=60-i*10),
                next_vaccination_date=today + timedelta(days=180),
                veterinarian=vet,
                notes=f'Вакцинация прошла успешно. {patient.name} чувствует себя хорошо.'
            )
            vaccines.append(vaccine)
        