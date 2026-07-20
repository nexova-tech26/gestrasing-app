<script setup>
import { useI18n } from 'vue-i18n'
import { useHead } from '@vueuse/head'
import { computed, ref, onMounted } from 'vue'

const { t } = useI18n()

useHead({
  title: computed(() => t('seo.about.title')),
  meta: [
    { name: 'description', content: computed(() => t('seo.about.desc')) },
    { property: 'og:title', content: computed(() => t('seo.about.title')) },
    { property: 'og:description', content: computed(() => t('seo.about.desc')) },
    { property: 'og:type', content: 'website' }
  ]
})

//refrencia pa capturar las tarjetas del dom
const cardsRef = ref([])

const setCardRef = (el) => {
  if (el && !cardsRef.value.includes(el)) {
    cardsRef.value.push(el)
  }
}

onMounted(() => {
  //observador
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      //apenas la tarjeta aparece en la pantalla
      if (entry.isIntersecting) {
        //agrega la clase
        entry.target.classList.add('is-visible')
        // Dejamos de observarla para no desperdiciar memoria de procesador
        observer.unobserve(entry.target)
      }
    })
  }, {
    threshold: 0.25 // Se activa cuando al menos el 15% de la tarjeta ya se ve
  })

  // Le decimos al observador que vigile cada tarjeta que capturamos
  cardsRef.value.forEach((card) => {
    if (card) observer.observe(card)
  })
})

//clientes para el carrusel
const clients = [
  { name: 'Del Llano Alto Oleico', logo: 'oleico-logo.png' },
  { name: 'Delta Zero', logo: 'deltazero-logo.png' },
  { name: 'Lycans Rugby Club', logo: 'lycans-logo.png' },
  { name: 'Panamericana', logo: 'logo-panamericana.png' }
]

</script>

<template>
  <div class="bg-white">
    
    <!-- ================= HERO INSTITUCIONAL ================= -->
    <section class="relative bg-ges-black text-white py-20 md:py-32 flex items-center min-h-[400px]">
      <img src="/img/nosotros-hero.webp" alt="Equipo Gestrasing" fetchpriority="high" class="absolute inset-0 w-full h-full object-cover" />
      <div class="absolute inset-0 bg-ges-black/75"></div>
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center w-full">
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-4 drop-shadow-md">
          <!-- Reemplazamos los textos fijos -->
          {{ t('about.hero.titlePart1') }} <span class="text-ges-green">{{ t('about.hero.titlePart2') }}</span>
        </h1>
        <p class="mt-4 max-w-2xl mx-auto text-lg md:text-xl text-ges-gray drop-shadow-sm">
          {{ t('about.hero.subtitle') }}
        </p>
      </div>
    </section>

    <!-- ================= MISIÓN Y VISIÓN ================= -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12 lg:gap-24 items-center">
        
        <!-- Misión -->
        <div class="space-y-6">
          <h2 class="text-3xl font-bold text-ges-black">{{ t('about.mission.title') }}</h2>
          <p class="text-lg text-gray-600 leading-relaxed">
            {{ t('about.mission.text') }}
          </p>
        </div>

        <!-- Visión -->
        <div class="space-y-6 md:border-l-4 border-ges-green/30 md:pl-12">
          <h2 class="text-3xl font-bold text-ges-black">{{ t('about.vision.title') }}</h2>
          <p class="text-lg text-gray-600 leading-relaxed">
            {{ t('about.vision.text') }}
          </p>
        </div>

      </div>
    </section>

    <!-- ================= VALORES CORPORATIVOS ================= -->
    <section class="bg-gray-50 py-16 md:py-24 border-t border-b border-gray-200 overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-extrabold text-ges-black">{{ t('about.values.title') }}</h2>
          <div class="h-1 w-20 bg-ges-green mx-auto mt-4 rounded"></div>
          <p class="mt-6 text-lg text-gray-600">{{ t('about.values.subtitle') }}</p>
        </div>
