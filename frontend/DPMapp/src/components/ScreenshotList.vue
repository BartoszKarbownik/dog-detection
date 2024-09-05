<template>
  <div class="max-w-lg mx-auto p-4">
    <h1 class="text-xl font-bold mb-4">Screenshots</h1>
    <ul v-if="screenshots.length" class="space-y-2">
      <li
        v-for="screenshot in screenshots"
        :key="screenshot.id"
        @click="selectScreenshot(screenshot)"
        class="p-4 bg-gray-100 rounded-lg shadow-md flex justify-between items-center cursor-pointer"
      >
        <div class="flex items-center">
          <p>{{ screenshot.filename }}</p>
          <p class="text-gray-500 text-sm ml-4">Uploaded: {{ new Date(screenshot.uploaded).toLocaleString() }}</p>
        </div>
      </li>
    </ul>
    <p v-else class="text-gray-500">No screenshots available.</p>

    <div v-if="selectedScreenshot" class="mt-8">
      <h2 class="text-lg font-semibold">Selected Screenshot:</h2>
      <img :src="`${apiUrl}/camera/screenshots/${selectedScreenshot.id}`" alt="Selected Screenshot" class="mt-4 w-full object-contain" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCameraStore } from '../stores/cameraStore';

const cameraStore = useCameraStore();
const apiUrl = 'http://localhost:5000';

const screenshots = ref([]);
const selectedScreenshot = ref(null);

const selectScreenshot = (screenshot) => {
  selectedScreenshot.value = screenshot;
};

onMounted(async () => {
  await cameraStore.refreshScreenshots();
  screenshots.value = cameraStore.screenshots;
});
</script>
