import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '../components/LoginForm.vue';
import HomeAlt from '../components/HomeAlt.vue';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Detections from '../views/Detections.vue';
import Camera from '../views/Camera.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login//LoginForm
  },
  {
    path: '/homealt',
    name: 'HomeAlt',
    component: HomeAlt
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/cameras',
    name: 'Camera',
    component: Camera 
  },
  {
    path: '/detections',
    name: 'Detections',
    component: Detections
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
