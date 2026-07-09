# backend/app/schemas/cotizacion.py
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import date
from enum import Enum

# ================= ENUMERADORES (Tipado Estricto) =================
# Restringimos los valores exactos que la API puede recibir, 
# evitando errores tipográficos ("Privado" vs "privado")

class TipoServicio(str, Enum):
    COMPARTIDO = "compartido"
    PRIVADO = "privado"
    CORPORATIVO = "corporativo"

class TipoVehiculo(str, Enum):
    DUSTER = "duster"
    MINIVAN = "minivan"
    VAN = "van"
    BUS = "bus"

# ================= ESQUEMA DE VALIDACIÓN =================

class CotizacionForm(BaseModel):
    """
    Esquema estricto para la recepción de solicitudes de cotización o reserva.
    Aplica reglas de negocio y validación cruzada antes de procesar cualquier dato.
    """
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre completo del cliente")
    email: EmailStr = Field(..., description="Correo electrónico válido para notificaciones")
    telefono: str = Field(..., min_length=7, max_length=20, description="Número de contacto")
    
    # Nuevos campos tipados estrictamente con Enum
    tipo_servicio: TipoServicio = Field(..., description="Modalidad: compartido, privado o corporativo")
    vehiculo_requerido: TipoVehiculo = Field(..., description="Vehículo solicitado: duster, minivan, van, bus")
    
    origen: str = Field(..., min_length=2, max_length=100)
    destino: str = Field(..., min_length=2, max_length=100)
    fecha_servicio: date = Field(..., description="Fecha requerida para el servicio en formato YYYY-MM-DD")
    
    cantidad_pasajeros: int = Field(..., gt=0, description="Número de personas a transportar")
    detalles_adicionales: Optional[str] = Field(None, max_length=500)

    # ================= REGLAS DE NEGOCIO (Validación Cruzada) =================
    @model_validator(mode='after')
    def validar_vehiculo_por_servicio(self) -> 'CotizacionForm':
        """
        Garantiza que si el servicio es 'compartido', el vehículo sea obligatoriamente una 'duster'.
        Los servicios privados y corporativos permiten cualquier vehículo.
        """
        # Regla: Servicio Compartido -> Solo Duster
        if self.tipo_servicio == TipoServicio.COMPARTIDO:
            if self.vehiculo_requerido != TipoVehiculo.DUSTER:
                raise ValueError("El servicio compartido solo está disponible en la Camioneta Duster.")
        
        # (Opcional a futuro): Aquí podrías agregar más reglas, 
        # ejemplo: si vehículo es DUSTER, cantidad_pasajeros no puede ser mayor a 4.
        
        return self