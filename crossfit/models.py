from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Bono(models.Model):
    tipo = models.CharField(max_length=30, unique=True)
    precio = models.FloatField(max_length=4)
    creditos_clase = models.PositiveSmallIntegerField()

    def __str__(self):
        return '[Tipo: ' + self.tipo + ' | Precio: ' + str(self.precio) + ' | Créditos Clase: ' + str(
            self.creditos_clase) + ']'

    def delete(self, *args, **kwargs):
        nPerfiles = Perfil.objects.filter(bono_id = self.pk )
        if(nPerfiles):
            for x in nPerfiles:
                x.fechaInicio = None
                x.fechaFin = None
                x.save()
        super(Bono,self).delete()

class Perfil(models.Model):
    Tipos_Sexo = (('H', 'Hombre',), ('M', 'Mujer',))

    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=25)
    apellido2 = models.CharField(max_length=25)
    dni = models.CharField(max_length=9)
    edad = models.PositiveSmallIntegerField()
    sexo = models.CharField(max_length=10, default='Hombre', choices=Tipos_Sexo)
    telefono = models.CharField(max_length=9,null=True, blank=True)
    foto = models.ImageField(upload_to='fotos', default='fotos/user.png', blank=True)
    ''' Relación con usuario '''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    '''Relación con Bono'''
    bono = models.ForeignKey(Bono, null=True, on_delete= models.SET_NULL , blank=True)
    fechaInicio = models.DateField(null=True, blank=True)
    fechaFin = models.DateField(null=True, blank=True)
    clase = models.ManyToManyField("Clase", through='Reservar')
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        if(self.telefono != None):
            return '[Nombre: ' + self.nombre + ' | Primer apellido: ' + self.apellido1 + ' | Segundo apellido: ' + self.apellido2 + ' | DNI: ' + self.dni + \
                   '\t\n | Sexo: ' + self.sexo + ' | Edad: ' + str(self.edad) +' | Teléfono: ' + self.telefono + ' ]'
        else:
            return '[Nombre: ' + self.nombre + ' | Primer apellido: ' + self.apellido1 + ' | Segundo apellido: ' + self.apellido2 + ' | DNI: ' + self.dni + \
                   '\t\n | Sexo: ' + self.sexo + ' | Edad: ' + str(self.edad) + ' ]'

class Clase(models.Model):
    capacidad_max = models.PositiveSmallIntegerField()
    m2 = models.FloatField()

    def __str__(self):
        return '[Clase:' + str(self.pk) + ' | Capacidad Máxima: ' + str(
            self.capacidad_max) + ' | Metros cuadrados: ' + str(self.m2) + ' ]'

''' Reservar clase intermedia entre Perfil y Clase'''

class Reservar(models.Model):
    atleta = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField(default = timezone.now)
    hora = models.TimeField(blank=True, null = True)

    def __str__(self):
        return '[Fecha:' + str(self.fecha) + ' | Hora:' + str(self.hora) + ' | Clase: ' + str(
            self.clase.pk) + ' | Atleta: ' + self.atleta.nombre + ' ]'
        
class Actividad(models.Model):
    tipo = models.CharField(max_length=50, unique=True)
    aforo = models.PositiveSmallIntegerField(default=6)

    def __str__(self):
        return '[Tipo: ' + self.tipo + ' | Aforo: ' + str(self.aforo) + ']'


class Horario(models.Model):
    Dias_Disponibles = (
    ('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'),
    ('Sábado', 'Sábado'), ('Domingo', 'Domingo'))
    diaSemana = models.CharField(max_length=12, default='Lunes', choices=Dias_Disponibles)
    horaInicio = models.TimeField(max_length=12)
    horaFin = models.TimeField(max_length=12)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, null = True)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return '[Día: ' + self.diaSemana + ' | Hora de inicio: ' + str(
            self.horaInicio) + ' | Hora de finalización: ' + str(self.horaFin) + ' | Actividad: ' + str(self.actividad.tipo) + \
             ' | Clase: ' + str(self.clase.pk) +']'

class Entreno(models.Model):
    nombre = models.CharField(max_length=30, unique = True)
    ejercicios = models.CharField(max_length=400)
    usuario = models.ForeignKey(Perfil, null=True, on_delete=models.SET_NULL, blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return '[Nombre: ' + self.nombre + ' | Ejercicios: ' + self.ejercicios  +']'


class Oficial(models.Model):
    categorias_Disponibles = (
    ('The Heroes', 'Héroes'), ('The Girls', 'Girls'))
    categoria = models.CharField(max_length = 20, default='The Heroes', choices=categorias_Disponibles)
    nombre = models.CharField(max_length = 30, unique = True)
    ejercicios = models.CharField(max_length = 400)
    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return '[Categoria : ' + self.categoria + ' | Ejercicios: ' + self.nombre + ' | Ejercicios: '+ self.ejercicios +']'
