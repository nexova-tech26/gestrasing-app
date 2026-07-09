import smtplib
from email.message import EmailMessage
import os

# ==========================================
# CONFIGURACIÓN CENTRAL DE CORREO
# ==========================================
# El .strip() elimina espacios fantasma o saltos de línea de Windows (\r)
REMITENTE = os.getenv("SMTP_USER", "contacto.nexovatech@gmail.com").strip()
PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()

def enviar_alerta_reserva(reserva_data: dict, id_reserva: int):
    tarifa = reserva_data.get('tarifa_total', 0)
    tarifa_formateada = f"${tarifa:,.0f} COP".replace(",", ".")

    msg = EmailMessage()
    msg['Subject'] = f"🚨 NUEVA RESERVA #{id_reserva} - {reserva_data.get('tipo_servicio', 'No especificado').upper()}"
    msg['From'] = REMITENTE
    msg['To'] = REMITENTE 

    texto_pasajeros_extra = ""
    if reserva_data.get('pasajeros_adicionales'):
        texto_pasajeros_extra = "\nPASAJEROS ADICIONALES:\n"
        for i, p in enumerate(reserva_data['pasajeros_adicionales']):
            texto_pasajeros_extra += f"{i+1}. {p['nombre']} - CC: {p['cedula']}\n"

    contenido = f"""
    Se ha recibido una nueva solicitud de reserva.
    
    DETALLES DEL CLIENTE (TITULAR):
    - Nombre: {reserva_data.get('nombre', '')}
    - Cédula: {reserva_data.get('cedula', '')}
    - Teléfono: {reserva_data.get('telefono', '')}
    
    DETALLES DEL SERVICIO:
    - Modalidad: {reserva_data.get('tipo_servicio', '')}
    - Vehículo Asignado: {reserva_data.get('vehiculo_requerido', '')}
    - Ruta: {reserva_data.get('origen', '')} -> {reserva_data.get('destino', '')}
    - Dirección de recogida: {reserva_data.get('direccion_recogida', 'No especificada')}
    - Fecha: {reserva_data.get('fecha', '')}
    - Hora de Recogida: {reserva_data.get('hora', '')}
    - Total Pasajeros: {reserva_data.get('cantidad_pasajeros', 1)}
    - Total estimado: {tarifa_formateada}
    {texto_pasajeros_extra}
    
    Por favor, comuníquese con el cliente para confirmar.
    """
    msg.set_content(contenido)

    try:
        # SISTEMA DE AUDITORÍA
        print(f"⚙️ DEBUG SMTP (RESERVA) -> Servidor: {SMTP_SERVER}:465")
        print(f"⚙️ DEBUG SMTP (RESERVA) -> Usuario: '{REMITENTE}' | Longitud Password: {len(PASSWORD)}")
        
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(REMITENTE, PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Correo enviado para reserva #{id_reserva}")
    except Exception as e:
        print(f"❌ Error enviando email de reserva #{id_reserva}: {e}")


def enviar_alerta_cotizacion(datos: dict, id_cotizacion: int):
    msg = EmailMessage()
    msg['Subject'] = f"🔔 NUEVA SOLICITUD DE COTIZACIÓN #{id_cotizacion}"
    msg['From'] = REMITENTE
    msg['To'] = REMITENTE

    modalidad = datos.get('tipo_servicio', 'No especificada')
    if hasattr(modalidad, 'value'): 
        modalidad = modalidad.value
    elif isinstance(modalidad, str):
        modalidad = modalidad.replace('TipoServicio.', '')

    empresa = datos.get('empresa')
    texto_empresa = f"    - Empresa: {empresa}" if empresa and empresa.strip() else ""

    vehiculo = datos.get('vehiculo_requerido', datos.get('tipo_vehiculo', 'No especificado'))
    if hasattr(vehiculo, 'value'):
        vehiculo = vehiculo.value

    contenido = f"""
    Se ha recibido una nueva solicitud de Cotización.
    
    DETALLES DEL CLIENTE:
    - Nombre: {datos.get('nombre', '')}
    - Email: {datos.get('email', '')}
    - Teléfono: {datos.get('telefono', '')}
    {texto_empresa}
 
    DETALLES DEL SERVICIO A COTIZAR:
    - Modalidad: {modalidad.capitalize() if isinstance(modalidad, str) else modalidad}
    - Vehículo Requerido: {vehiculo}
    - Origen: {datos.get('origen', '')}
    - Destino: {datos.get('destino', '')}
    - Fecha: {datos.get('fecha_servicio', 'Por definir')}
    - Cantidad de Pasajeros: {datos.get('cantidad_pasajeros', 1)}
    - Detalles adicionales: {datos.get('detalles_adicionales', 'Sin detalles adicionales')}
    """
    
    contenido_limpio = "\n".join([linea for linea in contenido.split('\n') if linea.strip() != "" or linea == ""])
    contenido_limpio += "\n\nPor favor, prepare la propuesta comercial y contacte al cliente."

    msg.set_content(contenido_limpio)

    try:
        # SISTEMA DE AUDITORÍA
        print(f"⚙️ DEBUG SMTP (COTIZACIÓN) -> Servidor: {SMTP_SERVER}:465")
        print(f"⚙️ DEBUG SMTP (COTIZACIÓN) -> Usuario: '{REMITENTE}' | Longitud Password: {len(PASSWORD)}")

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(REMITENTE, PASSWORD)
            smtp.send_message(msg)
            print(f"✅ Correo enviado para COTIZACIÓN #{id_cotizacion}")
    except Exception as e:
        print(f"❌ Error enviando email de cotización #{id_cotizacion}: {e}")