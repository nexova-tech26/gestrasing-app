# backend/app/api/rutas_cotizacion.py
from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.orm import Session

# Importamos el validador (Pydantic), el modelo (SQLAlchemy) y la conexión (Base de Datos)
from app.schemas.cotizacion import CotizacionForm
from app.models.cotizacion_model import CotizacionDB
from app.core.database import get_db
from app.core.email_service import enviar_alerta_cotizacion

router = APIRouter(
    prefix="/api/v1/cotizaciones",
    tags=["Cotizaciones y Reservas"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_cotizacion(
    cotizacion: CotizacionForm,
    background_tasks: BackgroundTasks, # <-- INYECTA LA TAREA EN SEGUNDO PLANO
    db: Session = Depends(get_db)
):
    # 1. Guardamos en la base de datos
    nueva_cotizacion = CotizacionDB(**cotizacion.model_dump())
    db.add(nueva_cotizacion)
    db.commit()
    db.refresh(nueva_cotizacion)
    
    # 2. ENVIAMOS EL CORREO EN SEGUNDO PLANO
    background_tasks.add_task(enviar_alerta_cotizacion, datos=cotizacion.model_dump(), id_cotizacion=int(nueva_cotizacion.id))
    
    return {"status": "success", "id_cotizacion": nueva_cotizacion.id}