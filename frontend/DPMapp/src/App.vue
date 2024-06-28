<script setup>
  import { useAuthStore } from './stores/authStore';
  import { RouterLink, RouterView } from 'vue-router'

  const authStore = useAuthStore();
  authStore.initializeStore();
</script>

<template>
  <div class="router-view">
    <RouterView />
  </div>
</template>

<style scoped>
.header{
  position: sticky;
}
/* .router-view {
  display: flex;
  justify-content: center;
  margin: 0;
} */

</style>