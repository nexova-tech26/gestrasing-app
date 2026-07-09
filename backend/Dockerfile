# Usamos una imagen oficial super ligera de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza a que los logs se impriman directo en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Optimizacion de cache: Copiamos SOLO requirements primero. 
# Si mañana cambias una línea de código, Docker no volverá a descargar las librerías.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del backend
COPY . .

EXPOSE 8000

# Comando de arranque (OJO: Sin --reload, eso es solo para desarrollo)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]