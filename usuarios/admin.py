from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SyncUsuario


class CustomUserCreationForm(UserCreationForm):
    """
    Um formulário para criar novos usuários, corrigido para salvar o campo 'name'.
    """

    class Meta(UserCreationForm.Meta):
        model = SyncUsuario
        # Define os campos do modelo que devem aparecer no formulário de criação.
        fields = ('username', 'name')

    def save(self, commit=True):
        # CORREÇÃO: Sobrescrevemos o método save para garantir que o campo 'name' seja salvo.
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
        # FIXED: Removidos 'groups' e 'user_permissions' para evitar erros com tabelas inexistentes
        fields = ('username', 'name', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')


class SyncUsuarioAdmin(UserAdmin):
    """
    Define a representação do seu modelo SyncUsuario no admin.
    """
    # Usa nossos formulários personalizados
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    # O modelo que esta classe de admin representa
    model = SyncUsuario

    # Colunas que serão exibidas na lista de usuários
    list_display = ['username', 'name', 'is_staff', 'is_active']

    # Precisamos sobrescrever os 'fieldsets' porque os padrões fazem
    # referência a campos como 'first_name' e 'last_name'
    # que não existem no nosso modelo.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('name',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Define os campos para a página de criação de usuário.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'password1', 'password2'),
        }),
    )

    # Adiciona uma barra de pesquisa no admin
    search_fields = ('username', 'name')

    # Garante que a lista de usuários esteja ordenada por nome de usuário
    ordering = ('username',)

    # FIXED: Disable editing of many-to-many fields that don't have tables
    filter_horizontal = ()


# Register the admin class
admin.site.register(SyncUsuario, SyncUsuarioAdmin)
