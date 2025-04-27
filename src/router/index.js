import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'
import VerticalDisplay from '../views/VerticalDisplay.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: App
    },
    {
      path: '/vertical_display',
      name: 'vertical_display',
      component: VerticalDisplay
    }
  ]
})

export default router 