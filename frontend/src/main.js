import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import { createHead } from '@vueuse/head' 
import App from './App.vue'
import router from './router'
import './assets/main.css'
import 'primeicons/primeicons.css'

import es from './locales/es.json'
import en from './locales/en.json'

const i18n = createI18n({
  legacy: false,
  locale: 'es',
  fallbackLocale: 'en',
  messages: {
    es,
    en
  }
})

// ESTA ES LA LÍNEA QUE FALTABA
const head = createHead() 

const app = createApp(App)

app.use(router)
app.use(i18n)
app.use(head) // Aquí se usa la variable que creamos arriba

app.mount('#app')