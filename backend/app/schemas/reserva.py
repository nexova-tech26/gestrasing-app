# backend/app/schemas/reserva.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, time

# Sub-modelo para los pasajeros extra
class PasajeroAdicional(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    cedula: str = Field(..., min_length=5, max_length=20)

class ReservaForm(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    cedula: str = Field(..., min_length=5, max_length=20)
    telefono: str = Field(..., min_length=7, max_length=20)
    
    tipo_servicio: str = Field(...)
    vehiculo_requerido: str = Field(...)
    
    origen: str = Field(..., min_length=2)
    destino: str = Field(..., min_length=2)
    direccion_recogida: str = Field(..., min_length=5, max_length=200, description="Dirección exacta donde se recoge al cliente")
    
    fecha: date = Field(...)
    hora: time = Field(...)
    
    cantidad_pasajeros: int = Field(default=1, gt=0)
    tarifa_total: int = Field(default=0, description="Costo total calculado en el frontend")
    pasajeros_adicionales: Optional[List[PasajeroAdicional]] = []