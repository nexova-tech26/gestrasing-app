<script setup>
import { computed, ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '@vueuse/head'

const { t } = useI18n()

const servicios = [
  { id: 'intercity', img: 'duster.webp', link: '/servicios', hash: '#servicio-puertapuerta' },
  { id: 'corporate', img: 'camioneta-platon.webp', link: '/servicios', hash: '#servicio-corporativo' },
  { id: 'parcels', img: 'servicio-encomiendas.webp', link: '/adicionales', hash: '#adicional-encomiendas' },
  { id: 'pets', img: 'mascota-transporte.jpg', link: '/adicionales', hash: '#adicional-mascotas' }
]


// ================= INYECCIÓN DE SEO DINÁMICO =================
// Usamos "computed" para que el título cambie instantáneamente si el usuario cambia el idioma
useHead({
  title: computed(() => t('seo.home.title')),
  meta: [
    { name: 'description', content: computed(() => t('seo.home.desc')) },
    
    // Open Graph (Para previsualizaciones en WhatsApp, Facebook, LinkedIn)
    { property: 'og:title', content: computed(() => t('seo.home.title')) },
    { property: 'og:description', content: computed(() => t('seo.home.desc')) },
    { property: 'og:type', content: 'website' },
    // Aquí le decimos qué imagen mostrar al compartir el link (usaremos el logo o el hero)
    { property: 'og:image', content: '/logo-gestrasing.jpeg' } 
  ]
})

//---------------------animación de contador para exp-----------------
//Referencias para guardar el número actual de cada contador
const expCount = ref(0)
const fleetCount = ref(0)
const supportCount = ref(0)

//Referencia para conectar con el HTML y saber cuándo es visible
const statsSection = ref(null)
let hasAnimated = false // Control para que solo se anime una vez

//Función para animar números
const animateValue = (refVariable, target, duration) => {
  let startTimestamp = null
  
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp
    // Calculamos qué porcentaje de la animación llevamos
    const progress = Math.min((timestamp - startTimestamp) / duration, 1)
    
    // Actualizamos el número usando una curva matemática suavizada
    // Esto hace que arranque rápido y frene un poquito al final
    refVariable.value = Math.floor(progress * target)
    
    // Si no hemos llegado al 100%, pedimos el siguiente frame
    if (progress < 1) {
      window.requestAnimationFrame(step)
    }
  }
  
  window.requestAnimationFrame(step)
}

//Observamos cuándo la secciión entra en pantalla
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    // Si la sección entra en la pantalla y no se ha animado antes
    if (entries[0].isIntersecting && !hasAnimated) {
      hasAnimated = true
      // Parámetros: (variable reactiva, número meta, duración en milisegundos)
      animateValue(expCount, 10, 1000)      // Cuenta hasta 10 en 2 seg
      animateValue(fleetCount, 100, 1000)   // Cuenta hasta 100 en 2 seg
      animateValue(supportCount, 24, 1000)  // Cuenta hasta 24 en 2 seg
    }
  }, { 
    threshold: 0.5 // Se dispara cuando el 50% de la caja es visible
  })

  // Conectamos el observador con nuestra caja en el HTML
  if (statsSection.value) {
    observer.observe(statsSection.value)
  }
})
</script>

<template>
  <div>
    <!-- ================= HERO SECTION ================= -->
    <section class="relative bg-ges-black text-white min-h-[600px] flex items-center">
      <img src="../assets/images/hero_home.webp" alt="Flota de buses Gestrasing" class="absolute inset-0 w-full h-full object-cover" fetchpriority="high" />
      <div class="absolute inset-0 bg-ges-black/70"></div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 flex flex-col items-center text-center w-full">
        <h1 class="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 drop-shadow-md">
          {{ t('home.hero.titlePart1') }} <br class="hidden md:block" />
          <span class="text-ges-green">{{ t('home.hero.titlePart2') }}</span>
        </h1>
        <h2 class="mt-4 max-w-2xl text-lg md:text-xl text-ges-gray mb-10 drop-shadow-sm">
          {{ t('home.hero.subtitle') }}
        </h2>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <router-link to="/servicios" class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow-lg transition-all duration-300 transform hover:-translate-y-1">
            {{ t('home.hero.btnQuote') }}
          </router-link>
          <router-link to="/adicionales/#adicional-mascotas" class="bg-transparent border-2 border-white hover:bg-white hover:text-ges-black text-white font-bold py-3 px-8 rounded-full transition-colors duration-300">
            {{ t('home.hero.btnTours') }}
          </router-link>
        </div>
      </div>
    </section>

    <!-- ================= SECCIÓN DE CONFIANZA ================= -->
<!-- ================= SECCIÓN DE CONFIANZA ================= -->
    <section 
      ref="statsSection" 
      class="bg-white py-12 border-b border-gray-200 relative z-10 -mt-10 mx-4 md:mx-auto max-w-5xl rounded-xl shadow-xl"
    >
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-gray-100">
        
        <!-- Años de Experiencia -->
        <div class="p-4">
          <h2 class="text-4xl font-extrabold text-ges-green mb-2">+{{ expCount }}</h2>
          <p class="text-ges-black font-medium uppercase tracking-wide text-sm">{{ t('home.trust.exp') }}</p>
        </div>
        
        <!-- Flota -->
        <div class="p-4">
          <h2 class="text-4xl font-extrabold text-ges-green mb-2">{{ fleetCount }}%</h2>
          <p class="text-ges-black font-medium uppercase tracking-wide text-sm">{{ t('home.trust.fleet') }}</p>
        </div>
        
        <!-- Soporte -->
        <div class="p-4">
          <h2 class="text-4xl font-extrabold text-ges-green mb-2">{{ supportCount }}/7</h2>
          <p class="text-ges-black font-medium uppercase tracking-wide text-sm">{{ t('home.trust.support') }}</p>
        </div>
        
      </div>
    </section>

    <!-- ================= SECCIÓN DE SERVICIOS DESTACADOS ================= -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-16">
          <h3 class="text-3xl font-extrabold text-ges-black sm:text-4xl">{{ t('home.services.title') }}</h3>
          <div class="h-1 w-20 bg-ges-green mx-auto mt-4 rounded"></div>
          <p class="mt-6 text-lg text-gray-600">{{ t('home.services.subtitle') }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          
          <!-- Iteramos sobre el arreglo 'servicios' creado en el script setup -->
          <div v-for="servicio in servicios" :key="servicio.id" class="bg-white rounded-2xl shadow-md overflow-hidden hover:shadow-2xl transition-all duration-300 group flex flex-col">
            
            <div class="h-48 overflow-hidden bg-ges-gray">
              <img :src="`/img/${servicio.img}`" :alt="t(`home.services.cards.${servicio.id}.title`)" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
            </div>
            <div class="p-6 flex-grow flex flex-col justify-between">
              <div>
                <!-- Usamos templates literales (`) para inyectar dinámicamente el ID del servicio en la ruta del JSON -->
                <h3 class="text-xl font-bold text-ges-black mb-2 group-hover:text-ges-green transition-colors">{{ t(`home.services.cards.${servicio.id}.title`) }}</h3>
                <p class="text-gray-600 text-sm mb-4">{{ t(`home.services.cards.${servicio.id}.desc`) }}</p>
              </div>
              <router-link :to="{ path: servicio.link, hash: servicio.hash }"  class="text-ges-green font-bold hover:text-ges-light text-sm uppercase tracking-wide inline-flex items-center">
                {{ t('home.services.learnMore') }} <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </router-link>
            </div>
          </div>

        </div>
      </div>
    </section>
  </div>
</template>