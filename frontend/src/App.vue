<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n' // <-- Importamos el composable de i18n

// Extraemos 't' (la función para traducir) y 'locale' (la variable que guarda el idioma actual)
const { t, locale } = useI18n() 

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// Función que alterna el idioma activo
const toggleLanguage = () => {
  locale.value = locale.value === 'es' ? 'en' : 'es'
}
</script>

<template>
  <div class="min-h-screen bg-white flex flex-col font-sans">
    
    <!-- ==================== HEADER CORPORATIVO ==================== -->
    <header class="bg-ges-black text-white shadow-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          
          <!-- Logo de la Empresa -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="flex items-center transition-transform transform hover:scale-105 duration-300">
              <img src="/img/logo.png" alt="Logo Gestrasing S.A.S."  width="69" height="60" />
              <span class="text-ges-green">GES</span>TRASING <span class="text-ges-blue">S.A.S.</span>

            </router-link>
          </div>

          <!-- Menú de Escritorio y Selector de Idioma -->
          <nav class="hidden lg:flex space-x-6 items-center">
            <!-- Usamos t('nav.home') en lugar del texto fijo -->
            <router-link to="/" class="hover:text-ges-light transition-colors px-3 py-2 text-sm font-medium uppercase tracking-wide">{{ t('nav.home') }}</router-link>
            <router-link to="/nosotros" class="hover:text-ges-light transition-colors px-3 py-2 text-sm font-medium uppercase tracking-wide">{{ t('nav.about') }}</router-link>
            <router-link to="/servicios" class="hover:text-ges-light transition-colors px-3 py-2 text-sm font-medium uppercase tracking-wide">{{ t('nav.services') }}</router-link>
            <router-link to="/adicionales" class="hover:text-ges-light transition-colors px-3 py-2 text-sm font-medium uppercase tracking-wide">{{ t('nav.additional') }}</router-link>
            <router-link to="/cotizar" class="bg-ges-green hover:bg-ges-light text-white font-bold py-2.5 px-6 rounded-full shadow-md transition-all duration-300 transform hover:-translate-y-0.5 flex items-center gap-2"><i class="pi pi-calendar-plus"></i>Reservar Viaje</router-link>
            <!-- Botón Cambiar Idioma (Escritorio) -->
            <button @click="toggleLanguage" class="ml-4 flex items-center gap-2 border border-ges-green text-ges-green hover:bg-ges-green hover:text-white transition-colors px-3 py-1.5 rounded-full text-xs font-bold tracking-widest uppercase">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              {{ locale === 'es' ? 'EN' : 'ES' }}
            </button>
          </nav>

          <!-- Botón de Menú Hamburguesa (Celulares) -->
          <div class="lg:hidden flex items-center gap-4">
            <!-- Botón Cambiar Idioma (Móvil) -->
            <button @click="toggleLanguage" class="flex items-center justify-center w-8 h-8 rounded-full bg-ges-green text-white font-bold text-xs">
               {{ locale === 'es' ? 'EN' : 'ES' }}
            </button>

            <button @click="toggleMenu" class="text-ges-gray hover:text-white focus:outline-none">
              <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!isMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

        </div>
      </div>

      <!-- Menú Desplegable para Celulares -->
      <div v-show="isMenuOpen" class="lg:hidden bg-ges-black shadow-inner border-t border-gray-800">
        <nav class="px-4 pt-2 pb-4 space-y-2">
          <router-link @click="toggleMenu" to="/" class="block hover:bg-gray-800 hover:text-ges-light px-3 py-3 rounded-md text-base font-medium">{{ t('nav.home') }}</router-link>
          <router-link @click="toggleMenu" to="/nosotros" class="block hover:bg-gray-800 hover:text-ges-light px-3 py-3 rounded-md text-base font-medium">{{ t('nav.about') }}</router-link>
          <router-link @click="toggleMenu" to="/servicios" class="block hover:bg-gray-800 hover:text-ges-light px-3 py-3 rounded-md text-base font-medium">{{ t('nav.services') }}</router-link>
          <router-link @click="toggleMenu" to="/adicionales" class="block hover:bg-gray-800 hover:text-ges-light px-3 py-3 rounded-md text-base font-medium">{{ t('nav.additional') }}</router-link>
          <router-link @click="toggleMenu" to="/cotizar" class="block hover:bg-gray-800 hover:text-ges-light px-3 py-3 rounded-md text-base font-medium">Reservar Viaje</router-link>
        </nav>
      </div>
    </header>

    <!-- ==================== CONTENIDO PRINCIPAL ==================== -->
    <main class="flex-grow w-full">
      <router-view></router-view>
    </main>
    
    <!-- ==================== FOOTER CORPORATIVO ==================== -->
    <footer class="bg-ges-black text-ges-gray py-12 border-t-4 border-ges-green mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 text-center md:text-left">
          
          <div class="flex flex-col items-center md:items-start">
            <h3 class="text-2xl font-bold text-white mb-4"><span class="text-ges-green">GES</span>TRASING</h3>
            <p class="text-sm leading-relaxed max-w-xs">
              Calidad & Eficiencia en transporte especializado puerta a puerta y empresarial. Conectando destinos de manera segura.
            </p>
          </div>

          <div class="flex flex-col items-center md:items-start">
            <h4 class="text-white font-bold mb-4 uppercase tracking-wider text-sm">Menú Principal</h4>
            <nav class="flex flex-col space-y-2">
              <router-link to="/" class="hover:text-ges-green transition-colors text-sm flex items-center gap-2">
                <span class="text-ges-green text-xs">▸</span> {{ t('nav.home') }}
              </router-link>
              <router-link to="/nosotros" class="hover:text-ges-green transition-colors text-sm flex items-center gap-2">
                <span class="text-ges-green text-xs">▸</span> {{ t('nav.about') }}
              </router-link>
              <router-link to="/servicios" class="hover:text-ges-green transition-colors text-sm flex items-center gap-2">
                <span class="text-ges-green text-xs">▸</span> {{ t('nav.services') }}
              </router-link>
              <router-link to="/adicionales" class="hover:text-ges-green transition-colors text-sm flex items-center gap-2">
                <span class="text-ges-green text-xs">▸</span> {{ t('nav.additional') }}
              </router-link>
              <router-link to="/cotizar" class="hover:text-ges-green transition-colors text-sm flex items-center gap-2">
                <span class="text-ges-green text-xs">▸</span>Reserva tu viaje
              </router-link>
            </nav>
          </div>

          <div class="flex flex-col items-center md:items-start">
            <h4 class="text-white font-bold mb-4 uppercase tracking-wider text-sm">Contáctanos</h4>
            <ul class="space-y-3 text-sm">
              <li class="flex items-start gap-3 justify-center md:justify-start">
                <svg class="w-5 h-5 text-ges-green flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                <span>Sede Administrativa / <br>Villavicencio, Meta</span>
              </li>
              <li class="flex items-center gap-3 justify-center md:justify-start">
                <svg class="w-5 h-5 text-ges-green flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
                <span>+57 322 398 5161 / +57 320 388 6044</span>
              </li>
              <li class="flex items-center gap-3 justify-center md:justify-start">
                <svg class="w-5 h-5 text-ges-green flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                <span>gestrasingsas@gmail.com</span>
              </li>
            </ul>
          </div>

        </div>

        <div class="pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center gap-4 text-center md:text-left">
          <p class="text-sm">&copy; 2026 Gestrasing S.A.S. Todos los derechos reservados.</p>
          <p class="text-xs">Desarrollado por <span class="font-bold text-white hover:text-ges-green cursor-pointer transition-colors tracking-wide">Nexova Tech</span></p>
        </div>
      </div>
    </footer>

    <!-- ==================== BOTÓN FLOTANTE WHATSAPP ==================== -->
    <a href="https://wa.me/573223985161?text=Hola,%20vengo%20de%20la%20página%20web%20y%20deseo%20información." target="_blank" rel="noopener noreferrer" class="fixed bottom-6 right-6 z-50 bg-[#25D366] text-white rounded-full p-4 shadow-xl hover:bg-[#20b858] transition-transform transform hover:scale-110 flex items-center justify-center group" aria-label="Contactar por WhatsApp">
      <svg class="w-8 h-8 fill-current" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg>
    </a>

  </div>
</template>