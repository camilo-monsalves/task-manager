from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
# from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib  import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import TareaForm, CambiarEstadoTareForm, ObservacionForm, FiltrarTareaForm, EditarTareaForm
from .models import Tarea
from django import forms
# from datetime import datetime

# Create your views here.

def index(request):
    return render(
        request=request,
        template_name='task/index.html'
    )

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con éxito !')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    context = {'form':form}
    return render(request, 'task/registro.html', context)

def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.success(request, 'Inicio de sesión exitoso. !')
            login(request, user)
            return redirect('index')
        else:
            form = AuthenticationForm()
            messages.error(request, 'Credenciales incorrectas.')
    else:
        form = AuthenticationForm()

    return render(request, 'task/login.html', {'form':form})

@login_required
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Sesión finalizada con éxito.')
    return redirect('index')

@login_required(login_url='login-usuario') 
def crear_tarea(request):

    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión o registrarte para crear una tarea.')

    if request.method == "POST":
        form = TareaForm(request.POST, user=request.user)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.asignado_a = form.cleaned_data.get('asignado_a')
            tarea.asignado_por = form.cleaned_data.get('asignado_por')
            
            # Asigna el usuario asignado a la tarea
            tarea.user = tarea.asignado_a  
            
            tarea.save()
            messages.success(request, 'Tarea agregada !')
            return redirect('list-tarea')
    else:
        form = TareaForm(user=request.user)

    context = {'form': form}
    
    
    
    return render(request, 'task/crear_tarea.html', context)

@login_required(login_url='login-usuario') 
def lista_tareas(request):
    form = FiltrarTareaForm(request.GET)
    tareas = Tarea.objects.filter(Q(user=request.user) | Q(asignado_a=request.user) | Q(asignado_a__isnull=True)).order_by('fecha_vencimiento')

    if form.is_valid():
        filtro_query = form.cleaned_data.get('filtro_query')
        categoria = form.cleaned_data.get('categoria')

        if filtro_query:
            tareas = tareas.filter(Q(titulo__icontains=filtro_query) | Q(descripcion__icontains=filtro_query))

        if categoria:
            tareas = tareas.filter(categoria=categoria)

    context = {'tareas': tareas, 'form': form}
    
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión o registrarte para acceder a esta página.')
    
    return render(request, 'task/lista_tareas.html', context)


@login_required
def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    return render(request, 'task/detalle_tarea.html', {'tarea': tarea})

@method_decorator(login_required, name='dispatch')
class EliminarTarea(DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'task/confirmar_eliminar_tarea.html'
    success_url = reverse_lazy('list-tarea')

    def form_valid(self, form):
        messages.success(self.request, 'Tarea borrada con éxito.')
        return super(EliminarTarea, self).form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class EditarTarea(UpdateView):
    model = Tarea
    form_class = EditarTareaForm
    template_name = 'task/editar_tarea.html'
    success_url = reverse_lazy('list-tarea')

    def form_valid(self, form):
        messages.success(self.request, 'Tarea actualizada con éxito.')
        return super(EditarTarea, self).form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['estado'].widget.attrs['disabled'] = True
        form.fields['estado'].required = False

        tarea = self.get_object()
        form.fields['fecha_vencimiento'].initial = tarea.fecha_vencimiento
        form.fields['estado'].initial = tarea.estado

        form.fields['fecha_vencimiento'].widget = forms.DateInput(attrs={'type': 'date'})
        return form

@login_required
def cambiar_estado_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == "POST":
        form = CambiarEstadoTareForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado de la tarea cambiado con éxito.')
            return redirect('detalle-tarea', tarea_id=tarea_id)
    else:
        form = CambiarEstadoTareForm(instance=tarea)
    
    return render(request, 'task/cambiar_estado_tarea.html', {'form': form, 'tarea': tarea})

@login_required
def crear_observacion(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == 'POST':
        form = ObservacionForm(request.POST, instance=tarea)
        if form.is_valid():
            observacion = form.save(commit=False)
            observacion.tarea = tarea
            observacion.save()
            messages.success(request, 'Observación agregada.')
            return redirect('detalle-tarea', tarea_id=tarea_id)
    else:
        form = ObservacionForm()

    return render(request, 'task/crear_observacion.html', {'form':form, 'tarea':tarea})

