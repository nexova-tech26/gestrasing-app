import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Services from '../views/Services.vue'
import AdditionalServices from '../views/AdditionalServices.vue'
import Cotizar from '../views/Quote.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/nosotros',
      name: 'about',
      component: About
    },
    {
      path: '/servicios',
      name: 'services',
      component: Services
    },
    {
      path: '/adicionales',
      name: 'additional-services',
      component: AdditionalServices
    },
    {
      path: '/cotizar', // <-- 2. Añadimos la ruta
      name: 'cotizar',
      component: Cotizar
    }
    // Nota: El /portal lo agregaremos cuando iniciemos la Épica del Backend Transaccional
  ],
    scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth', // Hace que el salto sea un deslizamiento elegante
        top: 80, // Opcional: Deja 80px de margen arriba por si tienes un menú fijo (navbar)
      }
    }
    // Si no hay hash, simplemente sube al inicio de la página
    return { top: 0 }
  }
  
})


export default router