# backend/app/models/reserva_model.py
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

# 1. TABLA PRINCIPAL (Arriba)
class ReservaDB(Base):
    __tablename__ = "reservas"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), nullable=False)
    telefono = Column(String(20), nullable=False)
    
    tipo_servicio = Column(String(50), nullable=False)
    vehiculo_requerido = Column(String(50), nullable=False)
    
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    direccion_recogida = Column(String(200), nullable=False)
    
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    estado = Column(String(20), default="pendiente")
    
    cantidad_pasajeros = Column(Integer, default=1)
    tarifa_total = Column(Integer, default = 0 )
    pasajeros_adicionales = relationship("PasajeroAdicionalDB", )
    

# 2. TABLA SECUNDARIA (Abajo)
class PasajeroAdicionalDB(Base):
    __tablename__ = "pasajeros_adicionales"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id", ondelete="CASCADE"))
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), nullable=False)
 
    # Usamos "backref". Esto le dice a SQLAlchemy: "Conéctame con ReservaDB 
    # y automáticamente créale a ReservaDB una lista llamada 'pasajeros_adicionales'".
    # Al pasar la clase ReservaDB directamente (sin comillas), jamás habrá error de "Multiple classes".
    reserva = relationship(ReservaDB, back_populates="pasajeros_adicionales")