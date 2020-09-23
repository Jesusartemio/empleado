from django.db import models
from applications.departamento.models import Departamento

from ckeditor.fields import RichTextField


class Habilidades(models.Model):
    habilidad = models.CharField('Habilidad', max_length=50)

    class Meta:
        verbose_name = "Mi Habilidad"
        verbose_name_plural = "Habilidades de Empleado"

    def __str__(self):
        return str(self.id) + '-' + self.habilidad

class Empleado(models.Model):
    JOB_CHOISES = (
        ('0', 'CONTADOR'),
        ('1', 'ADMINISTRADOR'),
        ('2', 'ECONOMISTA'),
        ('3', 'OTRO'),
    )
    # Contador
    # Administrador
    # Economista
    # Otro
    first_name = models.CharField('Nombres', max_length=50)
    last_name = models.CharField('Apellidos', max_length=50)
    full_name = models.CharField(
        'Nombres Completos', 
        max_length=120,
        blank=True
    )
    job = models.CharField('Trabajo', max_length=1, choices=JOB_CHOISES)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='empleado', blank=True, null=True)
    habilidades = models.ManyToManyField(Habilidades)
    hoja_vida = RichTextField()

    class Meta:
        verbose_name = "Mi Empleado"
        verbose_name_plural = "Empleados de la empresa"
        ordering = ['-first_name','last_name']
        unique_together = ('first_name', 'departamento')

    def __str__(self):
        return str(self.id) + '-' + self.first_name + '-' + self.last_name