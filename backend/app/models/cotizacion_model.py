# backend/app/models/cotizacion_model.py
from sqlalchemy import Column, Integer, String, Date, Text, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CotizacionDB(Base):
    """
    Representación exacta de la tabla 'cotizaciones' en la base de datos.
    """
    __tablename__ = "cotizaciones"

    # Llave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del cliente
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=False)
    
    # Datos del servicio
    tipo_servicio = Column(String(50), nullable=False)
    vehiculo_requerido = Column(String(50), nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    fecha_servicio = Column(Date, nullable=False)
    cantidad_pasajeros = Column(Integer, nullable=False)
    
    # Detalles extra (puede ser nulo)
    detalles_adicionales = Column(Text, nullable=True)
