from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
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
            return redirect('index')  # redirige a tu home
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # redirige a tu home
    else:
        form = CustomLoginForm()
    return render(request, 'log_in.html', {'form': form})

def detalle(request):
    return render(request, 'detalle.html')

def progreso(request):
    return render(request, 'progreso.html')

@csrf_protect
def entrenamiento(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')

        # Aquí podrías validar los datos y guardar en la DB
        # Ejemplo si tienes un modelo:
        # Entrenamiento.objects.create(fecha=fecha, tipo=tipo, descripcion=descripcion)

        # Por ahora solo redirigimos a la misma página o puedes enviar un mensaje
        return redirect('entrenamiento')

    # Si es GET, simplemente renderizamos el formulario
    return render(request, 'entrenamiento.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')  # Redirige donde quieras
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})