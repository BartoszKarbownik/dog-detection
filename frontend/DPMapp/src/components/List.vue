<template>
  <div class="max-w-lg mx-auto p-4">
    <h1 class="text-xl font-bold mb-4">Camera Detections</h1>
    <ul class="space-y-2">
      <li 
        v-for="(detection, index) in detections" 
        :key="index" 
        class="p-4 bg-gray-100 rounded-lg shadow-md flex justify-between items-center"
      >
        <span>{{ detection.label }}</span>
        <span class="text-gray-500 text-sm">{{ detection.time }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'DetectionList',
  props: {
    detections: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
</style>
