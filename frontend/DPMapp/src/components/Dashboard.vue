<template>
  <div class="bg-white py-24 sm:py-32">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <dl class="grid grid-cols-1 gap-x-8 gap-y-16 text-center lg:grid-cols-3">
        <div v-for="stat in stats" :key="stat.id" class="mx-auto flex max-w-xs flex-col gap-y-4">
          <dt class="text-base leading-7 text-gray-600">{{ stat.name }}</dt>
          <dd class="order-first text-3xl font-semibold tracking-tight text-gray-900 sm:text-5xl">{{ stat.value }}</dd>
        </div>
      </dl>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const stats = ref([
  { id: 1, name: 'Total stored detections', value: '0' },
  { id: 2, name: 'Current uptime', value: '00:00:00' },
  { id: 3, name: 'Detections today', value: '0' },
]);

let startTime = null;
let updateInterval;

const updateStats = async () => {
  try {
    const response = await axios.get('/camera/stats');
    const { total_detections, detections_today, status } = response.data;

    stats.value[0].value = (total_detections || 0).toString();
    stats.value[2].value = (detections_today || 0).toString();

    if (status === 'running' && !startTime) {
      startTime = Date.now();
    } else if (status !== 'running') {
      startTime = null;
      stats.value[1].value = '00:00:00';
    }

    if (startTime) {
      const uptime = Math.floor((Date.now() - startTime) / 1000);
      const hours = Math.floor(uptime / 3600);
      const minutes = Math.floor((uptime % 3600) / 60);
      const seconds = uptime % 60;
      stats.value[1].value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
  } catch (error) {
    console.error('Error fetching stats:', error);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
  }
};

onMounted(() => {
  updateStats();
  updateInterval = setInterval(updateStats, 1000);
});

onUnmounted(() => {
  if (updateInterval) {
    clearInterval(updateInterval);
  }
});
</script>