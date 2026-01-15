# Usa Python leve
FROM python:3.11-slim

# Evita arquivos .pyc e logs presos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala bibliotecas
COPY requirements.txt .
# Remove pywin32 caso tenha vindo do Windows (evita erro)
RUN sed -i '/pywin32/d' requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copia o código
COPY . .

# Comando de inicialização
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 supersync.wsgi:application