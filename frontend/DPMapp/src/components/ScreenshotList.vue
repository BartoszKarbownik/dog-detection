<template>
  <div class="max-w-7xl mx-auto p-4 flex">
    <div class="w-1/2 pr-4">
      <h1 class="text-xl font-bold mb-4">Screenshots</h1>
      <ul v-if="paginatedScreenshots.length" class="space-y-2">
        <li
          v-for="screenshot in paginatedScreenshots"
          :key="screenshot.id"
          @click="selectScreenshot(screenshot)"
          :class="[
            'p-4 rounded-lg shadow-md flex justify-between items-center cursor-pointer',
            selectedScreenshot && selectedScreenshot.id === screenshot.id
              ? 'bg-blue-100 border-2 border-blue-500'
              : 'bg-gray-100'
          ]"
        >
          <div class="flex items-center">
            <p>{{ screenshot.filename }}</p>
            <p class="text-gray-500 text-sm ml-4">Uploaded: {{ new Date(screenshot.uploaded).toLocaleString() }}</p>
          </div>
        </li>
      </ul>
      <p v-else class="text-gray-500">No screenshots available.</p>

      <!-- Pagination -->
      <div class="mt-4">
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <button
            @click="currentPage > 1 && currentPage--"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
          >
            <span class="sr-only">Previous</span>
            <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
          </button>
          <button
            v-for="page in totalPages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'relative inline-flex items-center px-4 py-2 text-sm font-semibold focus:z-20 focus:outline-offset-0',
              currentPage === page
                ? 'z-10 bg-indigo-600 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600'
                : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50'
            ]"
          >
            {{ page }}
          </button>
          <button
            @click="currentPage < totalPages && currentPage++"
            :disabled="currentPage === totalPages"
            class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
          >
            <span class="sr-only">Next</span>
            <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </nav>
      </div>
    </div>

    <div class="w-1/2 pl-4">
      <div v-if="selectedScreenshot" class="mt-8">
        <h2 class="text-lg font-semibold">Selected Screenshot:</h2>
        <img :src="`${apiUrl}/camera/screenshots/${selectedScreenshot.id}`" alt="Selected Screenshot" class="mt-4 w-full object-contain" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCameraStore } from '../stores/cameraStore';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

const cameraStore = useCameraStore();
const apiUrl = 'http://localhost:5000';

const screenshots = ref([]);
const selectedScreenshot = ref(null);
const currentPage = ref(1);
const itemsPerPage = 10;

const selectScreenshot = (screenshot) => {
  selectedScreenshot.value = screenshot;
};

onMounted(async () => {
  await cameraStore.refreshScreenshots();
  screenshots.value = cameraStore.screenshots;
  if (screenshots.value.length > 0) {
    selectScreenshot(screenshots.value[0]); // Select the most recent screenshot
  }
});

const totalPages = computed(() => Math.ceil(screenshots.value.length / itemsPerPage));

const paginatedScreenshots = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return screenshots.value.slice(start, end);
});
</script>