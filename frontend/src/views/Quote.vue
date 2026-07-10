<script setup>
import { ref, reactive, watch,computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '@vueuse/head'
import { useRoute } from 'vue-router'

const mostrarExito = ref(false);

//funcion dedicada a limpiar el formulario para reutilizarla
const limpiarFormulario = () => {
  reserveData.nombre = '';
  reserveData.cedula = '';
  reserveData.telefono = '';
  reserveData.tipo_servicio = 'Compartido';
  reserveData.vehiculo_requerido = '';
  reserveData.origen_select = '';
  reserveData.origen_otro = '';
  reserveData.destino_select = '';
  reserveData.destino_otro = '';
  reserveData.direccion_recogida = '';
  reserveData.fecha = '';
  reserveData.hora = '';
  reserveData.cantidad_pasajeros = 1;
};

const { t } = useI18n()

const route = useRoute()

useHead({
  title: () => `${t('quotePage.title')} | Gestrasing S.A.S.`
})

const today = new Date().toISOString().split('T')[0]

// ================= ESTADO DE MACRO-PESTAÑAS =================
// Lee la url y si dice ?tab=reserve abre esa pestaña, sino, abre quote por defecto
const mainTab = ref(route.query.tab === 'reserve' ? 'reserve' : 'quote')

// ================= ESTADO: FORMULARIO DE COTIZACIÓN =================
const formData = reactive({
  nombre: '',
  email: '',
  telefono: '',
  tipo_servicio: 'privado',
  vehiculo_requerido: 'van',
  origen: '',
  destino: '',
  fecha_servicio: '',
  cantidad_pasajeros: 1,
  direccion_recogida: '',
  detalles_adicionales: ''
})

const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref(false)
const idReserva = ref(null)

// Regla de Negocio: Si es compartido, fuerza la Duster.
watch(() => formData.tipo_servicio, (newVal) => {
  const servicio = newVal?.toLowerCase() || ''
  
  if (servicio === 'compartido') {
    // Debe coincidir exactamente con el texto del arreglo todosLosVehiculos
    formData.vehiculo_requerido = 'Camioneta Duster' 
  } else if (servicio === 'privado' || servicio === 'corporativo') {
    if (formData.vehiculo_requerido === 'Bus Intermunicipal') {
      formData.vehiculo_requerido = '' // Resetea si el vehículo no es válido
    }
  }
})

const submitCotizacion = async () => {
  isSubmitting.value = true
  submitSuccess.value = false
  submitError.value = false

  // DICCIONARIO DE TRADUCCIÓN (De texto de la interfaz a código backend)
  const mapaVehiculos = {
    'Camioneta Duster': 'duster',
    'Minivan': 'minivan',
    'Van': 'van',
    'Bus Intermunicipal': 'bus'
  };

  // 1. Armamos el paquete EXACTO que el backend necesita filtrando la basura
const payload = {
    nombre: formData.nombre,
    email: formData.email,
    telefono: formData.telefono,
    tipo_servicio: formData.tipo_servicio,
    
    // Usamos el traductor. Si eligen 'Camioneta Duster', enviará 'duster'
    vehiculo_requerido: mapaVehiculos[formData.vehiculo_requerido] || formData.vehiculo_requerido,
    
    origen: formData.origen,
    destino: formData.destino,
    fecha_servicio: formData.fecha_servicio, 
    direccion_recogida: formData.direccion_recogida,
    cantidad_pasajeros: Number(formData.cantidad_pasajeros),
    
    // Agregamos detalles adicionales por si el backend lo espera
    detalles_adicionales: formData.detalles_adicionales || "Sin detalles",
    empresa: "N/A" // Lo enviamos por defecto en caso de que el backend lo exija
  }

try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/cotizaciones/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    // 2. Si el guardia rechaza el paquete, leemos exactamente por qué
    if (!response.ok) {
      const errorData = await response.json()
      console.error(" MOTIVO DEL RECHAZO (422):", errorData.detail)
      throw new Error('Validación rechazada por el backend')
    }

    const data = await response.json()
    
    // el backend de cotizaciones debería estar devolviendo id_cotizacion
    idReserva.value = data.id_cotizacion || data.id_reserva 
    
    submitSuccess.value = true
  } catch (error) {
    console.error("Error al enviar cotización:", error)
    submitError.value = true
  } finally {
    isSubmitting.value = false
  }
}

