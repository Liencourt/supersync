from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from .forms import CadastroUsuarioForm
from .forms import CadastroUsuarioAppForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import ListView, UpdateView,DeleteView
from django.shortcuts import get_object_or_404, redirect

User = get_user_model()

class CadastroUsuarioView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    form_class = CadastroUsuarioAppForm
    template_name = 'usuarios/cadastro_usuario.html'
    success_url = reverse_lazy('usuarios:listar-usuarios') # Crie essa URL depois ou mande para a home
    permission_required = 'usuarios.add_syncusuario' # Apenas quem pode add user vê a tela
    
    def form_valid(self, form):
        response = super().form_valid(form)
        tipo = "Comprador" if form.cleaned_data.get('eh_comprador') else "Administrativo"
        messages.success(self.request, f"Usuário {form.instance.name} ({tipo}) cadastrado com sucesso!")
        return response
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Novo Usuário'
        return context
    
class UsuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    permission_required = 'usuarios.view_syncusuario' # Ajuste conforme sua permissão real

    def get_queryset(self):
        qs = User.objects.all().order_by('name')
        termo = self.request.GET.get('q')
        
        if termo:
            qs = qs.filter(
                Q(name__icontains=termo) |
                Q(username__icontains=termo)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '')
        return context

class UsuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = CadastroUsuarioAppForm
    template_name = 'usuarios/cadastro_usuario.html' # Reusa o template de cadastro
    success_url = reverse_lazy('usuarios:listar-usuarios')
    permission_required = 'usuarios.change_syncusuario'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Editar Usuário'
        # Preenche o checkbox manualmente pois ele não é um campo direto do User
        if hasattr(self.object, 'perfil'):
            context['form'].fields['eh_comprador'].initial = self.object.perfil.eh_comprador
        return context

    def form_valid(self, form):
        messages.success(self.request, "Dados do usuário atualizados com sucesso!")
        return super().form_valid(form)

def toggle_status_usuario(request, pk):
    """Ativa ou Inativa um usuário (Soft Delete)"""
    if not request.user.has_perm('usuarios.change_syncusuario'):
        messages.error(request, "Você não tem permissão para isso.")
        return redirect('usuarios:listar-usuarios')
        
    user = get_object_or_404(User, pk=pk)
    
    # Impede que o usuário desative a si mesmo
    if user == request.user:
        messages.warning(request, "Você não pode desativar seu próprio usuário.")
    else:
        user.is_active = not user.is_active
        user.save()
        status = "ativado" if user.is_active else "desativado"
        messages.success(request, f"Usuário {user.name} foi {status}.")
        
    return redirect('usuarios:listar-usuarios')

class UsuarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('usuarios:listar-usuarios')
    permission_required = 'usuarios.delete_syncusuario'
    
    def form_valid(self, form):
        # Proteção extra: Não deixar apagar a si mesmo
        if self.object == self.request.user:
            messages.error(self.request, "Você não pode excluir seu próprio usuário!")
            return redirect(self.success_url)
            
        messages.success(self.request, f"Usuário {self.object.name} excluído permanentemente.")
        return super().form_valid(form)