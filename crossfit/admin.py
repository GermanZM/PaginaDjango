from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from crossfit.models import Perfil,Bono,Clase,Reservar,Actividad,Horario, Entreno, Oficial
# Register your models here.

class PerfilStacked(admin.StackedInline):
	model = Perfil
	verbose_name_plural = 'Perfil'

class UserPAdmin(UserAdmin):
	inlines = (PerfilStacked, )

admin.site.unregister(User)
admin.site.register(User,UserPAdmin)

class HorarioStacked(admin.StackedInline):
	model = Horario
	verbose_name_plural = 'Horario'

class ActividadAdmin(admin.ModelAdmin):
	list_filter = ['aforo']
	ordering = ['aforo']
	list_per_page = 20
	search_fields = ['tipo']
	inlines = [HorarioStacked,]

admin.site.register(Actividad,ActividadAdmin)

class ValidarReservaAdmin(forms.ModelForm):
	
	def horas_permitidas():
		semanaH = Horario.objects.order_by('horaInicio')
		horas = []
		for h in semanaH:
			if(not h.horaInicio in horas):
				horas.append(h.horaInicio)

		return ((i, i) for i in horas)

	hora = forms.ChoiceField(choices= horas_permitidas())
	
	def clean_hora(self):
		if(self.cleaned_data['hora'] != None):
			diasSemana = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miércoles','THURSDAY':'Jueves', \
					  	  'FRIDAY':'Viernes','SATURDAY':'Sábado','SUNDAY':'Domingo'}
			dia = diasSemana[self.cleaned_data['fecha'].strftime('%A').upper()]
			existe = Horario.objects.filter(clase = self.cleaned_data['clase'], diaSemana = dia, horaInicio = self.cleaned_data['hora']).count()
			print(existe)
			if(existe == 1):
				return self.cleaned_data['hora']
			else:
				raise forms.ValidationError("Seleccione una clase y hora existente en el horario")

class ReservaAdmin(admin.ModelAdmin):
	form = ValidarReservaAdmin


admin.site.register(Reservar,ReservaAdmin)

class ValidarHorarioAdmin(forms.ModelForm):

	def clean_clase(self):
		if(self.cleaned_data['actividad'] != None):
			libres = Horario.objects.filter(horaInicio__range = (self.cleaned_data['horaInicio'] , self.cleaned_data['horaFin']) , \
				diaSemana = self.cleaned_data['diaSemana'] , clase = self.cleaned_data['clase'])
			print(libres)
			if(libres != True):
				return self.cleaned_data['clase']
			else:
				clases = Horario.objects.filter(horaInicio__range = (self.cleaned_data['horaInicio'] , self.cleaned_data['horaFin']) , \
				diaSemana =self.cleaned_data['diaSemana'] , clase = self.cleaned_data['clase'])
				for c in clases:
					if(c.horaInicio == self.cleaned_data['horaFin']):
						return self.cleaned_data['clase']
					else:
						raise forms.ValidationError("Está clase está ocupada ese día a esa hora")
			return self.cleaned_data['clase']
		else:
			raise forms.ValidationError("Debes de seleccionar una actividad")

	def clean_actividad(self):
		if(self.cleaned_data['actividad'] == None):
			raise forms.ValidationError("Debes de seleccionar una actividad")

class HorarioAdmin(admin.ModelAdmin):
	form = ValidarHorarioAdmin

admin.site.register(Horario,HorarioAdmin)

admin.site.register(Bono)
admin.site.register(Clase)
admin.site.register(Entreno)
admin.site.register(Oficial)