// ================= ESTADO: FORMULARIO DE RESERVA =================
const reserveData = reactive({
  nombre: '',
  cedula: '',
  telefono: '',
  tipo_servicio: 'compartido',
  vehiculo_requerido: 'duster',
  origen_select: 'Villavicencio',  
  origen_otro: '',
  direccion_recogida: '',
  destino_select: 'Bogotá',
  destino_otro: '',
  fecha: '',
  hora: '',
  vehiculo_requerido: '',
  cantidad_pasajeros: 1, 
  pasajeros_adicionales: []
})

const todosLosVehiculos = [ 
  'Camioneta Duster', 
  'Minivan', 
  'Van', 
  'Bus Intermunicipal'
];


// Si el servicio es Privado o Corporativo, excluimos el Bus Intermunicipal
// Propiedad computada para filtrar vehículos en COTIZACIÓN
const vehiculosCotizacionFiltrados = computed(() => {
  // Observamos la variable correcta: formData
  const tipo = formData.tipo_servicio?.toLowerCase() || '';
  
  // Si es compartido, la lista se reduce a una sola opción
  if (tipo === 'compartido') {
    return ['Camioneta Duster'];
  }
  
  if (tipo === 'privado' || tipo === 'corporativo') {
    return todosLosVehiculos;
  }
  
  return todosLosVehiculos;
});

// 4. Propiedad computada para calcular la tarifa exacta en tiempo real
const tarifaTotalCalculada = computed(() => {
const tipo = reserveData.tipo_servicio.toLowerCase();
const vehiculo = reserveData.vehiculo_requerido.toLowerCase();
const pasajeros = reserveData.cantidad_pasajeros || 1;

if (tipo === 'compartido') {
  return 130000 * pasajeros;
} 
//la van y mini van completas cuestan 650000
if (tipo === 'privado' || tipo === 'corporativo') {
  if (vehiculo === 'minivan' || vehiculo === 'van') {
    return 650000;
  }
  // Tarifa base para privado y corporativo en vehículos estándar
  return 360000; 
}

return 0;
});

const formatearMoneda = (valor) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(valor)
}

watch(() => reserveData.cantidad_pasajeros, (newVal) => {
  // Evitamos que pongan números locos (mínimo 1, máximo 8)
  if (newVal < 1) reserveData.cantidad_pasajeros = 1
  if (newVal > 8) reserveData.cantidad_pasajeros = 8

  const numAcompanantes = reserveData.cantidad_pasajeros - 1
  
  // Si aumentan pasajeros, agregamos objetos vacíos al arreglo
  if (numAcompanantes > reserveData.pasajeros_adicionales.length) {
    for (let i = reserveData.pasajeros_adicionales.length; i < numAcompanantes; i++) {
      reserveData.pasajeros_adicionales.push({ nombre: '', cedula: '' })
    }
  } 
  // Si disminuyen, cortamos el arreglo
  else if (numAcompanantes < reserveData.pasajeros_adicionales.length) {
    reserveData.pasajeros_adicionales.splice(numAcompanantes)
  }
})

// Regla 1: Bloqueo de Vehículo y Destinos según Servicio
watch(() => reserveData.tipo_servicio, (newVal) => {
  // Si es compartido, fuerza la Duster
  if (newVal === 'compartido') {
    reserveData.vehiculo_requerido = 'duster'
  }
  
  // Si deja de ser corporativo, resetea "Otro" a las ciudades base
  if (newVal !== 'corporativo') {
    if (reserveData.origen_select === 'Otro') reserveData.origen_select = 'Villavicencio'
    if (reserveData.destino_select === 'Otro') reserveData.destino_select = 'Bogotá'
  }
  
  validateTime() // Re-valida la hora al cambiar las reglas
})

// ================= VALIDACIÓN DE CIUDADES (No permitir iguales) =================

