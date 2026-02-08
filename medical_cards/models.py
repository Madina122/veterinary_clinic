from django.db import models
from patients.models import Patient
from appointments.models import Veterinarian, Appointment

class MedicalRecord(models.Model):
    """Medical entry"""
    RECORD_TYPES = [
        ('examination', 'Осмотр'),
        ('vaccination', 'Вакцинация'),
        ('surgery', 'Операция'),
        ('test', 'Анализ/Тест'),
        ('treatment', 'Лечение'),
        ('diagnostic', 'Диагностика'),
        ('prescription', 'Назначение'),
        ('other', 'Другое'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medical_records',
        verbose_name='Пациент'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='medical_records',
        verbose_name='Запись на прием'
    )
    veterinarian = models.ForeignKey(
        Veterinarian,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Ветеринар'
    )
    
    record_type = models.CharField(
        max_length=20,
        choices=RECORD_TYPES,
        default='examination',
        verbose_name='Тип записи'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    
    diagnosis = models.TextField(verbose_name='Диагноз', blank=True)
    symptoms = models.TextField(verbose_name='Симптомы', blank=True)
    treatment = models.TextField(verbose_name='Лечение/Назначения', blank=True)
    prescription = models.TextField(verbose_name='Рецепт', blank=True)
    
    record_date = models.DateTimeField(verbose_name='Дата записи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Температура (°C)'
    )
    weight = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Вес (кг)'
    )
    heart_rate = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Пульс (уд/мин)'
    )
    notes = models.TextField(verbose_name='Дополнительные заметки', blank=True)
    
    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
        ordering = ['-record_date']
        indexes = [
            models.Index(fields=['patient', 'record_date']),
            models.Index(fields=['record_type']),
        ]
    
    def __str__(self):
        return f"{self.patient.name} - {self.title} ({self.record_date.strftime('%d.%m.%Y')})"
    
    @property
    def is_vaccination(self):
        return self.record_type == 'vaccination'
    
    @property
    def is_surgery(self):
        return self.record_type == 'surgery'
    


class Vaccination(models.Model):
    """Vaccine"""
    VACCINE_TYPES = [
        ('rabies', 'Бешенство'),
        ('distemper', 'Чумка'),
        ('parvovirus', 'Парвовирус'),
        ('leptospirosis', 'Лептоспироз'),
        ('kennel_cough', 'Питомниковый кашель'),
        ('feline_leukaemia', 'Вирусный лейкоз кошек'),
        ('other', 'Другая'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        verbose_name='Пациент'
    )
    vaccine_type = models.CharField(
        max_length=50,
        choices=VACCINE_TYPES,
        verbose_name='Тип вакцины'
    )
    vaccine_name = models.CharField(max_length=200, verbose_name='Название вакцины')
    administration_date = models.DateField(verbose_name='Дата введения')
    next_vaccination_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата следующей вакцинации'
    )
    batch_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Номер партии'
    )
    veterinarian = models.ForeignKey(
        Veterinarian,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Ветеринар'
    )
    notes = models.TextField(verbose_name='Примечания', blank=True)
    
    class Meta:
        verbose_name = 'Вакцинация'
        verbose_name_plural = 'Вакцинации'
        ordering = ['-administration_date']
    
    def __str__(self):
        return f"{self.patient.name} - {self.get_vaccine_type_display()} ({self.administration_date})"
    
    @property
    def is_due(self):
        """Check vaccine date"""
        from django.utils import timezone
        if self.next_vaccination_date:
            return self.next_vaccination_date <= timezone.now().date()
        return False