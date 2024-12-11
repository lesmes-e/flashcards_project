from django import forms
from .models import Mazo, Flashcard
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Renombramos el formulario de Mazo para evitar conflictos con el modelo Mazo
class MazoForm(forms.ModelForm):
    class Meta:
        model = Mazo
        fields = ['nombre', 'descripcion']

# Renombramos el formulario de Flashcard para evitar conflictos con el modelo Flashcard
class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pregunta', 'respuesta']

# Formulario de registro
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encriptar la contraseña
        if commit:
            user.save()
        return user

# Formulario de login
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
