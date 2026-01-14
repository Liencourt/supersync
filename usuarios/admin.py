from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SyncUsuario
from .models import PerfilUsuario  # Já estava importado, vamos usar agora

# --- 1. CONFIGURAÇÃO DO INLINE (NOVO) ---
# Isso faz o Perfil aparecer dentro da tela do Usuário
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Acesso (Configurações Extras)'
    fk_name = 'user'

class CustomUserCreationForm(UserCreationForm):
    """
    Um formulário para criar novos usuários, corrigido para salvar o campo 'name'.
    """
    class Meta(UserCreationForm.Meta):
        model = SyncUsuario
        fields = ('username', 'name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name', '')
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Um formulário para atualizar usuários existentes.
    """
    class Meta:
        model = SyncUsuario
        # FIXED: Removidos 'groups' e 'user_permissions'
        fields = ('username', 'name', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')


class SyncUsuarioAdmin(UserAdmin):
    """
    Define a representação do seu modelo SyncUsuario no admin.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = SyncUsuario
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # --- 2. ADICIONANDO O INLINE AQUI (NOVO) ---
    inlines = (PerfilUsuarioInline, )

    # Adicionei a coluna 'eh_comprador' na listagem para facilitar sua vida
    list_display = ['username', 'name', 'is_staff', 'is_active', 'ver_comprador']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('name',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )

    search_fields = ('username', 'name')
    ordering = ('username',)
    filter_horizontal = ()

    # --- 3. MÉTODO PARA MOSTRAR NA LISTAGEM (NOVO) ---
    def ver_comprador(self, obj):
        # Garante que não quebre se o usuário não tiver perfil criado ainda
        return getattr(obj, 'perfil', None) and obj.perfil.eh_comprador
    
    ver_comprador.short_description = 'É Comprador?'
    ver_comprador.boolean = True # Mostra o ícone de ✅ ou ❌

# Register the admin class
admin.site.register(SyncUsuario, SyncUsuarioAdmin)