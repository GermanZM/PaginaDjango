from django.shortcuts import render, render_to_response
from django.views.generic import View,TemplateView, ListView, DetailView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from crossfit.forms import registroForm, ContactoForm, NuevoEntrenoForm, modPerfil
from django.contrib.auth.models import User
from crossfit.models import Perfil,Bono, Horario, Reservar, Actividad, Oficial, Entreno, Clase
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import login,logout
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime,timedelta

# Create your views here.
#Vista Index de la página web
class Principal(TemplateView):
	template_name = "index.html"

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['usuarios'] = User.objects.filter(is_staff = False)
		reservas = Reservar.objects.all()
		horario = Horario.objects.all()
		diasSemana = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miércoles','THURSDAY':'Jueves', \
					  'FRIDAY':'Viernes','SATURDAY':'Sábado','SUNDAY':'Domingo'}
		nCrossfit = 0
		for r in reservas:
			for h in horario:
				if(r.clase.pk == h.clase.pk and h.actividad.tipo.lower() == 'crossfit'
					and r.hora.strftime('%H:%M') == h.horaInicio.strftime('%H:%M')
					and diasSemana[r.fecha.strftime('%A').upper()] == h.diaSemana):
					nCrossfit = nCrossfit + 1

		context['nClases'] = nCrossfit
		return context

#Función de logout y que te redireccione al index
def logoutUsuario(request):
	logout(request)
	return HttpResponseRedirect('/crossfit/index')

#Muestra todas las tarifas existentes
def Tarifas(request):
	bonos = Bono.objects.order_by('tipo')
	context = {'tarifas': bonos}
	return render(request,'tarifas.html',context)

#Muestra el horario definido
def mostrarHorario(request):
	semanaH = Horario.objects.order_by('horaInicio')
	diaSemana = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
	horas = []
	for h in semanaH:
		if(not h.horaInicio in horas):
			horas.append(h.horaInicio)
	print(horas)
	horarioT = []
	for d in diaSemana:
		horarioT.append(Horario.objects.filter(diaSemana = d))

	context = {'horario': horarioT, 'horas':horas}
	return render(request,'horario.html',context)

