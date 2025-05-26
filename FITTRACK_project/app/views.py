from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from .forms import BodyDataForm
from django.core.serializers.json import DjangoJSONEncoder
import json

from .forms import SignUpForm, CustomLoginForm

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
    chart_data = []

    if request.method == 'POST':
        if 'guardar' in request.POST:
            # Guardar nueva medición y luego mostrar gráfico con esa medición guardada
            if form.is_valid():
                bodydata = form.save(commit=False)
                bodydata.user = request.user
                bodydata.save()
                # Recargar la última medición tras guardar
                last_measurement = bodydata
                chart_data = [{
                    'height': last_measurement.height,
                    'weight': last_measurement.weight,
                    'grasa_corporal': last_measurement.grasa_corporal,
                    'masa_muscular': last_measurement.masa_muscular,
                    'liquido_corporal': last_measurement.liquido_corporal,
                    'fecha': last_measurement.mesures_update.strftime('%Y-%m-%d'),
                }]
                return render(request, 'progreso.html', {
                    'form': BodyDataForm(),  # formulario limpio tras guardar
                    'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder),
                })

        elif 'comparar' in request.POST:
            # No guardamos, tomamos datos del formulario + última medición guardada y comparamos
            if form.is_valid():
                form_data = form.cleaned_data
                if last_measurement:
                    chart_data = [
                        {
                            'height': last_measurement.height,
                            'weight': last_measurement.weight,
                            'grasa_corporal': last_measurement.grasa_corporal,
                            'masa_muscular': last_measurement.masa_muscular,
                            'liquido_corporal': last_measurement.liquido_corporal,
                            'fecha': last_measurement.mesures_update.strftime('%Y-%m-%d'),
                        },
                        {
                            'height': form_data['height'],
                            'weight': form_data['weight'],
                            'grasa_corporal': form_data['grasa_corporal'],
                            'masa_muscular': form_data['masa_muscular'],
                            'liquido_corporal': form_data['liquido_corporal'],
                            'fecha': 'Formulario (sin guardar)',
                        }
                    ]
                else:
                    # No hay última medición guardada, solo mostramos formulario
                    chart_data = [
                        {
                            'height': form_data['height'],
                            'weight': form_data['weight'],
                            'grasa_corporal': form_data['grasa_corporal'],
                            'masa_muscular': form_data['masa_muscular'],
                            'liquido_corporal': form_data['liquido_corporal'],
                            'fecha': 'Formulario (sin guardar)',
                        }
                    ]

                return render(request, 'progreso.html', {
                    'form': form,
                    'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder),
                })

    # GET o cualquier otro caso: mostramos solo la última medición
    if last_measurement:
        chart_data = [{
            'height': last_measurement.height,
            'weight': last_measurement.weight,
            'grasa_corporal': last_measurement.grasa_corporal,
            'masa_muscular': last_measurement.masa_muscular,
            'liquido_corporal': last_measurement.liquido_corporal,
            'fecha': last_measurement.mesures_update.strftime('%Y-%m-%d'),
        }]
    else:
        chart_data = []

    return render(request, 'progreso.html', {
        'form': form,
        'chart_data': json.dumps(chart_data, cls=DjangoJSONEncoder),
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
