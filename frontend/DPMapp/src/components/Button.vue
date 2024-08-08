<template>
    <button @click="handleClick" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
      Start Detection
    </button>
  </template>
  
  <script>
  export default {
    methods: {
      handleClick() {
        console.log('Button clicked');
        "http://localhost:5000/camera/start_detection"
      }
    }
  }
  </script>
  
  <style scoped>
  
  </style>
  