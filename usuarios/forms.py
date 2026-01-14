from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario
from django.contrib.auth import get_user_model

class CadastroUsuarioForm(UserCreationForm):
    # Adicionamos campos extras visuais
    first_name = forms.CharField(label="Nome", max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Sobrenome", max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    eh_comprador = forms.BooleanField(label="Usuário é Comprador?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] # Senha já vem automática
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # 1. Salva o usuário padrão (tabela auth_user)
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # 2. Atualiza o perfil (tabela usuarios_perfilusuario)
            # O perfil já foi criado pelo signal, apenas atualizamos
            user.perfil.eh_comprador = self.cleaned_data['eh_comprador']
            user.perfil.save()
            
        return user

User = get_user_model() # Pega o SyncUsuario

class CadastroUsuarioAppForm(UserCreationForm):
    # Campos visuais extras
    name = forms.CharField(
        label="Nome Completo", 
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Maria da Silva'})
    )
    
    eh_comprador = forms.BooleanField(
        label="Definir como Comprador?", 
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'name'] # Senha 1 e 2 vêm automático do UserCreationForm
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login do sistema'}),
        }

    def save(self, commit=True):
        # 1. Salva o Usuário (SyncUsuario)
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        
        if commit:
            user.save()
            # 2. Atualiza ou Cria o Perfil
            # O signal já deve ter criado, mas usamos get_or_create por segurança
            perfil, created = PerfilUsuario.objects.get_or_create(user=user)
            perfil.eh_comprador = self.cleaned_data['eh_comprador']
            perfil.save()
            
        return user