// Observar cambios en el origen
watch(() => reserveData.origen_select, (newVal) => {
  if (newVal !== 'Otro' && newVal === reserveData.destino_select) {
    // Si eligen el mismo, cambiamos el destino al opuesto
    reserveData.destino_select = newVal === 'Villavicencio' ? 'Bogotá' : 'Villavicencio'
  }
})

// Observar cambios en el destino
watch(() => reserveData.destino_select, (newVal) => {
  if (newVal !== 'Otro' && newVal === reserveData.origen_select) {
    // Si eligen el mismo, cambiamos el origen al opuesto
    reserveData.origen_select = newVal === 'Villavicencio' ? 'Bogotá' : 'Villavicencio'
  }
})

// Regla extra: Si el servicio no es corporativo y ambos quedan en 'Otro', resetear a valores base
watch(() => reserveData.tipo_servicio, (newVal) => {
  if (newVal !== 'corporativo') {
    if (reserveData.origen_select === 'Otro') reserveData.origen_select = 'Villavicencio'
    if (reserveData.destino_select === 'Otro') reserveData.destino_select = 'Bogotá'
  }
  
  // Forzar que no sean iguales tras el cambio de tipo de servicio
  if (reserveData.origen_select === reserveData.destino_select && reserveData.origen_select !== 'Otro') {
    reserveData.destino_select = reserveData.origen_select === 'Villavicencio' ? 'Bogotá' : 'Villavicencio'
  }
  
  validateTime()
})

// Regla 2: Cálculo Dinámico de Hora Mínima
const currentOffsetHours = computed(() => {
  if (reserveData.tipo_servicio === 'privado') return 1
  if (reserveData.tipo_servicio === 'compartido') return 2
  return 4
})

const minReserveTime = computed(() => {
  if (reserveData.fecha && reserveData.fecha !== today) return "00:00"
  
  const now = new Date()
  now.setHours(now.getHours() + currentOffsetHours.value)
  
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  return `${h}:${m}`
})

// Regla 3: Bloqueo estricto de la hora (Forzar corrección en UI)
const validateTime = () => {
  if (reserveData.fecha === today && reserveData.hora) {
    if (reserveData.hora < minReserveTime.value) {
      reserveData.hora = minReserveTime.value // Sobrescribe la hora inválida automáticamente
    }
  }
}

// Escuchar cambios en la fecha para re-validar la hora inmediatamente
watch(() => reserveData.fecha, () => validateTime())

// Agrega estas variables de estado justo arriba de la función si no las tienes:
const isReserving = ref(false)
const reserveSuccess = ref(false)
const reserveError = ref(false)
const errorMessage = ref('')
const idReservaInmediata = ref(null)


const submitReserva = async () => {
  // 1. Construimos el paquete
  const payload = {
    nombre: reserveData.nombre,
    cedula: reserveData.cedula,
    telefono: reserveData.telefono,
    tipo_servicio: reserveData.tipo_servicio,
    vehiculo_requerido: reserveData.vehiculo_requerido,
    origen: reserveData.origen_select === 'Otro' ? reserveData.origen_otro : reserveData.origen_select,
    destino: reserveData.destino_select === 'Otro' ? reserveData.destino_otro : reserveData.destino_select,
    direccion_recogida: reserveData.direccion_recogida,
    fecha: reserveData.fecha,
    hora: reserveData.hora.length === 5 ? reserveData.hora + ":00" : reserveData.hora, // formato HH:MM:SS
    cantidad_pasajeros: reserveData.cantidad_pasajeros, 
    pasajeros_adicionales: reserveData.pasajeros_adicionales,
    tarifa_total: tarifaTotalCalculada.value
  }

try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/reservas/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      // Si el servidor responde correctamente, mostramos el mensaje
      mostrarExito.value = true;
      
      // Limpiamos los campos del formulario
      limpiarFormulario();
      
      // Ocultamos el mensaje automaticamente despues de 5 segundos
      setTimeout(() => {
        mostrarExito.value = false;
      }, 5000);
      
    } else {
      console.error("Error validando los datos en el servidor");
      // Aqui podrias manejar una alerta de error si lo deseas
    }
  } catch (error) {
    console.error("Error de red:", error);
  }

  // IMPRIMIMOS LO QUE VAMOS A ENVIAR - NO OLVIDAR QUITARRRR
  console.log("📦 PAYLOAD A ENVIAR:", payload)

  isReserving.value = true
  reserveSuccess.value = false
  reserveError.value = false
  errorMessage.value = ''

}

