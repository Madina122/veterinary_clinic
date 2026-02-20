from django.db import models
from patients.models import Patient

class Veterinarian(models.Model):
    """Vet doctor"""
    SPECIALIZATIONS = [
        ('general', 'Общая практика'),
        ('surgeon', 'Хирург'),
        ('dentist', 'Стоматолог'),
        ('dermatologist', 'Дерматолог'),
        ('ophthalmologist', 'Офтальмолог'),
        ('cardiologist', 'Кардиолог'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    specialization = models.CharField(
        max_length=50, 
        choices=SPECIALIZATIONS,
        default='general',
        verbose_name='Специализация'
    )
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    experience_years = models.IntegerField(default=0, verbose_name='Стаж (лет)')
    is_active = models.BooleanField(default=True, verbose_name='Работает')
    
    class Meta:
        verbose_name = 'Ветеринар'
        verbose_name_plural = 'Ветеринары'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"Доктор {self.last_name} {self.first_name} ({self.get_specialization_display()})"
    
    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"
    

class Appointment(models.Model):
    """Запись на прием к ветеринару"""
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('confirmed', 'Подтвержден'),
        ('in_progress', 'На приеме'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
        ('no_show', 'Не явился'),
    ]
    
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пациент'
    )
    veterinarian = models.ForeignKey(
        Veterinarian,
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='Ветеринар'
    )
    appointment_date = models.DateTimeField(verbose_name='Дата и время приема')
    reason = models.TextField(verbose_name='Причина обращения', blank=True)
    diagnosis = models.TextField(verbose_name='Диагноз', blank=True)
    treatment = models.TextField(verbose_name='Назначенное лечение', blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-appointment_date']
        indexes = [
            models.Index(fields=['appointment_date', 'status']),
            models.Index(fields=['patient', 'veterinarian']),
        ]
    
    def __str__(self):
        return f"{self.patient.name} → {self.veterinarian} ({self.appointment_date.strftime('%d.%m.%Y %H:%M')})"
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.appointment_date > timezone.now() and self.status in ['scheduled', 'confirmed']
    
    @property
    def duration_minutes(self):
        """Продолжительность приема"""
        return 30 
