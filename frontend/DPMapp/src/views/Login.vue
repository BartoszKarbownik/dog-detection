<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-800">
    <LoginForm />
  </div>
</template>

<script>
import LoginForm from '../components/LoginForm.vue'

export default {
  name: 'Login',
  components: {
    LoginForm
  },
  data() {
    return {};
  },
  methods: {}
};
</script>

<style scoped>
</style>
