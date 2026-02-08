from django.db import models

class Patient(models.Model):
    ANIMAL_TYPES = [
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
        ('bird', 'Птица'),
        ('rabbit', 'Кролик'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=100, verbose_name='Кличка животного')
    animal_type = models.CharField(
        max_length=20,
        choices=ANIMAL_TYPES,
        verbose_name='Вид животного'
    )

    breed = models.CharField(max_length=100, blank=True, verbose_name='Порода')
    age = models.IntegerField(verbose_name='Возвраст')
    owner_name = models.CharField(max_length=100, verbose_name='Имя владельца')
    owner_phone = models.CharField(max_length=20, verbose_name='Телефон владельца')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_animal_type_display()})"
    
