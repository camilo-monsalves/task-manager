from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib  import messages
from django.shortcuts import render, redirect

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
            return redirect('registro-usuario')
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
            messages.error(request, 'Credenciales incorrectas.')
    else:
        form = AuthenticationForm()

    return render(request, 'task/login.html', {'form':form})

@login_required
def logout_usuario(request):
    logout(request)
    messages.success(request, 'Sesión finalizada con éxito.')
    return redirect('index')