from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

# Importando nosso novo formulário
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":
        # 1. Usando o AuthenticationForm em vez de request.POST direto
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # O form.is_valid() já chama o `authenticate()` por baixo dos panos
            user = form.get_user()
            login(request, user)

            # 2. Corrigido para usar `user.name` que existe no nosso modelo
            messages.success(request, f"Bem-vindo, {user.name or user.username}!")

            # 3. Validando a URL `next` para evitar Open Redirect
            next_url = request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("dashboard:home")
        else:
            # Se o formulário não for válido, as mensagens de erro já são adicionadas
            # pelo próprio formulário. Apenas exibimos o formulário novamente.
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logout realizado com sucesso!")
        return redirect("accounts:login")


    return redirect("dashboard:home")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {'user': request.user})