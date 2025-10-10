# SuperSync (Projeto Django)

Projeto web em Django para gestão/autenticação de usuários e módulos de contratos, contas (login/logout/perfil) e dashboard. Este README fornece visão geral, requisitos, configuração, comandos de execução, variáveis de ambiente, testes, estrutura e licença.

Observação importante: informações desconhecidas foram marcadas como TODO para futura atualização. Este documento está em pt-BR.

## Visão Geral
- Stack: Python + Django (5.2.7) com PostgreSQL.
- Apps principais:
  - `usuarios`: modelo de usuário customizado (`SyncUsuario`) e backend de autenticação simples (plaintext).
  - `accounts`: views de login, logout (via POST) e perfil, com templates.
  - `contratos`: app reservado para regras de negócio de contratos (modelos/admin presentes; views/urls podem ser expandidas).
  - `dashboard`: base para telas iniciais (views ainda a definir).
- Entry points:
  - CLI: `python manage.py ...`
  - Servidor dev: `python manage.py runserver`
  - WSGI: `supersync.wsgi.application`
  - ASGI: `supersync.asgi.application`
- URLs atualmente mapeadas: `/admin/`. Há `accounts/urls.py` com rotas (`login`, `logout`, `profile`), mas elas não estão incluídas em `supersync/urls.py` ainda (ver TODO em “Rotas”).

## Requisitos
- Python 3.11+ (recomendado)
- PostgreSQL 13+ (local ou remoto)
- Pip / venv
- Dependências Python:
  - Django==5.2.7
  - psycopg2-binary (para conexão com PostgreSQL)
  - TODO: adicionar outras libs quando conhecidas (ex.: django-environ, etc.)

Sugerido criar `requirements.txt` (TODO):
```
Django==5.2.7
psycopg2-binary
```

## Configuração
1) Clonar o repositório
- Windows PowerShell:
```
cd C:\Users\alexandro.nascimento\
# (Se já estiver na pasta, pule)
```

2) Criar ambiente virtual e instalar dependências
```
python -m venv .venv
.\.venv\Scripts\activate
# Se houver requirements.txt
pip install -r requirements.txt
# Alternativa (sem requirements.txt por enquanto)
pip install Django==5.2.7 psycopg2-binary
```

3) Variáveis de ambiente (recomendado usar .env) – ver seção “Variáveis de ambiente”.

4) Aplicar migrações e criar superusuário
```
python manage.py migrate
python manage.py createsuperuser
```
Observação: o projeto utiliza um modelo de usuário customizado (`usuarios.SyncUsuario`) com `username` como chave primária. O `REQUIRED_FIELDS` inclui `name`. Durante `createsuperuser`, informe pelo menos `username`, `password` e opcionalmente `name` (se solicitado).

5) Executar servidor de desenvolvimento
```
python manage.py runserver
```
Acesse: http://127.0.0.1:8000/admin/

## Variáveis de Ambiente
Atualmente, `supersync/settings.py` contém valores sensíveis hardcoded (SECRET_KEY, credenciais do DB). Recomenda-se mover para variáveis de ambiente via `.env` e carregá-las com `os.environ` ou `django-environ`.

- SECRET_KEY: chave secreta do Django (produção deve usar valor forte e secreto)
- DEBUG: `True` ou `False` (produção: `False`)
- ALLOWED_HOSTS: lista de hosts permitidos (produção)
- Banco de dados (PostgreSQL):
  - DB_ENGINE: `django.db.backends.postgresql`
  - DB_NAME: nome do banco (ex.: `sync`)
  - DB_USER: usuário Postgres
  - DB_PASSWORD: senha Postgres
  - DB_HOST: host (ex.: `localhost`)
  - DB_PORT: porta (ex.: `5432`)

Exemplo `.env` (TODO: integrar leitura no settings.py):
```
SECRET_KEY=defina-uma-chave-forte
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sync
DB_USER=postgres
DB_PASSWORD=trocar-esta-senha
DB_HOST=localhost
DB_PORT=5432
```

## Comandos de Setup e Execução
- Criar migrações (se alterar modelos):
```
python manage.py makemigrations
python manage.py migrate
```
- Criar superusuário:
```
python manage.py createsuperuser
```
- Rodar servidor de desenvolvimento:
```
python manage.py runserver
```
- Checar versão do Django/diagnóstico:
```
python -m django --version
```

## Scripts/Management Commands
- Não há management commands customizados no repositório até o momento.
- Utilize os comandos padrão do Django via `manage.py` listados acima.

## Rotas e Autenticação
- Projetadas/Existentes:
  - Admin: `GET /admin/`
  - Accounts (definidas em `accounts/urls.py`):
    - `GET, POST /accounts/login/`
    - `POST /accounts/logout/` (logout somente via POST)
    - `GET /accounts/profile/`
- TODO: Incluir as rotas de `accounts` (e possíveis de `dashboard`/`contratos`) no `supersync/urls.py`, por exemplo:
```python
# supersync/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # path('', include('dashboard.urls', namespace='dashboard')),  # TODO se/ quando existir
]
```

### Observações de segurança
- O backend `usuarios.backends.PlainTextAuthBackend` compara senha em texto puro com o campo `password` de `SyncUsuario`. Isso NÃO é seguro e deve ser usado apenas para desenvolvimento/testes isolados.
- TODO: Substituir por armazenamento com hash (padrão Django `set_password()`/`check_password()`), remover campo duplicado `password` do modelo customizado (já herdado de `AbstractBaseUser`) e desativar o backend plaintext em produção.

## Testes
- Comando para rodar testes:
```
python manage.py test
```
- Arquivos `tests.py` existem nos apps, mas podem estar vazios. TODO: adicionar testes unitários/integração (autenticação, permissões, views e modelos).

## Estrutura do Projeto
```
C:/Users/alexandro.nascimento/supersync
├─ manage.py
├─ supersync/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ usuarios/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ backends.py
│  ├─ migrations/
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_alter_syncusuario_options.py
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  └─ views.py
├─ accounts/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ contratos/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  └─ views.py
├─ dashboard/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ tests.py
│  └─ views.py
└─ templates/
   ├─ base.html
   └─ accounts/
      ├─ login.html
      └─ profile.html
```

## Requisitos de Sistema e Banco de Dados
- Banco padrão no `settings.py`:
```
ENGINE: django.db.backends.postgresql
NAME: sync
USER: postgres
PASSWORD: 13752738  # mover para variável de ambiente
HOST: localhost
PORT: 5432
```
- TODO: externalizar credenciais e permitir configuração via variáveis de ambiente.

## Execução com Docker (opcional)
- TODO: Adicionar `Dockerfile` e `docker-compose.yml` com serviços para web e Postgres.

## Licença
- TODO: Definir licença do projeto (ex.: MIT, Apache-2.0). Adicionar arquivo LICENSE e atualizar esta seção.

## Créditos e Contribuição
- TODO: Adicionar informações de autores/mantenedores e diretrizes de contribuição.

## Changelog
- 2025-10-07: README inicial criado/atualizado com base no código do repositório.
