<template>
  <div>
    <Navbar />
    <button @click="handleStartDetection" :disabled="isDetecting">Start Detection</button>
    <button @click="handleStopDetection" :disabled="!isDetecting">Stop Detection</button>
    <p v-if="error" class="error">{{ error }}</p>
    <div v-if="isDetecting">
      <h3>Live Feed</h3>
      <img :src="videoFeedUrl" alt="Live detection feed" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useCameraStore } from '../stores/cameraStore';
import Navbar from '../components/Navbar.vue';

const store = useCameraStore();
const { isDetecting, error } = storeToRefs(store);
const videoFeedUrl = ref('http://localhost:5000/camera/video_feed');

const handleStartDetection = async () => {
  console.log('Start detection button clicked');
  try {
    await store.startDetection();
  } catch (error) {
    console.error('Error in component when starting detection:', error);
  }
};

const handleStopDetection = async () => {
  console.log('Stop detection button clicked');
  try {
    await store.stopDetection();
  } catch (error) {
    console.error('Error in component when stopping detection:', error);
  }
};
</script>

<style scoped>
.error {
  color: red;
}
</style>