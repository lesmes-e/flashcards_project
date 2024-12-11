from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Mazo, Flashcard
from .forms import RegisterForm, LoginForm, MazoForm, FlashcardForm
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'flashcards_app/login.html')

# Vista para el dashboard de mazos
@login_required
def dashboard(request):
    user = request.user
    mazos = Mazo.objects.filter(usuario=user)  # Mostrar los mazos asociados al usuario
    return render(request, 'flashcards_app/dashboard.html', {'mazos': mazos})

# Vista para ver las flashcards de un mazo
@login_required
def flashcard_list(request, mazo_id):
    mazo = get_object_or_404(Mazo, id=mazo_id, usuario=request.user)
    flashcards = Flashcard.objects.filter(mazo=mazo)
    
    # Filtros para ver tarjetas completas o pendientes
    filtro = request.GET.get('filtro', 'todos')  # Filtro por defecto es 'todos'
    if filtro == 'completadas':
        flashcards = flashcards.filter(completada=True)
    elif filtro == 'pendientes':
        flashcards = flashcards.filter(completada=False)

    # Pasar el progreso del mazo a la plantilla
    progreso = mazo.get_progreso()

    return render(request, 'flashcards_app/flashcard_list.html', {
        'mazo': mazo,
        'flashcards': flashcards,
        'progreso': progreso,
        'filtro': filtro,
    })

# Vista para marcar una flashcard como completada o pendiente
@login_required
def toggle_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    flashcard.toggle_completada()  # Usamos el método toggle_completada() definido en el modelo
    return redirect('flashcard_list', mazo_id=flashcard.mazo.id)

# Vista para crear un nuevo mazo
@login_required
def create_mazo(request):
    if request.method == 'POST':
        form = MazoForm(request.POST)
        if form.is_valid():
            mazo = form.save(commit=False)
            mazo.usuario = request.user  # Asignamos el usuario actual al mazo
            mazo.save()
            return redirect('flashcard_list', mazo_id=mazo.id)
    else:
        form = MazoForm()
    return render(request, 'flashcards_app/create_mazo.html', {'form': form})

# Vista para agregar una flashcard a un mazo
@login_required
def add_flashcard(request, mazo_id):
    mazo = get_object_or_404(Mazo, id=mazo_id, usuario=request.user)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.mazo = mazo  # Asignamos el mazo actual a la flashcard
            flashcard.save()
            return redirect('flashcard_list', mazo_id=mazo.id)
    else:
        form = FlashcardForm()
    return render(request, 'flashcards_app/add_flashcard.html', {'form': form, 'mazo': mazo})

# Vista para registrar un nuevo usuario
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir al login después de registrarse
    else:
        form = RegisterForm()
    return render(request, 'flashcards_app/register.html', {'form': form})

# Vista para iniciar sesión
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirigir al dashboard después de iniciar sesión
    else:
        form = LoginForm()
    return render(request, 'flashcards_app/login.html', {'form': form})