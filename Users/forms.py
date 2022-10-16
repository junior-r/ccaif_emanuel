from django import forms
from django.contrib.auth.forms import UserCreationForm
from Users.models import User


class SignupForm(UserCreationForm):
    picture_profile = forms.ImageField(label='Imagen de Perfil', required=False, widget=forms.FileInput(attrs={'class': 'inputfile inputfile-5', 'id': 'file-5', 'data-multiple-caption': '{count} archivos seleccionados'}))
    username = forms.TextInput()
    email = forms.EmailInput()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True, min_length=8)
    password2 = forms.CharField(label='Contraseña (Confirmación)', widget=forms.PasswordInput, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['picture_profile', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser']
        help_texts = {
            'is_staff': '',
            'is_superuser': ''
        }
        labels = {
            'first_name': 'Nombres'
        }
