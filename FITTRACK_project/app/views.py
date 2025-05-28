from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy, reverse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, CustomLoginForm, BodyDataForm
from .models import BodyData  # asegúrate de importar tu modelo

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

class ProgresoView(LoginRequiredMixin, FormMixin, ListView):
    model = BodyData
    template_name = 'progreso.html'
    form_class = BodyDataForm
    context_object_name = 'mediciones'
    login_url = 'log_in'
    success_url = reverse_lazy('progreso')

    def get_queryset(self):
        return BodyData.objects.filter(user=self.request.user).order_by('-mesures_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        ultima = self.get_queryset().first()
        dataRadar = []
        labels = []

        if ultima:
            dataRadar.append([
                float(ultima.height),
                float(ultima.weight),
                float(ultima.grasa_corporal),
                float(ultima.masa_muscular),
                float(ultima.liquido_corporal)
            ])
            labels.append("Última medición")

        indicator = [
            {'name': 'height', 'max': 220},
            {'name': 'weight', 'max': 120},
            {'name': 'grasa_corporal', 'max': 40},
            {'name': 'masa_muscular', 'max': 60},
            {'name': 'liquido_corporal', 'max': 70},
        ]

        context['indicator'] = json.dumps(indicator, cls=DjangoJSONEncoder)
        context['data_radar'] = json.dumps(dataRadar, cls=DjangoJSONEncoder)
        context['labels'] = json.dumps(labels, cls=DjangoJSONEncoder)
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()

        indicator = [
            {'name': 'height', 'max': 220},
            {'name': 'weight', 'max': 120},
            {'name': 'grasa_corporal', 'max': 40},
            {'name': 'masa_muscular', 'max': 60},
            {'name': 'liquido_corporal', 'max': 70},
        ]

        if form.is_valid():
            if 'guardar' in request.POST:
                bodydata = form.save(commit=False)
                bodydata.user = request.user
                bodydata.save()
                return redirect('progreso')

            elif 'comparar' in request.POST:
                ultima = self.object_list.first()
                current_data = form.cleaned_data

                dataRadar = []
                labels = []

                if ultima:
                    dataRadar.append([
                        float(ultima.height),
                        float(ultima.weight),
                        float(ultima.grasa_corporal),
                        float(ultima.masa_muscular),
                        float(ultima.liquido_corporal)
                    ])
                    labels.append("Última medición")

                dataRadar.append([
                    float(current_data['height']),
                    float(current_data['weight']),
                    float(current_data['grasa_corporal']),
                    float(current_data['masa_muscular']),
                    float(current_data['liquido_corporal'])
                ])
                labels.append("Formulario (sin guardar)")

                return self.render_to_response({
                    'form': form,
                    'mediciones': self.object_list,
                    'data_radar': json.dumps(dataRadar, cls=DjangoJSONEncoder),
                    'indicator': json.dumps(indicator, cls=DjangoJSONEncoder),
                    'labels': json.dumps(labels, cls=DjangoJSONEncoder),
                })

        return self.form_invalid(form)
# @login_required(login_url='log_in')
# def progreso(request):
#     form = BodyDataForm(request.POST or None)
#     user = request.user

#     indicator = [
#         {'name': 'Altura', 'max': 220},
#         {'name': 'Peso', 'max': 120},
#         {'name': 'Grasa corporal', 'max': 40},
#         {'name': 'Masa muscular', 'max': 60},
#         {'name': 'Líquido corporal', 'max': 70},
#     ]

#     # Si se quiere guardar una nueva medición
#     if request.method == 'POST' and 'guardar' in request.POST and form.is_valid():
#         bodydata = form.save(commit=False)
#         bodydata.user = user
#         bodydata.save()
#         return redirect('progreso')

#     # Si se quiere comparar
#     elif request.method == 'POST' and 'comparar' in request.POST:
#         mediciones = list(user.body_data.order_by('-mesures_update')[:2])
#         dataRadar = []
#         labels = []

#         if len(mediciones) >= 1:
#             ultima = mediciones[0]
#             dataRadar.append([
#                 ultima.height,
#                 ultima.weight,
#                 ultima.grasa_corporal,
#                 ultima.masa_muscular,
#                 ultima.liquido_corporal
#             ])
#             labels.append("Última medición")

#         if len(mediciones) == 2:
#             anterior = mediciones[1]
#             dataRadar.append([
#                 anterior.height,
#                 anterior.weight,
#                 anterior.grasa_corporal,
#                 anterior.masa_muscular,
#                 anterior.liquido_corporal
#             ])
#             labels.append("Medición anterior")
#         elif form.is_valid():
#             current_data = form.cleaned_data
#             dataRadar.append([
#                 current_data['height'],
#                 current_data['weight'],
#                 current_data['grasa_corporal'],
#                 current_data['masa_muscular'],
#                 current_data['liquido_corporal']
#             ])
#             labels.append("Formulario (sin guardar)")

#         return render(request, 'progreso.html', {
#             'form': form,
#             'data_radar': json.dumps(dataRadar, cls=DjangoJSONEncoder),
#             'indicator': json.dumps(indicator, cls=DjangoJSONEncoder),
#             'labels': json.dumps(labels, cls=DjangoJSONEncoder),
#         })

#     # Si no es POST o no se ha hecho nada
#     return render(request, 'progreso.html', {
#         'form': form,
#         'data_radar': json.dumps([], cls=DjangoJSONEncoder),
#         'indicator': json.dumps(indicator, cls=DjangoJSONEncoder),
#         'labels': json.dumps([], cls=DjangoJSONEncoder),
#     })

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
