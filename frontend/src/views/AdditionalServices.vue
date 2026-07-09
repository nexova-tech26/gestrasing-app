<script setup>
import { useI18n } from 'vue-i18n'
import { useHead } from '@vueuse/head'
import { computed } from 'vue'

// Inicializacion del composable de internacionalizacion
const { t } = useI18n()

useHead({
  title: computed(() => t('seo.additional.title')),
  meta: [
    { name: 'description', content: computed(() => t('seo.additional.desc')) },
    { property: 'og:title', content: computed(() => t('seo.additional.title')) },
    { property: 'og:description', content: computed(() => t('seo.additional.desc')) },
    { property: 'og:type', content: 'website' }
  ]
})
</script>

<template>
  <div class="bg-white min-h-screen">
    
    <!-- ==================== HERO SECTION ==================== -->
    <section class="relative bg-ges-black text-white py-20 md:py-32 flex items-center min-h-[400px]">
      <img src="../assets/images/aditional-services-banner.webp" alt="Servicios Adicionales Gestrasing" fetchpriority="high" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-ges-black/75"></div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center w-full">
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 drop-shadow-md">
          {{ t('additionalPage.hero.title') }}
        </h1>
        <div class="h-1 w-24 bg-ges-green mx-auto mb-6 rounded"></div>
        <p class="mt-4 max-w-2xl mx-auto text-lg md:text-xl text-ges-gray drop-shadow-sm">
          {{ t('additionalPage.hero.subtitle') }}
        </p>
      </div>
    </section>

    <!-- ==================== SECCIÓN 1: MASCOTAS ==================== -->
    <!-- Patrón: Imagen Izquierda / Fondo Blanco -->
    <section class="py-16 md:py-24 border-b border-gray-100 bg-white" >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row gap-12 items-center">
          
          <div class="w-full lg:w-1/2 h-80 md:h-[450px] rounded-2xl overflow-hidden shadow-lg border border-gray-100"  id="adicional-mascotas">
             <img src="../assets/images/mascota-transporte.jpg" alt="Transporte de Mascotas" loading="lazy" class="w-full h-full object-cover hover:scale-105 transition-transform duration-700" />
          </div>

          <div class="w-full lg:w-1/2">
            <div class="inline-flex items-center justify-center p-3 bg-ges-gray/20 rounded-lg text-ges-green mb-4">
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2a3 3 0 013 3 3 3 0 01-3 3 3 3 0 01-3-3 3 3 0 013-3m-4 6a3 3 0 013 3 3 3 0 01-3 3 3 3 0 01-3-3 3 3 0 013-3m8 0a3 3 0 013 3 3 3 0 01-3 3 3 3 0 01-3-3 3 3 0 013-3m-4 14c-2.33 0-4.31-1.46-5.11-3.5L4.45 13c-.26-.71.1-1.49.81-1.75.7-.26 1.48.1 1.74.81l1.52 4.14C9.17 17.5 10.5 18 12 18s2.83-.5 3.48-1.8l1.52-4.14c.26-.71 1.04-1.07 1.74-.81.71.26 1.07 1.04.81 1.75l-2.44 6.5c-.8 2.04-2.78 3.5-5.11 3.5z"/></svg>
            </div>
            <h2 class="text-3xl font-bold text-ges-black mb-6">{{ t('additionalPage.pets.title') }}</h2>
            <p class="text-gray-600 leading-relaxed mb-8 text-lg">{{ t('additionalPage.pets.desc') }}</p>
            
            <h3 class="text-xl font-bold text-ges-black mb-4">{{ t('additionalPage.pets.featuresTitle') }}</h3>
            <ul class="space-y-3 mb-8">
              <li class="flex items-start text-gray-700" v-for="index in 3" :key="`pet-feat-${index}`">
                <svg class="w-6 h-6 text-ges-green mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>{{ t(`additionalPage.pets.features[${index - 1}]`) }}</span>
              </li>
            </ul>
              <a 
                href="https://wa.me/573223985161?text=Quisiera%20informaci%C3%B3n%20sobre%20el%20servicio%20de%20transporte%20de%20mascotas"
                target="_blank"
                rel="noopener noreferrer"
                class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow transition-all duration-300 inline-block text-center"
              >
                {{ t('additionalPage.pets.cta') }}
              </a>
          </div>

        </div>
      </div>
    </section>

    <!-- ==================== SECCIÓN 2: ENCOMIENDAS ==================== -->
    <!-- Patrón: Texto Izquierda / Imagen Derecha / Fondo Gris -->
    <section class="py-16 md:py-24 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col-reverse lg:flex-row gap-12 items-center">
          
          <div class="w-full lg:w-1/2" >
            <div class="inline-flex items-center justify-center p-3 bg-white shadow-sm rounded-lg text-ges-black mb-4">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
            </div>
            <h4 class="text-3xl font-bold text-ges-black mb-6">{{ t('additionalPage.parcels.title') }}</h4>
            <p class="text-gray-600 leading-relaxed mb-8 text-lg">{{ t('additionalPage.parcels.desc') }}</p>
            
            <h3 class="text-xl font-bold text-ges-black mb-4">{{ t('additionalPage.parcels.featuresTitle') }}</h3>
            <ul class="space-y-3 mb-8">
              <li class="flex items-start text-gray-700" v-for="index in 3" :key="`parcel-feat-${index}`">
                <svg class="w-6 h-6 text-ges-green mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>{{ t(`additionalPage.parcels.features[${index - 1}]`) }}</span>
              </li>
            </ul>
              <a 
                href="https://wa.me/573223985161?text=Quisiera%20informaci%C3%B3n%20sobre%20el%20servicio%20de%20encomiendas"
                target="_blank"
                rel="noopener noreferrer"
                class="bg-ges-green hover:bg-ges-light text-white font-bold py-3 px-8 rounded-full shadow transition-all duration-300 inline-block text-center"
              >
                {{ t('additionalPage.parcels.cta') }}
              </a>
          </div>

          <div class="w-full lg:w-1/2 h-80 md:h-[450px] rounded-2xl overflow-hidden shadow-lg" id="adicional-encomiendas">
             <img src="../assets/images/servicio-encomiendas.webp" alt="Envíos y Encomiendas" class="w-full h-full object-cover hover:scale-105 transition-transform duration-700" />
          </div>

        </div>
      </div>
    </section>

    <!-- ==================== SECCIÓN 3: TOURS ==================== -->
    <!-- Patrón: Imagen Izquierda / Fondo Blanco -->
    <section class="py-16 md:py-24 bg-white relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col lg:flex-row gap-12 items-center">
          
          <div class="relative w-full lg:w-1/2 h-80 md:h-[450px] rounded-2xl overflow-hidden shadow-lg border border-gray-100 group cursor-not-allowed">
             <img src="../assets/images/duster.webp" alt="Tours por el Llano" class="w-full h-full object-cover blur-[3px] opacity-80" />
             
             <div class="absolute inset-0 bg-ges-black/40 flex items-center justify-center">
                <span class="bg-amber-500 text-white font-extrabold text-2xl px-8 py-3 rounded-xl shadow-2xl transform -rotate-12 border-4 border-white tracking-widest uppercase">
                  {{ t('additionalPage.tours.badge') }}
                </span>
             </div>
          </div>

          <div class="w-full lg:w-1/2">
            <span class="inline-block px-4 py-1.5 bg-amber-100 text-amber-700 font-bold text-xs rounded-full uppercase tracking-wider mb-4 border border-amber-200">
              {{ t('additionalPage.tours.badge') }}
            </span>
            
            <h4 class="text-3xl font-bold text-ges-black mb-6">{{ t('additionalPage.tours.title') }}</h4>
            <p class="text-gray-600 leading-relaxed mb-8 text-lg">{{ t('additionalPage.tours.desc') }}</p>
            
            <h4 class="text-xl font-bold text-ges-black mb-4">{{ t('additionalPage.tours.featuresTitle') }}</h4>
            <ul class="space-y-3 mb-8">
              <li class="flex items-start text-gray-700" v-for="index in 4" :key="`tour-feat-${index}`">
                <svg class="w-6 h-6 text-amber-500 mr-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span>{{ t(`additionalPage.tours.features[${index - 1}]`) }}</span>
              </li>
            </ul>
            
            <button aria-label="servicio de tour" class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-3 px-8 rounded-full shadow-lg transition-all duration-300 flex items-center gap-2"
            >
            <a href="https://wa.me/573223985161?text=Quisiera%20informaci%C3%B3n%20sobre%20el%20servicio%20de%20tours"
                target="_blank">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
              {{ t('additionalPage.tours.cta') }}
            </a>

            </button>
          </div>

        </div>
      </div>
    </section>

  </div>
</template>