<template>
  <div>
    <Navbar />
    <p>Status: {{ statusText }}</p>
    <p v-if="cameraStore.error" class="error">
      Error: {{ cameraStore.error }}
    </p>
    <button @click="startDetection" :disabled="cameraStore.status !== 'idle'">
      Start Detection
    </button>
    <button @click="stopDetection" :disabled="cameraStore.status === 'idle'">
      Stop Detection
    </button>
  </div>
</template>

<script setup>
import { useCameraStore } from '../stores/cameraStore';
import { computed, onMounted, onUnmounted } from 'vue';
import Navbar from '../components/Navbar.vue';

const cameraStore = useCameraStore();

const statusText = computed(() => {
  switch (cameraStore.status) {
    case 'idle': return 'Idle';
    case 'starting': return 'Starting...';
    case 'warming_up': return 'Warming up...';
    case 'running': return 'Running';
    case 'error': return 'Error';
    default: return 'Unknown';
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

button {
  margin: 0 10px;
  padding: 5px 10px;
  font-size: 16px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>