# backend/app/api/rutas_reserva.py
from fastapi import APIRouter, Depends, status, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.schemas.reserva import ReservaForm
# Importamos ambos modelos de forma global al inicio
from app.models.reserva_model import ReservaDB, PasajeroAdicionalDB
from app.core.database import get_db
from app.core.email_service import enviar_alerta_reserva

router = APIRouter(
    prefix="/api/v1/reservas",
    tags=["Reservas On-Demand"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def procesar_reserva(
    reserva: ReservaForm, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    try:
        # 1. Separamos los pasajeros extra
        reserva_data = reserva.model_dump(exclude={"pasajeros_adicionales"})
        
        # 2. Guardamos la reserva principal
        nueva_reserva = ReservaDB(**reserva_data)
        db.add(nueva_reserva)
        db.commit()
        db.refresh(nueva_reserva)
        
        # 3. Guardamos los acompañantes
        if reserva.pasajeros_adicionales:
            for pasajero in reserva.pasajeros_adicionales:
                nuevo_pasajero = PasajeroAdicionalDB(**pasajero.model_dump(), reserva_id=nueva_reserva.id)
                db.add(nuevo_pasajero)
            db.commit()
        
        # 4. Enviamos correo...
        background_tasks.add_task(enviar_alerta_reserva, reserva_data=reserva.model_dump(), id_reserva=int(nueva_reserva.id))
        
        return {"status": "success", "id_reserva": nueva_reserva.id}

    except Exception as e:
        # 🚨 ESTO IMPRIMIRÁ EL ERROR EN GIGANTE EN TU TERMINAL 🚨
        print("\n" + "="*50)
        print("🚨 EL VERDADERO ERROR ES ESTE 🚨:")
        print(repr(e))
        print("="*50 + "\n")
        
        # ESTO EVITA EL ERROR DE CORS Y LE ENVÍA EL ERROR AL FRONTEND
        raise HTTPException(status_code=500, detail=str(e))