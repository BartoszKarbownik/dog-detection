<template>
    <div>
      <Navbar />
    </div>
    <div class="min-h-screen bg-gray-50 flex items-center justify-center">
      <ScreenshotList />
    </div>
  </template>
  
  <script setup>
  import Navbar from '../components/Navbar.vue';
  import ScreenshotList from '../components/ScreenshotList.vue';
  </script>
  