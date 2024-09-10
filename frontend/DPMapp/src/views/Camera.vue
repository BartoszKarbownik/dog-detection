<template>
  <div>
    <Navbar />
  </div>
  <div class="max-w-7xl mx-auto p-6 bg-gray-100 min-h-screen">
    <h1 class="text-3xl font-bold mb-6 text-gray-800">Camera Feed</h1>
    
    <div class="bg-white rounded-lg shadow-lg p-6">
      <div class="relative aspect-video bg-black rounded-lg overflow-hidden mb-6">
        <img 
          :src="streamUrl" 
          alt="Camera Feed"
          class="absolute inset-0 w-full h-full object-cover"
        />
        <div 
          v-if="cameraStore.status === 'running'"
          class="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold"
        >
          Detection Active
        </div>
        <div 
          class="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-semibold"
        >
          FPS: {{ fps }}
        </div>
      </div>
      
      <div class="flex justify-center">
        <button 
          @click="toggleDetection"
          :class="[
            'px-6 py-3 rounded-md font-semibold text-lg focus:outline-none focus:ring-2 focus:ring-offset-2',
            cameraStore.status === 'running'
              ? 'bg-red-500 hover:bg-red-600 focus:ring-red-500 text-white' 
              : 'bg-green-500 hover:bg-green-600 focus:ring-green-500 text-white'
          ]"
        >
          {{ cameraStore.status === 'running' ? 'Stop Detection' : 'Start Detection' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCameraStore } from '../stores/cameraStore';
import Navbar from '../components/Navbar.vue';

const cameraStore = useCameraStore();
const fps = ref(0);

const streamUrl = computed(() => {
  return cameraStore.status === 'running'
    ? 'http://localhost:5000/camera/video_feed'
    : 'http://localhost:5000/camera/plain_video_feed';
});

const toggleDetection = async () => {
  if (cameraStore.status === 'running') {
    await cameraStore.stopDetection();
  } else {
    await cameraStore.startDetection();
  }
};

const updateFps = async () => {
  try {
    const response = await fetch('http://localhost:5000/camera/fps');
    const data = await response.json();
    fps.value = data.fps || 0;
  } catch (error) {
    console.error('Error fetching FPS:', error);
  }
};

let statusInterval;
let fpsInterval;

onMounted(() => {
  statusInterval = cameraStore.startStatusChecks(1000);
  fpsInterval = setInterval(updateFps, 1000);
});

onUnmounted(() => {
  clearInterval(statusInterval);
  clearInterval(fpsInterval);
});
</script>