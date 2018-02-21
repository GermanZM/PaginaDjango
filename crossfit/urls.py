from django.contrib import admin
from django.urls import path
from crossfit import views
from django.contrib.auth.views import login,logout

urlpatterns = [
	path('index/',views.Principal.as_view()),
	path('login/',login,{'template_name':'privadaLogin.html',}, name='login'),
	path('logout/',views.logoutUsuario, name='logout'),
	path('registro/',views.nuevoRegistro, name='registro'),
	path('tarifa/',views.Tarifas, name='Tarifas'),
	path('horario/',views.mostrarHorario, name='Horario'),
	path('privada/',views.Privada),
	path('privada/contacto/',views.Contactar, name='Contacto'),
	path('privada/atletas/',views.mostrarAtletas.as_view(), name='Atletas'),
	path('privada/atletas/mostrar/<int:pk>',views.atletaSeleccionado.as_view(), name='detalle_Atleta'),
	path('privada/benchmarks/',views.Benchmarks.as_view()),
	path('privada/benchmarks/girls/',views.mostrarGirl.as_view(), name='Girls'),
	path('privada/benchmarks/heroes/',views.mostrarHeroes.as_view(), name='Heroes'),
	path('privada/benchmarks/Oficial/mostrar/<int:pk>',views.oficialSeleccionado.as_view(), name='detalle_Oficial'),
	path('privada/benchmarks/entreno/',views.NuevoEntreno.as_view(), name='nuevoEntreno'),
	path('privada/benchmarks/listaEntrenos',views.mostrarEntrenos.as_view(), name='entrenosAtletas'),
	path('privada/modPerfil',views.modificarPerfil, name='modInfAtleta'),
	path('privada/reservarClase',views.reservaClase.as_view()),
	path('privada/reservarClase/<int:pk>/?P<fecha>[0-9]{2}-?[0-9]{2}-?[0-9]{2}',views.diaReservaSeleccionado, name="rSeleccionada"),
	path('privada/reservarClase/reserva/',views.realizarReserva, name='nuevaReserva'),
	path('privada/reservarClase/cancelarReserva/',views.cancelarReserva, name='cancelarReserva'),
]