#Nos permite añadir un nuevo atleta
def nuevoRegistro(request):
	if request.method == 'POST':
		form = registroForm(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			n_username = cd['username']
			n_password = cd['password']
			n_email = cd['email']
			n_nombre = cd['nombre']
			n_apellido1 = cd['apellido1']
			n_apellido2 = cd['apellido2']
			n_dni = cd['dni']
			n_sexo = cd['sexo']
			n_telefono = cd['telefono']
			n_foto = cd['imagen']
			n_edad = cd['edad']
			if(n_foto == None):
				n_foto = 'fotos/user.png'
			user = User(username = n_username,email = n_email)
			user.set_password(n_password)
			user.save()
			perfil = Perfil( nombre = n_nombre, apellido1 = n_apellido1, apellido2 = n_apellido2,
				dni = n_dni, sexo = n_sexo, telefono = n_telefono, foto = n_foto, edad = n_edad, usuario = user)
			perfil.save()
			messages.success(request, 'Registro realizado correctamente')
			return HttpResponseRedirect('/crossfit/login')
	else:
		form = registroForm()
	return render(request,'registro.html',{'form':form})

#Index de la zona privada, solo se puede acceder si está logueado
@login_required
def Privada(request):
	try:
		perfil = Perfil.objects.get(usuario = request.user.pk)
		context = {'perfil':perfil}
		return render(request,'zonaPrivada/zonaPrivada.html',context)
	except Exception as e:
		raise
	return render(request,'zonaPrivada/zonaPrivada.html')
	
#Nos permite contactar con el dueño del Box mediante correo
@login_required
def Contactar(request):
	try:
		perfil = Perfil.objects.get(usuario = request.user.pk)
		context = {'perfil':perfil}
		if request.method == 'POST':
			form = ContactoForm(request.POST)
			if form.is_valid():
				data = form.cleaned_data
				nombre = data['nombre']
				email = data['email']
				asunto = data['asunto']
				contenido = data['contenido']
				contenidoFINAL = 'Nombre: ' + nombre + '\n' + 'Correo electrónico: ' + email + '\n \n' + contenido
				send_mail(
					asunto,
				    contenidoFINAL,
					email,
				    ['germanaplication@gmail.com'],
				    fail_silently=False,
				)
				messages.success(request, 'Correo enviado correctamente')
				return HttpResponseRedirect('/crossfit/privada/contacto')
		else:
			form = ContactoForm()
			context['form'] = form
		return render(request, 'zonaPrivada/contacto.html', context)
	except Exception as e:
		raise
	return render(request,'zonaPrivada/contacto.html')

#Vista que nos permite mostrar información de todos los atletas
@method_decorator(login_required, name='dispatch')
class mostrarAtletas(ListView):
	model = Perfil
	template_name = "zonaPrivada/mostrarAtletas.html"

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			paginador = Paginator(context['object_list'], 10)
			actual = self.request.GET.get('page')
			informacionAtletas = paginador.get_page(actual)
			context['object_list'] = informacionAtletas
			return context
		except Exception as e:
			raise

#Nos muestra la información de un atleta en concreto
@method_decorator(login_required, name='dispatch')
class atletaSeleccionado(DetailView):
	model = Perfil
	template_name = 'zonaPrivada/infoAtleta.html'

#Vista Benchmarck
@method_decorator(login_required, name='dispatch')
class Benchmarks(TemplateView):
	template_name = 'zonaPrivada/benchmarks.html'

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			return context
		except Exception as e:
			raise

#Vista que nos permite mostrar información The Girls
@method_decorator(login_required, name='dispatch')
class mostrarGirl(ListView):
	model = Oficial
	template_name = "zonaPrivada/girls.html"

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			context['object_list'] = Oficial.objects.filter(categoria = 'The Girls')
			paginador = Paginator(context['object_list'], 14)
			actual = self.request.GET.get('page')
			entrenosGirls = paginador.get_page(actual)
			context['object_list'] = entrenosGirls
			return context
		except Exception as e:
			raise

#Vista que nos permite mostrar información The Heroes
@method_decorator(login_required, name='dispatch')
class mostrarHeroes(ListView):
	model = Oficial
	template_name = "zonaPrivada/heroes.html"

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			context['object_list'] = Oficial.objects.filter(categoria = 'The Heroes')
			paginador = Paginator(context['object_list'], 14)
			actual = self.request.GET.get('page')
			entrenosHeroes = paginador.get_page(actual)
			context['object_list'] = entrenosHeroes
			return context
		except Exception as e:
			raise

#Nos muestra la información de un entreno oficial en concreto
@method_decorator(login_required, name='dispatch')
class oficialSeleccionado(DetailView):
	model = Oficial
	template_name = 'zonaPrivada/entrenoOficial.html'

#Registro de un nuevo entreno
@method_decorator(login_required, name='dispatch')
class NuevoEntreno(View):
	def get(self,request):
		form = NuevoEntrenoForm()
		perfilA = Perfil.objects.get(usuario = self.request.user.pk)
		context= {'perfil': perfilA ,'form': form}
		return render(request,'zonaPrivada/entrenos.html',context)

	def post(self,request):
		form = NuevoEntrenoForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			n_nombre = cd['nombre']
			n_ejercicios = cd['ejercicios']
			perfil = Perfil.objects.get(usuario = request.user.pk)
			entreno = Entreno(nombre = n_nombre, ejercicios = n_ejercicios, usuario = perfil)
			entreno.save()
			messages.success(request, 'Entreno personalizado guardado correctamente')
			return HttpResponseRedirect("/crossfit/privada/benchmarks/entreno")
		perfilA = Perfil.objects.get(usuario = self.request.user.pk)
		context= {'perfil': perfilA ,'form': form}
		return render (request,'zonaPrivada/entrenos.html',context)

@method_decorator(login_required, name='dispatch')
class mostrarEntrenos(ListView):
	model = Entreno
	template_name = "zonaPrivada/entrenosAtletas.html"

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			paginador = Paginator(context['object_list'], 3)
			actual = self.request.GET.get('page')
			entrenos = paginador.get_page(actual)
			context['object_list'] = entrenos
			return context
		except Exception as e:
			raise

@login_required
def modificarPerfil(request):
	try:
		perfil = Perfil.objects.get(usuario = request.user.pk)
		context = {'perfil':perfil}
		if request.method == 'POST':
			form = modPerfil(request.POST, request.FILES)
			if form.is_valid():
				cd = form.cleaned_data
				n_nombre = cd['nombre']
				n_apellido1 = cd['apellido1']
				n_apellido2 = cd['apellido2']
				n_dni = cd['dni']
				n_sexo = cd['sexo']
				n_telefono = cd['telefono']
				n_foto = cd['imagen']
				n_edad = cd['edad']
				perfil = Perfil.objects.get(usuario = request.user.pk)
				perfil.nombre = n_nombre
				perfil.apellido1 = n_apellido1
				perfil.apellido2 = n_apellido2
				perfil.dni = n_dni
				perfil.sexo = n_sexo
				perfil.telefono = n_telefono
				if(n_foto != None):
					perfil.foto = n_foto
				perfil.edad = n_edad
				perfil.save()
				messages.success(request, 'Perfil modificado correctamente')
				return HttpResponseRedirect('/crossfit/privada/modPerfil')
		else:
			form = modPerfil(initial={'nombre':perfil.nombre,'apellido1':perfil.apellido1, 'apellido2':perfil.apellido2 ,
				'edad':perfil.edad ,'dni':perfil.dni, 'sexo':perfil.sexo,'telefono':perfil.telefono})
		context['form'] = form
		return render(request,'zonaPrivada/modPerfil.html',context)
	except Exception as e:
		raise
	return render(request,'registro.html',{'form':form})


@method_decorator(login_required, name='dispatch')
class reservaClase(TemplateView):
	template_name = "zonaPrivada/reservarClase.html"

	def get_context_data(self,**kwargs):
		try:
			context = super().get_context_data(**kwargs)
			context['perfil'] = Perfil.objects.get(usuario = self.request.user.pk)
			diasSemana = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miércoles','THURSDAY':'Jueves', \
					  	  'FRIDAY':'Viernes','SATURDAY':'Sábado','SUNDAY':'Domingo'}
			semanaFechas = []
			semanaFechas.append(datetime.now().strftime("%d-%m-%y"))
			for i in range(1,7):
				diaMas = datetime.now() + timedelta(days=i)
				semanaFechas.append(diaMas.strftime("%d-%m-%y"))

			horarioSemanal = []
			for fecha in semanaFechas:
				reservaA = []
				dia = diasSemana[datetime.strptime(fecha,'%d-%m-%y').strftime("%A").upper()]
				horario = Horario.objects.filter(diaSemana = dia)
				if(horario):
					reservaA.append(fecha)
					for h in horario:
						reservaA.append(h)
					horarioSemanal.append(reservaA)
			context['object_list'] = horarioSemanal
			paginador = Paginator(context['object_list'], 1)
			actual = self.request.GET.get('page')
			sistemaReservas = paginador.get_page(actual)
			context['fechas'] = semanaFechas
			context['object_list'] = sistemaReservas
			return context
		except Exception as e:
			raise

#Nos muestra el dia seleccionado en la reserva
def diaReservaSeleccionado(request, pk, fecha):
	#Pillamos los datos de esa reserva
	seleccionada = Horario.objects.get(pk = pk)
	fecha = datetime.strptime(fecha, '%d-%m-%y').date().strftime("%Y-%m-%d")
	atletas = Reservar.objects.filter(fecha = fecha, hora = seleccionada.horaInicio, clase = seleccionada.clase)
	#Comprobamos si el usuario puede reservar o cancelar reserva.
	fechaActual = datetime.now().strftime("%Y-%m-%d")
	opcion = 'Reservar'
	atleta = Perfil.objects.get(usuario = request.user.pk)
	if(datetime.now().strftime('%H:%M') <= seleccionada.horaInicio.strftime('%H:%M') or fecha > fechaActual):
		if(atleta.bono != None and fecha >= str(atleta.fechaInicio) and fecha <= str(atleta.fechaFin)):
			numReservas = Reservar.objects.filter(atleta = atleta, fecha__range = (atleta.fechaInicio , atleta.fechaFin)).count()
			if(numReservas < atleta.bono.creditos_clase or atleta.bono.tipo == 'ILIMITADO'):
				aforo = Reservar.objects.filter(fecha = fecha, hora = seleccionada.horaInicio, clase = seleccionada.clase).count()
				if(aforo < seleccionada.actividad.aforo):
					reservado = Reservar.objects.filter(fecha = fecha, hora = seleccionada.horaInicio, clase = seleccionada.clase, atleta = atleta).count()
					if(reservado == 0):
						opcion = 'Reservar'
					else:
						opcion = 'CancelarReserva'
				else:
					opcion = 'Aforo completo'
			else:
				reservado = Reservar.objects.filter(fecha = fecha, hora = seleccionada.horaInicio, clase = seleccionada.clase, atleta = atleta).count()
				if(reservado == 1):
					opcion = 'CancelarReserva'
				else:
					opcion = 'No te quedan créditos'
		else:
			opcion = 'Pendiente de pago para poder reservar'
	else:
		opcion = 'La clase ya ha pasado'
	context = {'object': seleccionada , 'atletas': atletas , 'opcion': opcion ,'fecha' : fecha}
	return render(request,'zonaPrivada/reservaSeleccionada.html',context)

@login_required
def realizarReserva(request):
	if request.method == 'POST':
		n_atleta = request.POST.get('atleta')
		n_clase = request.POST.get('clase')
		n_fecha = request.POST.get('fecha')
		n_hora = request.POST.get('hora')
		atleta = Perfil.objects.get(usuario = n_atleta)
		clase = Clase.objects.get(pk = n_clase)
		reserva = Reservar(atleta = atleta, clase = clase , fecha = n_fecha , hora = n_hora )
		reserva.save()
		messages.success(request, 'Reserva realizada con éxito')
		return HttpResponseRedirect('/crossfit/privada/reservarClase')

@login_required
def cancelarReserva(request):
	if request.method == 'POST':
		n_atleta = request.POST.get('atleta')
		n_clase = request.POST.get('clase')
		n_fecha = request.POST.get('fecha')
		n_hora = request.POST.get('hora')
		atleta = Perfil.objects.get(usuario = n_atleta)
		clase = Clase.objects.get(pk = n_clase)
		reserva = Reservar.objects.get(atleta = atleta, clase = clase , fecha = n_fecha , hora = n_hora).delete()
		messages.success(request, 'Reserva eliminada satisfactoriamente')
		return HttpResponseRedirect('/crossfit/privada/reservarClase')
