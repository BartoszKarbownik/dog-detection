<template>
    <div class="bg-white py-24 sm:py-32">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <dl class="grid grid-cols-1 gap-x-8 gap-y-16 text-center lg:grid-cols-3">
          <div v-for="stat in cameraStore.stats" :key="stat.id" class="mx-auto flex max-w-xs flex-col gap-y-4">
            <dt class="text-base leading-7 text-gray-600">{{ stat.name }}</dt>
            <dd class="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{{ stat.value }}</dd>
          </div>
        </dl>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, onUnmounted } from 'vue';
  import { useCameraStore } from '../stores/cameraStore';
  
  const cameraStore = useCameraStore();
  let updateInterval;
  
  onMounted(() => {
    cameraStore.updateStats();  
    updateInterval = cameraStore.startStatsUpdate(1000);  
  });
  
  onUnmounted(() => {
    if (updateInterval) {
      clearInterval(updateInterval);  
    }
  });
  </script>
  