from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import BodyData

User = get_user_model()

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, strip=False)
    confirm_password = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ('nickname', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class BodyDataForm(forms.ModelForm):
    class Meta:
        model = BodyData
        fields = ['height', 'weight', 'grasa_corporal', 'masa_muscular', 'liquido_corporal', 'mesures_update']
        labels = {
            'height': 'Altura (cm)',
            'weight': 'Peso (kg)',
            'grasa_corporal': 'Grasa Corporal (%)',
            'masa_muscular': 'Masa Muscular (%)',
            'liquido_corporal': 'Líquido Corporal (%)',
            'mesures_update': 'Fecha de medición',
        }
        widgets = {
            'mesures_update': forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'YYYY-MM-DD'  # Ejemplo de formato ISO
         }),
        }

