from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    """
    Herda do formulário de autenticação padrão do Django para facilitar
    a customização no futuro, se necessário. Por enquanto, ele já faz
    tudo o que precisamos.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Customizar labels ou widgets, se desejar
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome de Usuário'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