</script>

<template>
  <div class="bg-gray-50 min-h-screen py-16 md:py-24">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center mb-12">
        <h1 class="text-3xl md:text-5xl font-extrabold text-ges-black mb-4">{{ t('quotePage.title') }}</h1>
        <div class="h-1 w-24 bg-ges-green mx-auto mb-4 rounded"></div>
        <p class="text-lg text-gray-600">{{ t('quotePage.subtitle') }}</p>
      </div>

      <div class="flex flex-col sm:flex-row justify-center border-b border-gray-200 mb-10">
        <button
          aria-label="tab de cotización"
          @click="mainTab = 'quote'" 
          :class="['px-8 py-4 text-lg font-bold transition-colors border-b-4 flex items-center justify-center gap-2', mainTab === 'quote' ? 'border-ges-green text-ges-green' : 'border-transparent text-gray-500 hover:text-ges-black']">
          <i class="pi pi-file-edit"></i> {{ t('quotePage.mainTabs.quote') }}
        </button>
        <button
          aria-label="tab de reserva" 
          @click="mainTab = 'reserve'" 
          :class="['px-8 py-4 text-lg font-bold transition-colors border-b-4 flex items-center justify-center gap-2', mainTab === 'reserve' ? 'border-ges-green text-ges-green' : 'border-transparent text-gray-500 hover:text-ges-black']">
          <i class="pi pi-ticket"></i> {{ t('quotePage.mainTabs.reserve') }}
        </button>
      </div>

      <div 
        v-if="mostrarExito" 
        class="mb-6 p-4 bg-green-50 border border-green-500 text-green-800 rounded-lg font-medium text-center transition-all duration-500"
      >
        Su reserva ha sido solicitada exitosamente. Un asesor revisará su solicitud y se comunicará pronto.
      </div>

      <div v-if="mainTab === 'quote'" class="bg-white rounded-[2rem] shadow-xl p-8 md:p-12 border border-gray-100 animate-fade-in">
        
        <div v-if="submitSuccess" class="bg-green-50 border-l-4 border-ges-green p-4 mb-8 rounded-r-lg flex items-center gap-3 text-green-800">
          <i class="pi pi-check-circle text-2xl"></i>
          <div><p class="font-bold">{{ t('quotePage.form.success') }}{{ idReserva }}</p></div>
        </div>

        <div v-if="submitError" class="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-r-lg flex items-center gap-3 text-red-800">
          <i class="pi pi-times-circle text-2xl"></i>
          <p class="font-bold">{{ t('quotePage.form.error') }}</p>
        </div>

        <form v-if="!submitSuccess" @submit.prevent="submitCotizacion" class="space-y-8">
          
          <div>
            <h1 class="text-xl font-bold text-ges-black mb-4 border-b pb-2 flex items-center gap-2">
              <i class="pi pi-user text-ges-green"></i> {{ t('quotePage.form.personalData') }}
            </h1>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.name') }} *</label>
                <input v-model="formData.nombre" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.email') }} *</label>
                <input v-model="formData.email" type="email" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.phone') }} *</label>
                <input v-model="formData.telefono" type="tel" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
            </div>
          </div>

          <div>
            <h2 class="text-xl font-bold text-ges-black mb-6 border-b pb-2 flex items-center gap-2">
              <i class="pi pi-map-marker text-ges-green"></i> {{ t('quotePage.form.serviceData') }}
            </h2>
            
            <div class="mb-8">
              <label class="block text-sm font-semibold text-gray-700 mb-3">{{ t('quotePage.form.serviceType') }} *</label>
              <div class="flex flex-col sm:flex-row rounded-lg border border-gray-200 overflow-hidden">
                <button type="button" @click="formData.tipo_servicio = 'privado'" :class="['flex-1 py-3 px-4 font-bold transition-colors text-center border-b-2 sm:border-b-0 sm:border-r', formData.tipo_servicio === 'privado' ? 'bg-ges-green/10 text-ges-green' : 'bg-white text-gray-500 hover:bg-gray-50']">
                  <i class="pi pi-car mr-2"></i> {{ t('quotePage.options.services.privado') }}
                </button>
                <button type="button" @click="formData.tipo_servicio = 'corporativo'" :class="['flex-1 py-3 px-4 font-bold transition-colors text-center border-b-2 sm:border-b-0 sm:border-r', formData.tipo_servicio === 'corporativo' ? 'bg-ges-green/10 text-ges-green' : 'bg-white text-gray-500 hover:bg-gray-50']">
                  <i class="pi pi-briefcase mr-2"></i> {{ t('quotePage.options.services.corporativo') }}
                </button>
                <button type="button" @click="formData.tipo_servicio = 'compartido'" :class="['flex-1 py-3 px-4 font-bold transition-colors text-center', formData.tipo_servicio === 'compartido' ? 'bg-ges-green/10 text-ges-green' : 'bg-white text-gray-500 hover:bg-gray-50']">
                  <i class="pi pi-users mr-2"></i> {{ t('quotePage.options.services.compartido') }}
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.vehicleType') }} *</label>
                <select v-model="formData.vehiculo_requerido" required class="w-full px-4 py-3 rounded-lg border border-gray-300">
                    <option value="" disabled>Seleccione un vehículo</option>
                    <option v-for="vehiculo in vehiculosCotizacionFiltrados" :key="vehiculo" :value="vehiculo">
                      {{ vehiculo }}
                    </option>
                </select>
                <p v-if="formData.tipo_servicio === 'compartido'" class="text-xs text-amber-600 mt-1 font-semibold">
                  
                  <i class="pi pi-info-circle"></i> El servicio compartido opera exclusivamente en Camioneta Duster.
                </p>


              </div>
              <div class="hidden md:block"></div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.origin') }} *</label>
                <input v-model="formData.origen" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.destination') }} *</label>
                <input v-model="formData.destino" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
              <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.pickupAddress') }} *</label>
            <input v-model="formData.direccion_recogida" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" placeholder="Ej: Calle 45 # 12-34, Barrio Centro" />
          </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.date') }} *</label>
                <input v-model="formData.fecha_servicio" type="date" :min="today" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              </div>
