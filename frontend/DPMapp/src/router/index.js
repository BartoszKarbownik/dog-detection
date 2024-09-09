import { createRouter, createWebHistory } from 'vue-router';
import LoginFormx from '../components/LoginFormAlt1.vue';
import LoginForm from '../components/LoginForm.vue';
import HomeAlt from '../components/HomeAlt.vue';
import Home from '../views/Home.vue';
import RegisterForm from '../components/RegisterForm.vue';
import Cameras from '../components/Cameras.vue';
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
    name: 'Camera',//s
    component: Camera //s
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterForm
  },
  {
    path: '/detections',
    name: 'Detections',
    component: Detections
  },
  {
    path: '/calendar',
    name: 'Cameras',
    component: Cameras
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
