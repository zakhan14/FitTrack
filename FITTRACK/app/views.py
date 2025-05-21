from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm, CustomLoginForm


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')  # redirige a la home
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # redirige a la home
    else:
        form = CustomLoginForm()
    return render(request, 'log_in.html', {'form': form})


@login_required(login_url='log_in')
def detalle(request):
    id = request.GET.get('id')
    # Aquí usas el id para lo que necesites (buscar en DB, etc)
    return render(request, 'detalle.html', {'id': id})


@login_required(login_url='log_in')
def progreso(request):
    return render(request, 'progreso.html')


@login_required(login_url='log_in')
@csrf_protect
def entrenamiento(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')

        # Aquí validaré los datos y guardar en la DB
        # Ejemplo:
        # Entrenamiento.objects.create(fecha=fecha, tipo=tipo, descripcion=descripcion)

        return redirect('entrenamiento')

    return render(request, 'entrenamiento.html')


def custom_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect('index')  # Redirige a la página de inicio
