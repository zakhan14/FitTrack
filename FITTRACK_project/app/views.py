from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SignUpForm, CustomLoginForm

User = get_user_model()


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.nickname = user.nickname or user.username  # asegurar nickname
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})


def log_in(request):
    next_url = request.GET.get('next', 'index')  # por si accedió a una página protegida

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            redirect_to = request.POST.get('next', next_url)
            if url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
                return redirect(redirect_to)
            else:
                return redirect('index')
    else:
        form = CustomLoginForm()

    return render(request, 'log_in.html', {'form': form, 'next': next_url})


@login_required(login_url='log_in')
def detalle(request):
    id = request.GET.get('id')
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

        # Aquí guardará los datos en la base de datos
        # Training.objects.create(
        #     user=request.user,
        #     training_date=fecha,
        #     tipo_entrenamiento=tipo,
        #     comment=descripcion
        # )

        return redirect('entrenamiento')

    return render(request, 'entrenamiento.html')


def custom_logout(request):
    logout(request)
    return redirect('index')
