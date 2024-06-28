import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginForm
  },
  // You can add more routes here
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
