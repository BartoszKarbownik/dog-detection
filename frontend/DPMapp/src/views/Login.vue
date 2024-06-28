<template>
    <div class="login-container">
      <LoginForm 
        v-if="!isRegisterMode" 
        @register="handleRegisterMode" 
      />
      <RegisterForm 
        v-else 
        @registered="handleRegistered" 
        @login="handleLoginMode"
      />
    </div>
  </template>
  
  <script>
  import LoginForm from '../components/LoginForm.vue'
  import RegisterForm from '../components/RegisterForm.vue';
  export default {
    name: 'Login',
    components: {
      LoginForm,
      RegisterForm
    },
    data() {
      return {
        isRegisterMode: false,
      };
    },
    methods: {
      handleRegisterMode() {
        this.isRegisterMode = true;
      },
      handleLoginMode() {
        this.isRegisterMode = false;
      },
      handleRegistered() {
        this.isRegisterMode = false;
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  