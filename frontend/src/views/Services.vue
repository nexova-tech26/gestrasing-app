<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useHead } from '@vueuse/head'


const { t } = useI18n()

useHead({
  title: computed(() => t('seo.services.title')),
  meta: [
    { name: 'description', content: computed(() => t('seo.services.desc')) },
    { property: 'og:title', content: computed(() => t('seo.services.title')) },
    { property: 'og:description', content: computed(() => t('seo.services.desc')) },
    { property: 'og:type', content: 'website' }
  ]
})

// ================= ESTADO DE LAS PESTAÑAS =================
const activeTab = ref('intercity')
const setTab = (tabName) => {
  activeTab.value = tabName
}

// ================= ESTADO DEL SLIDER DE FLOTA =================
// Array con los IDs y nombres de imágenes para la flota
const fleet = [
  { id: 'bus', img: 'bus.webp' },
  { id: 'van', img: 'van.png' },
  { id: 'minivan', img: 'minivan.png' },
  { id: 'duster', img: 'duster.webp' },
  {id: 'platon', img: 'camioneta-platon.webp'}
]

const currentSlide = ref(0)

// Función para ir al siguiente vehículo (vuelve a 0 si llega al final)
const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % fleet.length
}

// Función para ir al vehículo anterior (vuelve al final si está en 0)
const prevSlide = () => {
  currentSlide.value = (currentSlide.value - 1 + fleet.length) % fleet.length
}

// Función para saltar a un vehículo específico desde los "puntitos"
const goToSlide = (index) => {
  currentSlide.value = index
}
</script>

<template>
  <div class="bg-white min-h-screen">
    
    <section class="relative bg-ges-black text-white py-20 md:py-32 flex items-center min-h-[400px]">
      <img src="/img/services-banner.jpg" alt="Servicios Gestrasing" fetchpriority="high" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-ges-black/75"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center w-full">
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 drop-shadow-md">
          {{ t('servicesPage.hero.title') }}
        </h1>
        <div class="h-1 w-24 bg-ges-green mx-auto mb-6 rounded"></div>
        <p class="mt-4 max-w-2xl mx-auto text-lg md:text-xl text-ges-gray drop-shadow-sm">
          {{ t('servicesPage.hero.subtitle') }}
        </p>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="flex flex-col sm:flex-row justify-center border-b border-gray-200 mb-10">
        <button aria-label="tab puerta a puerta" @click="setTab('intercity')" :class="['px-8 py-4 text-lg font-bold transition-colors border-b-4', activeTab === 'intercity' ? 'border-ges-green text-ges-green' : 'border-transparent text-gray-500 hover:text-ges-black'] " >
          {{ t('servicesPage.tabs.intercity') }}
        </button>
        <button aria-label="tab servicio corporativo" @click="setTab('corporate')" :class="['px-8 py-4 text-lg font-bold transition-colors border-b-4', activeTab === 'corporate' ? 'border-ges-green text-ges-green' : 'border-transparent text-gray-500 hover:text-ges-black']" id="servicio-corporativo">
          {{ t('servicesPage.tabs.corporate') }}
        </button>
      </div>

      <div class="bg-gray-50 rounded-2xl p-8 md:p-12 shadow-sm border border-gray-100 min-h-[500px]">
        
        <div v-if="activeTab === 'intercity'" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center animate-fade-in"  id="servicio-puertapuerta">
          <div>
            <h2 class="text-3xl font-bold text-ges-black mb-6">{{ t('servicesPage.intercity.heading') }}</h2>
            <p class="text-gray-600 leading-relaxed mb-8 text-lg">{{ t('servicesPage.intercity.description') }}</p>
            <h3 class="text-xl font-bold text-ges-black mb-4">{{ t('servicesPage.intercity.featuresTitle') }}</h3>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center text-gray-700" v-for="index in 5" :key="`int-${index}`">
                <svg class="w-6 h-6 text-ges-green mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ t(`servicesPage.intercity.features[${index - 1}]`) }}
              </li>
            </ul>
          <router-link
            :to="{ path: '/cotizar', query: { tab: 'reserve' } }"
            class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow transition-all duration-300 inline-block text-center" 
          >
            {{ t('servicesPage.intercity.cta') }}
          </router-link>
          </div>
          <div class="h-96 bg-gray-200 rounded-xl overflow-hidden shadow-inner">
             <img src="/img/duster2.webp" fetchpriority="high" alt="Servicio Intermunicipal" class="w-full h-full object-cover" />
          </div>
        </div>

        <div v-if="activeTab === 'corporate'" class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center animate-fade-in" >
          <div>
            <h2 class="text-3xl font-bold text-ges-black mb-6">{{ t('servicesPage.corporate.heading') }}</h2>
            <p class="text-gray-600 leading-relaxed mb-8 text-lg">{{ t('servicesPage.corporate.description') }}</p>
            <h3 class="text-xl font-bold text-ges-black mb-4">{{ t('servicesPage.corporate.featuresTitle') }}</h3>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center text-gray-700" v-for="index in 5" :key="`corp-${index}`">
                <svg class="w-6 h-6 text-ges-green mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                {{ t(`servicesPage.corporate.features[${index - 1}]`) }}
              </li>
            </ul>
          <router-link
            :to="{ path: '/cotizar', query: { tab: 'corporate' } }"
            class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow transition-all duration-300 inline-block text-center" 
          >
            {{ t('servicesPage.corporate.cta') }}
          </router-link>
          </div>
          <div class="h-96 bg-gray-200 rounded-xl overflow-hidden shadow-inner flex items-center justify-center">
             <img src="/img/camioneta-platon.webp" alt="Servicio Empresarial" fetchpriority="high" class="w-full h-full object-cover" />
          </div>
        </div>

      </div>
    </section>

    <section class="py-16 md:py-24 bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-extrabold text-ges-black mb-4">{{ t('servicesPage.fleet.title') }}</h2>
          <div class="h-1 w-24 bg-ges-green mx-auto mb-6 rounded"></div>
          <p class="mt-4 max-w-2xl mx-auto text-lg text-gray-600">
            {{ t('servicesPage.fleet.subtitle') }}
          </p>
        </div>

