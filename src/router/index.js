import { createRouter, createWebHistory } from 'vue-router'
import VerticalDisplay from '../views/VerticalDisplay.vue'
import App from '../App.vue'
import VehicleView from '../views/VehicleView.vue'
import DroneView from '../views/DroneView.vue'
import DeliveryView from '../views/DeliveryView.vue'
import EnvironmentView from '../views/EnvironmentView.vue'
import DatabaseView from '@/views/DatabaseView.vue'

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
    },
    {
      path: '/vehicle',
      name: 'vehicle',
      component: VehicleView
    },
    {
      path: '/drone',
      name: 'drone',
      component: DroneView
    },
    {
      path: '/delivery',
      name: 'delivery',
      component: DeliveryView
    },
    {
      path: '/environment',
      name: 'environment',
      component: EnvironmentView
    },
    {
      path: '/database',
      name: 'Database',
      component: DatabaseView
    }
  ]
})

export default router 