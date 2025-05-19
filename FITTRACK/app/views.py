from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

def index(request):
    return render(request, 'index.html')

def sing_up(request):
    return render(request, 'sing_up.html')

def log_in(request):
    return render(request, 'log_in.html')

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