<div class="relative w-full h-[450px] md:h-[600px] rounded-[2.5rem] overflow-hidden shadow-2xl bg-gray-900 group">
          
          <div 
            class="flex h-full transition-transform duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]"
            :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
          >
            
            <div v-for="vehicle in fleet" :key="vehicle.id" class="min-w-full h-full relative">
              
              <img :src="`/src/assets/images/${vehicle.img}`" :alt="t(`servicesPage.fleet.vehicles.${vehicle.id}.name`)" loading="lazy" 
              class="absolute inset-0 w-full h-full object-contain
              object-top
              md:object-cover 
              opacity-90 p-4 md:p-0" />
              
              <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent"></div>
 
              <div class="absolute bottom-14 left-2 md:bottom-16 md:left-16 max-w-md p-6 md:p-8 rounded-[2rem] backdrop-blur-md bg-white/10 border border-white/20 text-white shadow-xl transform transition-transform duration-500 hover:-translate-y-2">
                <h3 class="text-2xl md:text-3xl font-extrabold mb-4">{{ t(`servicesPage.fleet.vehicles.${vehicle.id}.name`) }}</h3>
                
                <div class="flex flex-wrap gap-1">
                  <div class="flex items-center gap-2 bg-ges-green text-white px-4 py-2 rounded-full font-bold text-xs md:text-sm">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                    <span>{{ t(`servicesPage.fleet.vehicles.${vehicle.id}.seats`) }} {{ t('servicesPage.fleet.specs.seats') }}</span>
                  </div>
                  <div class="flex items-center gap-2 bg-white text-ges-black px-4 py-2 rounded-full font-bold text-xs md:text-sm">
                    <svg class="w-5 h-5 text-ges-green" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"></path></svg>
                    <span>{{ t(`servicesPage.fleet.vehicles.${vehicle.id}.type`) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button aria-label="Ver anterior vehículo" @click="prevSlide" class="absolute top-1/2 left-2 md:left-4 -translate-y-1/2 w-10 h-10 md:w-12 md:h-12 rounded-full bg-black/40 border border-white/20 hover:bg-ges-green text-white flex justify-center items-center transition-all opacity-100 shadow-lg z-10">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
          </button>
          
          <button aria-label="Ver siguiente vehículo" @click="nextSlide" class="absolute top-1/2 right-2 md:right-4 -translate-y-1/2 w-10 h-10 md:w-12 md:h-12 rounded-full bg-black/40 border border-white/20 hover:bg-ges-green text-white flex justify-center items-center transition-all opacity-100 shadow-lg z-10">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </button>

          <div class="absolute bottom-6 left-1/2 -translate-x-1/2 flex space-x-3">
            <button 
              v-for="(_, index) in fleet" 
              :key="'dot-'+index" 
              @click="goToSlide(index)"
              :class="['w-3 h-3 rounded-full transition-all duration-300', currentSlide === index ? 'bg-ges-green w-8' : 'bg-white/50 hover:bg-white']"
              aria-label="Ir a diapositiva"
            ></button>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
/* animación suave para cuando se cambian las pestañas de arriba */
.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>