<!-- grid para mosrtrar tarjetas de valores -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Valor 1 -->
<!-- Valor 1 (Aparece de inmediato al hacer scroll) -->
            <div 
              :ref="setCardRef"
              class="reveal-card bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-all duration-700 ease-out opacity-0 translate-y-8 hover:-translate-y-1 text-center border-b-4 border-transparent hover:border-ges-green group"
            >
            <div class="w-16 h-16 mx-auto bg-[#4A9B3F]/10 text-ges-green rounded-full flex items-center justify-center mb-6 transition-transform duration-300 group-hover:scale-110">
              <i class="pi pi-shield text-2xl font-bold"></i>
            </div>
            <h3 class="text-xl font-bold text-ges-black mb-3">{{ t('about.values.card1.title') }}</h3>
            <p class="text-gray-600">{{ t('about.values.card1.text') }}</p>
          </div>

          <!-- Valor 2 (Aparece con 150ms de retraso) -->
            <div 
              :ref="setCardRef"
              class="reveal-card bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-all duration-700 ease-out opacity-0 translate-y-8 hover:-translate-y-1 text-center border-b-4 border-transparent hover:border-ges-green group"
            >
            <div class="w-16 h-16 mx-auto bg-[#4A9B3F]/10 text-ges-green rounded-full flex items-center justify-center mb-6 transition-transform duration-300 group-hover:scale-110">
              <i class="pi pi-clock text-2xl font-bold"></i>
            </div>
            <h3 class="text-xl font-bold text-ges-black mb-3">{{ t('about.values.card2.title') }}</h3>
            <p class="text-gray-600">{{ t('about.values.card2.text') }}</p>
          </div>

          <!-- Valor 3 (Aparece con 300ms de retraso) -->
            <div 
              :ref="setCardRef"
              class="reveal-card bg-white p-8 rounded-2xl shadow-sm hover:shadow-md transition-all duration-700 ease-out opacity-0 translate-y-8 hover:-translate-y-1 text-center border-b-4 border-transparent hover:border-ges-green group"
            >
            <div class="w-16 h-16 mx-auto bg-[#4A9B3F]/10 text-ges-green rounded-full flex items-center justify-center mb-6 transition-transform duration-300 group-hover:scale-110">
              <i class="pi pi-star text-2xl font-bold"></i>
            </div>
            <h3 class="text-xl font-bold text-ges-black mb-3">{{ t('about.values.card3.title') }}</h3>
            <p class="text-gray-600">{{ t('about.values.card3.text') }}</p>
          </div>

        </div>
        </div>
    </section>

    <!-- ================= RESPALDO Y CERTIFICACIONES ================= -->
<section class="py-16 md:py-20 bg-white overflow-hidden border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        
        <h4 class="text-2xl font-bold text-gray-400 uppercase tracking-widest mb-12">
          {{ t('about.clients.title') }}
        </h4>
        
        <div class="marquee-container relative w-full overflow-hidden flex select-none">
          
          <div class="marquee-track flex items-center gap-16 md:gap-24 hover:pause-animation">
            
            <div 
              v-for="(client, index) in clients" 
              :key="'orig-' + index" 
              class="flex flex-col items-center justify-center min-w-[140px] md:min-w-[160px] group cursor-pointer"
            >
              <img 
                :src="`/img/${client.logo}`" 
                :alt="client.name" 
                loading="lazy" 
                class="w-14 h-14 md:w-16 md:h-16 object-contain grayscale opacity-50 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:scale-110 mb-3" 
              />
              <span class="font-semibold text-xs md:text-sm text-gray-500 group-hover:text-ges-green transition-colors text-center line-clamp-1">
                {{ client.name }}
              </span>
            </div>

            <div 
              v-for="(client, index) in clients" 
              :key="'clone-' + index" 
              class="flex flex-col items-center justify-center min-w-[140px] md:min-w-[160px] group cursor-pointer"
              aria-hidden="true"
            >
              <img 
                :src="`/img/${client.logo}`" 
                :alt="client.name" 
                loading="lazy" 
                class="w-14 h-14 md:w-16 md:h-16 object-contain grayscale opacity-50 group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:scale-110 mb-3" 
              />
              <span class="font-semibold text-xs md:text-sm text-gray-500 group-hover:text-ges-green transition-colors text-center line-clamp-1">
                {{ client.name }}
              </span>
            </div>

          </div>
        </div>

      </div>
    </section>

  </div>
</template>

<style scoped>
/* Transición activada por el observador de scroll */
.reveal-card.is-visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
}

/* animacion del carrusel de clientes */
.marquee-container {
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 15%,
    black 85%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 15%,
    black 85%,
    transparent 100%
  );
}

.marquee-track {
  display: flex;
  width: max-content;
  /* más logos, aumenta el tiempo */
  animation: scrollMarquee 20s linear infinite;
}

/* Detener el movimiento si el usuario pone el cursor sobre un logo para leerlo */
.marquee-track:hover {
  animation-play-state: paused;
}

@keyframes scrollMarquee {
  0% {
    transform: translateX(0%);
  }
  100% {
    /* Se traslada exactamente la mitad del ancho del contenedor duplicado */
    transform: translateX(-50%);
  }
}
</style>