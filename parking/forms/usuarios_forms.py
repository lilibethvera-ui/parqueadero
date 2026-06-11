from django import forms
from django.contrib.auth.models import Group





class RegistroSaaSForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: alejandro_admin'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    nombre_empresa = forms.CharField(
        label="Nombre de tu Parqueadero / Empresa",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Parqueadero Central'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'})
    )