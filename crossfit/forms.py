from django import forms
from django.forms import ModelForm , Textarea
from crossfit.models import Perfil , Entreno , Reservar
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator
import os

# Definición de nuestros formularios

# Formulario de registro de un atleta (User y Perfil)
class registroForm(forms.Form):
    username = forms.CharField(max_length=80, label = 'Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label = 'Contraseña',max_length=50)
    email = forms.EmailField(label = 'Email',max_length=100)
    nombre = forms.CharField(max_length=20,label = 'Nombre')
    apellido1 = forms.CharField(max_length=25,label = 'Apellido1')
    apellido2 = forms.CharField(max_length=25,label = 'Apellido2')
    edad = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    dni = forms.CharField(max_length=9,label = 'DNI')
    sexo = forms.ChoiceField(choices = (('H', 'Hombre',), ('M', 'Mujer',)))
    telefono = forms.CharField(max_length=9, label = 'Teléfono', required = False)
    imagen = forms.ImageField(required = False, widget= forms.FileInput)

    def clean_dni(self):
    	if(len(self.data['dni']) < 9):
    		raise forms.ValidationError("DNI demasiado corto")
    	else:
	    	for i in self.data['dni'][0:-1]:
	    		if(not i.isdigit()):
	    			raise forms.ValidationError("DNI incorrecto")
	    	if(self.data['dni'][-1].isdigit()):
	    		raise forms.ValidationError("DNI incorrecto (se esperaba una letra)")
    	return self.cleaned_data['dni']

    def clean_foto(self):
        if(self.data['imagen']):
            extensiones = ['png','jpg','jpeg']
            ext = os.path.splitext(self.data['imagen'])[1].split('.')[1]
            if(not ext.lower() in extensiones):
                raise forms.ValidationError("Debes de añadir una foto válida (PNG | JPG | JPEG)")
        return self.cleaned_data['imagen']

    def clean_password(self):
    	if(len(self.data['password']) < 8):
    		raise forms.ValidationError("Contraseña demasiado corta (Mínimo 8 caracteres)")
    	elif(self.data['password'][0] == " "):
    		raise forms.ValidationError("Contraseña errónea")
    	else:
	    	for x in self.data['password']:
	    		if(x == " "):
	    			raise forms.ValidationError("Contraseña errónea, no puede contener espacios")
    	return self.cleaned_data['password']

    def clean_telefono(self):
    	if(len(self.data['telefono']) < 9):
    		raise forms.ValidationError("Teléfono incorrecto")
    	else:
    		for i in self.data['telefono']:
	    		if(not i.isdigit()):
	    			raise forms.ValidationError("Teléfono incorrecto, solo se aceptan números")
    	return self.cleaned_data['telefono']

    def clean(self):
    	cleaned_data = self.cleaned_data
    	return cleaned_data

# Formulario para el envío de un nuevo correo desde login
class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=50, required = True)
    email = forms.EmailField(max_length=100, required = True)
    asunto = forms.ChoiceField(choices = (('Consulta', 'Consulta general',),('Problema al reservar', 'Problema al realizar una reserva',),
        ('Día de prueba', 'Quiero llevar a un amigo',)))
    contenido = forms.CharField(max_length=520 ,widget = forms.Textarea)

# Formulario para definir un nuevo entreno.
class NuevoEntrenoForm(forms.ModelForm):
    class Meta:
        model = Entreno
        fields = '__all__'
        exclude = ['usuario']
        widgets = {
            'ejercicios': Textarea(attrs={'cols': 80, 'rows': 8,'style':'resize:none;'}),
        }
        labels = {
            'nombre' : ('Entreno'),
            'ejercicios' : ('Serie de ejercicios'),
        }
        help_texts = {
            'nombre' : ('Define un nombre característico para tu entreno'),
            'ejercicios': ('Define tus propios ejercicios'),
        }

# Formulario para modificar un perfil
class modPerfil(forms.Form):
    nombre = forms.CharField(max_length=20,label = 'Nombre')
    apellido1 = forms.CharField(max_length=25,label = 'Apellido1')
    apellido2 = forms.CharField(max_length=25,label = 'Apellido2')
    edad = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    dni = forms.CharField(max_length=9,label = 'DNI')
    sexo = forms.ChoiceField(choices = (('H', 'Hombre',), ('M', 'Mujer',)))
    telefono = forms.CharField(max_length=9, label = 'Teléfono', required = False)
    imagen = forms.ImageField(required = False, widget= forms.FileInput)

    def clean_dni(self):
        if(len(self.data['dni']) < 9):
            raise forms.ValidationError("DNI demasiado corto")
        else:
            for i in self.data['dni'][0:-1]:
                if(not i.isdigit()):
                    raise forms.ValidationError("DNI incorrecto")
            if(self.data['dni'][-1].isdigit()):
                raise forms.ValidationError("DNI incorrecto (se esperaba una letra)")
        return self.cleaned_data['dni']

    def clean_telefono(self):
        if(len(self.data['telefono']) < 9):
            raise forms.ValidationError("Teléfono incorrecto")
        else:
            for i in self.data['telefono']:
                if(not i.isdigit()):
                    raise forms.ValidationError("Teléfono incorrecto, solo se aceptan números")
        return self.cleaned_data['telefono']

    def clean_foto(self):
        if(self.data['imagen']):
            extensiones = ['png','jpg','jpeg']
            ext = os.path.splitext(self.data['imagen'])[1].split('.')[1]
            if(not ext.lower() in extensiones):
                raise forms.ValidationError("Debes de añadir una foto válida (PNG | JPG | JPEG)")
        return self.cleaned_data['imagen']

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data