<div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.passengers') }} *</label>
                
                <div class="flex items-center border border-gray-300 rounded-lg focus-within:ring-2 focus-within:ring-ges-green overflow-hidden">
                  
                  <button
                    aria-label="cantidad pasajeros" 
                    type="button" 
                    @click="formData.cantidad_pasajeros > 1 ? formData.cantidad_pasajeros-- : null"
                    class="px-5 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 font-bold border-r border-gray-300 transition-colors focus:outline-none select-none"
                  >
                    −
                  </button>
                  
                  <input 
                    v-model="formData.cantidad_pasajeros" 
                    type="number" 
                    min="1" 
                    required 
                    class="w-full text-center py-3 outline-none appearance-none m-0 ocultar-flechas" 
                  />
                  
                  <button 
                    type="button" 
                    @click="formData.cantidad_pasajeros++"
                    class="px-5 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 font-bold border-l border-gray-300 transition-colors focus:outline-none select-none"
                  >
                    +
                  </button>
                  
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.details') }}</label>
                <textarea v-model="formData.detalles_adicionales" rows="3" class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none resize-none"></textarea>
              </div>
            </div>
          </div>

          <button aria-label="boton enviar" type="submit" :disabled="isSubmitting" class="w-full bg-ges-black hover:bg-gray-800 text-white font-bold py-4 px-8 rounded-full shadow-lg transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2">
            <i v-if="isSubmitting" class="pi pi-spin pi-spinner"></i>
            {{ isSubmitting ? t('quotePage.form.loading') : t('quotePage.form.submit') }}
          </button>
        </form>
      </div>
    </div>

