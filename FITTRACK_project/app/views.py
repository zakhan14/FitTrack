from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
import json

from .forms import SignUpForm, CustomLoginForm, BodyDataForm

User = get_user_model()

def index(request):
    return render(request, 'index.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if not hasattr(user, 'nickname') or not user.nickname:
                user.nickname = user.email.split('@')[0]
                user.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})

def log_in(request):
    next_url = request.GET.get('next', reverse('index'))

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                redirect_to = request.POST.get('next', next_url)
                if url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
                    return redirect(redirect_to)
                else:
                    return redirect(reverse('index'))
            else:
                form.add_error(None, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = CustomLoginForm()

    return render(request, 'log_in.html', {'form': form, 'next': next_url})

@login_required(login_url='log_in')
def detalle(request):
    id = request.GET.get('id')
    return render(request, 'detalle.html', {'id': id})

@login_required(login_url='log_in')
def progreso(request):
    form = BodyDataForm(request.POST or None)
    last_measurement = request.user.body_data.order_by('-mesures_update').first()

    indicator = [
        {'name': 'Altura', 'max': 220},
        {'name': 'Peso', 'max': 120},
        {'name': 'Grasa corporal', 'max': 40},
        {'name': 'Masa muscular', 'max': 60},
        {'name': 'Líquido corporal', 'max': 70},
    ]

    if request.method == 'POST':
        if 'guardar' in request.POST and form.is_valid():
            bodydata = form.save(commit=False)
            bodydata.user = request.user
            bodydata.save()
            last_measurement = bodydata

        # En este caso solo guardamos, sin comparación visual
            return redirect('progreso')

        elif 'comparar' in request.POST and form.is_valid():
            form_data = form.cleaned_data
            dataRadar = []

            if last_measurement:
                dataRadar.append([
                    last_measurement.height,
                    last_measurement.weight,
                    last_measurement.grasa_corporal,
                    last_measurement.masa_muscular,
                    last_measurement.liquido_corporal
                ])
                label_1 = "Guardado"
            else:
                label_1 = "No hay medición previa"

            dataRadar.append([
                form_data['height'],
                form_data['weight'],
                form_data['grasa_corporal'],
                form_data['masa_muscular'],
                form_data['liquido_corporal']
            ])

            labels = [label_1, "Formulario (sin guardar)"]

            return render(request, 'progreso.html', {
                'form': form,
                'data_radar': json.dumps(dataRadar, cls=DjangoJSONEncoder),
                'indicator': json.dumps(indicator, cls=DjangoJSONEncoder),
                'labels': json.dumps(labels, cls=DjangoJSONEncoder),
            })

# Si no es POST o no entra en ninguno de los if anteriores
    return render(request, 'progreso.html', {
        'form': form,
        'data_radar': json.dumps([], cls=DjangoJSONEncoder),
        'indicator': json.dumps(indicator, cls=DjangoJSONEncoder),
        'labels': json.dumps([], cls=DjangoJSONEncoder),
    })

@login_required(login_url='log_in')
@csrf_protect
def entrenamiento(request):
    if request.method == "POST":
        fecha = request.POST.get('fecha')
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')

        # Cuando tengas el modelo Training, descomenta esto:
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
