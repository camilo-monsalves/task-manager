from django import forms
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit

# forms.py
class TareaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-class-from-bootstrap'

        self.fields['asignado_por'].queryset = User.objects.filter(pk=self.user.pk) if self.user else User.objects.none()


    asignado_a = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    asignado_por = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control form-control-lg', 'rows':3})
    )

    def clean(self):
        cleaned_data = super().clean()
        asignado_a = cleaned_data.get('asignado_a')
        asignado_por = self.user  # Usamos el usuario logeado

        if asignado_a and asignado_por:
            if asignado_a == asignado_por:
                raise forms.ValidationError('No puedes asignarte una tarea a ti mismo.')

        return cleaned_data

    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'estado', 'categoria', 'asignado_a', 'asignado_por', 'prioridad']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento and fecha_vencimiento < timezone.now().date():
            raise forms.ValidationError('La fecha de vencimiento no puede ser anteriro a la fecha actual')
        return fecha_vencimiento
    
    estado = forms.ChoiceField(choices=Tarea.ESTADO_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))
    prioridad = forms.ChoiceField(choices=Tarea.PRIORIDAD_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))

class CambiarEstadoTareForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['estado']
        widgets = {
            'estado':forms.Select(attrs={'class':'form-control'}),
        }

class EditarTareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'fecha_vencimiento', 'estado', 'categoria', 'prioridad']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['observacion']

class FiltrarTareaForm(forms.Form):
    filtro_query = forms.CharField(
        label='Buscar Tareas',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    CATEGORIA_CHOICES = Tarea.CATEGORIA_CHOICES

    categoria = forms.ChoiceField(
        label='Filtrar por categoría',
        required=False,
        choices=[('', 'Todos')] + list(CATEGORIA_CHOICES),
        widget=forms.Select(attrs={'class':'form-control'})
    )