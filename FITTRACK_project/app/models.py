from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50)
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname or self.username

class BodyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='body_data')
    weight = models.FloatField()
    height = models.FloatField()
    grasa_corporal = models.FloatField()
    liquido_corporal = models.FloatField()
    masa_muscular = models.FloatField()
    mesures_update = models.DateTimeField()

    class Meta:
        ordering = ['-mesures_update']

    def __str__(self):
        return f"Medidas de {self.user.nickname} - {self.mesures_update}"

class Training(models.Model):
    TIPO_ENTRENAMIENTO = [
        ('fuerza', 'Fuerza'),
        ('resistencia', 'Resistencia'),
        ('tecnica', 'Técnica'),
        ('partido', 'Partido'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainings')
    training_date = models.DateField()
    tipo_entrenamiento = models.CharField(max_length=20, choices=TIPO_ENTRENAMIENTO)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-training_date']

    def __str__(self):
        return f"{self.get_tipo_entrenamiento_display()} - {self.training_date}"
