# Usar imagen oficial de Playwright con Python
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para datos
RUN mkdir -p data

# Variables de entorno
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 10000

# Comando para iniciar la aplicación
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
