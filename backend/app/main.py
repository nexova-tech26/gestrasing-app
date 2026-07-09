from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import rutas_cotizacion 
from app.core.database import engine, Base
from app.models import cotizacion_model, reserva_model
from app.api import rutas_reserva

# ================= CREA LAS TABLAS EN LA BD FISICA ================

Base.metadata.create_all(bind=engine)

# ================= CONFIGURACIÓN DE LA APLICACIÓN =================
# Inicializamos FastAPI con metadatos descriptivos que alimentarán 
# la documentación automática de Swagger UI (/docs)
app = FastAPI(
    title="API Transaccional Gestrasing",
    description="Motor backend para reservas, cotizaciones y formularios de contacto.",
    version="1.0.0"
)

# ================= CONFIGURACIÓN DE SEGURIDAD (CORS) =================
# Definimos qué dominios (orígenes) tienen permiso para hablar con nuestro backend.
# En desarrollo, Vite corre por defecto en el puerto 5173.
ORIGINS = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    # NOTA: Al pasar a producción, aquí debes agregar el dominio real (ej. https://gestrasing.com)
]

# Inyectamos el middleware de CORS para interceptar y autorizar el tráfico
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,         # Permite los dominios declarados arriba
    allow_credentials=True,        # Permite el envío de cookies/tokens de autenticación
    allow_methods=["*"],           # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],           # Permite todas las cabeceras personalizadas
)

# ================= REGISTRO DE ENRUTADORES =================
# Conectamos las rutas modulares a la aplicación principal
app.include_router(rutas_cotizacion.router)
app.include_router(rutas_reserva.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"estado": "Operativo", "servicio": "API Gestrasing S.A.S."}

# IMPORTANTE: Más adelante, aquí registraremos los "routers" (ej. app.include_router(reservas.router))