<div v-if="reserveError" class="bg-red-50 border-l-4 border-red-500 p-4 mb-8 rounded-r-lg flex items-center gap-3 text-red-800">
          <i class="pi pi-times-circle text-2xl"></i>
          <div>
            <p class="font-bold">Solicitud rechazada</p>
            <p class="text-sm mt-1">{{ errorMessage }}</p>
          </div>
        </div>

<div v-if="mainTab === 'reserve'" class="bg-white rounded-[2rem] shadow-xl p-8 md:p-12 border border-gray-100 animate-fade-in max-w-4xl mx-auto">
        <h3 class="text-2xl font-bold text-ges-black mb-8 flex items-center gap-2 border-b pb-4">
          <i class="pi pi-calendar-plus text-ges-green"></i> {{ t('quotePage.reserveForm.title') }}
        </h3>
        
        <form @submit.prevent="submitReserva" class="space-y-6">
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.name') }} *</label>
              <input v-model="reserveData.nombre" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.idNumber') }} *</label>
              <input v-model="reserveData.cedula" type="text" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.phone') }} *</label>
              <input v-model="reserveData.telefono" type="tel" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 bg-gray-50 p-6 rounded-xl border border-gray-100">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.serviceType') }} *</label>
              <select v-model="reserveData.tipo_servicio" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green bg-white outline-none">
                <option value="compartido">{{ t('quotePage.options.services.compartido') }}</option>
                <option value="privado">{{ t('quotePage.options.services.privado') }}</option>
                <option value="corporativo">{{ t('quotePage.options.services.corporativo') }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.vehicleType') }} *</label>
              <select v-model="reserveData.vehiculo_requerido" :disabled="reserveData.tipo_servicio === 'compartido'" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green bg-white outline-none disabled:bg-gray-200">
                <option value="duster">{{ t('quotePage.options.vehicles.duster') }}</option>
                <option value="minivan" :disabled="reserveData.tipo_servicio === 'compartido'">{{ t('quotePage.options.vehicles.minivan') }}</option>
                <option value="van" :disabled="reserveData.tipo_servicio === 'compartido'">{{ t('quotePage.options.vehicles.van') }}</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.origin') }} *</label>
              <select v-model="reserveData.origen_select" class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green bg-white outline-none mb-2">
                <option value="Villavicencio">Villavicencio</option>
                <option value="Bogotá">Bogotá</option>
                <option v-if="reserveData.tipo_servicio === 'corporativo'" value="Otro">{{ t('quotePage.reserveForm.otherOption') }}</option>
              </select>
              <input v-if="reserveData.origen_select === 'Otro'" v-model="reserveData.origen_otro" type="text" :placeholder="t('quotePage.reserveForm.specifyOther')" required class="w-full px-4 py-2 text-sm rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none bg-amber-50" />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.destination') }} *</label>
              <select v-model="reserveData.destino_select" class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green bg-white outline-none mb-2">
                <option value="Bogotá">Bogotá</option>
                <option value="Villavicencio">Villavicencio</option>
                <option v-if="reserveData.tipo_servicio === 'corporativo'" value="Otro">{{ t('quotePage.reserveForm.otherOption') }}</option>
              </select>
              <input v-if="reserveData.destino_select === 'Otro'" v-model="reserveData.destino_otro" type="text" :placeholder="t('quotePage.reserveForm.specifyOther')" required class="w-full px-4 py-2 text-sm rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none bg-amber-50" />
            </div>
          </div>
          <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.pickupAddress') }} *</label>
            <input v-model="reserveData.direccion_recogida" type="text"  class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" placeholder="Ej: Calle 45 # 12-34, Barrio Centro" />
          </div>
          <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg flex justify-between items-center">
            <span class="text-gray-800 font-semibold">Valor Total Estimado:</span>
            <span class="text-2xl text-green-700 font-bold">{{ formatearMoneda(tarifaTotalCalculada) }}</span>
          </div>
          <div class="border-t pt-6">
            <!-- <div class="w-full md:w-1/3 mb-4">
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.passengers') }} *</label>
              <input v-model="reserveData.cantidad_pasajeros" type="number" min="1" max="15" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
            </div> -->
            <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.form.passengers') }} *</label>
                
                <div class="flex items-center border border-gray-300 rounded-lg focus-within:ring-2 focus-within:ring-ges-green overflow-hidden">
                  
                  <button 
                    type="button" 
                    @click="reserveData.cantidad_pasajeros > 1 ? reserveData.cantidad_pasajeros-- : null"
                    class="px-5 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 font-bold border-r border-gray-300 transition-colors focus:outline-none select-none"
                  >
                    −
                  </button>
                  
                  <input 
                    v-model="reserveData.cantidad_pasajeros" 
                    type="number" 
                    min="1" 
                    required 
                    class="w-full text-center py-3 outline-none appearance-none m-0 ocultar-flechas" 
                  />
                  
                  <button 
                    type="button" 
                    @click="reserveData.cantidad_pasajeros++"
                    class="px-5 py-3 bg-gray-50 hover:bg-gray-100 text-gray-600 font-bold border-l border-gray-300 transition-colors focus:outline-none select-none"
                  >
                    +
                  </button>
                  
                </div>
              </div>

            <div v-if="reserveData.pasajeros_adicionales.length > 0" class="space-y-4 bg-ges-green/5 p-6 rounded-xl border border-ges-green/20">
              <h4 class="font-bold text-ges-green border-b border-ges-green/20 pb-2 mb-4"><i class="pi pi-users mr-2"></i>Acompañantes</h4>
              
              <div v-for="(pasajero, index) in reserveData.pasajeros_adicionales" :key="index" class="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
                <span class="md:col-span-2 text-sm font-semibold text-gray-500">{{ t('quotePage.reserveForm.extraPassenger').replace('{num}', index + 1) }}</span>
                <div>
                  <input v-model="pasajero.nombre" type="text" :placeholder="t('quotePage.reserveForm.name')" required class="w-full px-4 py-2 text-sm rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
                </div>
                <div>
                  <input v-model="pasajero.cedula" type="text" :placeholder="t('quotePage.reserveForm.idNumber')" required class="w-full px-4 py-2 text-sm rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 border-t pt-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.date') }} *</label>
              <input v-model="reserveData.fecha" type="date" :min="today" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">{{ t('quotePage.reserveForm.time') }} *</label>
              <input v-model="reserveData.hora" @change="validateTime" @input="validateTime" type="time" :min="minReserveTime" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-ges-green outline-none" />
              
              <p v-if="reserveData.fecha === today" class="text-xs text-amber-600 mt-2 font-semibold flex items-start gap-1">
                <i class="pi pi-exclamation-triangle mt-0.5"></i>
                {{ t('quotePage.reserveForm.timeWarning', { hours: currentOffsetHours }) }}
              </p>
            </div>
          </div>
          
          <div class="mt-8">
            <button type="submit" class="w-full bg-ges-green hover:bg-ges-light text-white font-bold py-4 px-8 rounded-full shadow-lg transition-all duration-300 flex items-center justify-center gap-2">
              <i class="pi pi-check-circle"></i> {{ t('quotePage.reserveForm.submitBtn') }}
            </button>
          </div>
        </form>
      </div>
     </div> 
          
          <!-- <div class="mt-6 flex justify-end">
            <button type="submit" class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow transition-all duration-300 flex items-center gap-2">
              <i class="pi pi-search"></i> {{ t('quotePage.reserveForm.searchBtn') }}
            </button>
          </div>
        </form> -->
<!-- 
        <div class="mt-8 text-center text-gray-500">
           <p><i class="pi pi-info-circle mr-1"></i> Seleccione sus criterios de viaje para ver los horarios disponibles.</p>
        </div>
      </div>

    </div>
  </div> -->
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Ocultar por completo las flechas nativas del input number */
.ocultar-flechas::-webkit-outer-spin-button,
.ocultar-flechas::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Soporte para Firefox */
.ocultar-flechas {
  -moz-appearance: textfield;
}

</style>