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
          @click="toggleFullscreen"
        />
        <div 
          v-if="cameraStore.status === 'running'"
          class="absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold"
        >
          Detection Active
        </div>
      </div>
      
      <div class="flex space-x-4 mb-6">
        <button 
          @click="toggleDetection"
          :class="[
            'px-4 py-2 rounded-md font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2',
            cameraStore.status === 'running'
              ? 'bg-red-500 hover:bg-red-600 focus:ring-red-500 text-white' 
              : 'bg-green-500 hover:bg-green-600 focus:ring-green-500 text-white'
          ]"
        >
          {{ cameraStore.status === 'running' ? 'Stop Detection' : 'Start Detection' }}
        </button>
        <button 
          @click="captureScreenshot"
          class="px-4 py-2 bg-purple-500 text-white rounded-md font-semibold hover:bg-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
        >
          Capture Screenshot
        </button>
      </div>
      
      <div class="bg-gray-100 p-4 rounded-md">
        <h2 class="text-xl font-semibold mb-2 text-gray-800">Stream Information</h2>
        <p><strong>Status:</strong> {{ cameraStore.status }}</p>
        <p v-if="cameraStore.error"><strong>Error:</strong> {{ cameraStore.error }}</p>
        <p><strong>FPS:</strong> {{ fps }}</p>
      </div>
    </div>
    
    <!-- Modal for fullscreen view -->
    <div v-if="isFullscreen" class="fixed inset-0 bg-black z-50 flex items-center justify-center">
      <img :src="streamUrl" alt="Fullscreen Camera Feed" class="max-w-full max-h-full object-contain" />
      <button 
        @click="isFullscreen = false"
        class="absolute top-4 right-4 text-white bg-gray-800 rounded-full p-2 hover:bg-gray-700 focus:outline-none"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useCameraStore } from '../stores/cameraStore';
import Navbar from '../components/Navbar.vue';

const cameraStore = useCameraStore();
const isFullscreen = ref(false);
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

const captureScreenshot = async () => {
  // Implement screenshot capture logic here
  console.log('Screenshot captured');
};

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value;
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