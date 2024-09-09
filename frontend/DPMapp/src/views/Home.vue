<template>
  <div>
    <Navbar />
  </div>
  <div class="pt-24 pb-5">
    <div class="flex justify-center mb-10">
      <button 
        @click="startDetection" 
        :disabled="cameraStore.status !== 'idle'" 
        class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed">
        Start Detection
      </button>
      <button 
        @click="stopDetection" 
        :disabled="cameraStore.status === 'idle'" 
        class="ml-4 px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed">
        Stop Detection
      </button>
    </div>

    <div class="flex justify-center mb-4">
      <span class="px-4 py-2 text-lg font-semibold rounded-lg" 
            :class="statusClass">
        Status: {{ statusText }}
      </span>
    </div>

    <p v-if="cameraStore.error" class="text-center text-red-600 font-bold">
      Error: {{ cameraStore.error }}
    </p>
  </div>
  <div class="">
    <Dashboard />
  </div>
</template>

<script setup>
import { useCameraStore } from '../stores/cameraStore';
import { computed, onMounted, onUnmounted } from 'vue';
import Navbar from '../components/Navbar.vue';
import Dashboard from '../components/Dashboard.vue';
const cameraStore = useCameraStore();

const statusText = computed(() => {
  switch (cameraStore.status) {
    case 'idle': return 'Idle';
    case 'starting': return 'Starting...';
    case 'running': return 'Running';
    case 'error': return 'Error';
    default: return 'Unknown';
  }
});

const statusClass = computed(() => {
  switch (cameraStore.status) {
    case 'idle': return 'bg-gray-200 text-gray-800';
    case 'starting': return 'bg-yellow-100 text-yellow-800';
    case 'warming_up': return 'bg-yellow-100 text-yellow-800';
    case 'running': return 'bg-green-100 text-green-800';
    case 'error': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-200 text-gray-800';
  }
});

const startDetection = () => {
  cameraStore.startDetection();
};

const stopDetection = () => {
  cameraStore.stopDetection();
};

let statusCheckInterval;

onMounted(() => {
  statusCheckInterval = cameraStore.startStatusChecks();
});

onUnmounted(() => {
  if (statusCheckInterval) clearInterval(statusCheckInterval);
});
</script>

<style scoped>
.error {
  color: red;
  font-weight: bold;
}
</style>
