<template>
    <div>
        <Navbar />
      <select v-model="selectedCamera" @change="startCamera">
        <option value="">Select Camera</option>
        <option v-for="camera in cameras" :key="camera.deviceId" :value="camera.deviceId">{{ camera.label || 'Camera ' + (cameras.indexOf(camera) + 1) }}</option>
      </select>
      <video ref="cameraFeed" autoplay></video>
          <h1>Live Camera Feed</h1>
    <img src="http://localhost:5000/camera/video_feed" alt="Video Stream" />
    </div>
  </template>

  <script setup>
  import Navbar from './Navbar.vue'
  import Button from './Button.vue';
  </script>
  
  <script>
  export default {
    data() {
      return {
        selectedCamera: '',
        cameras: []
      };
    },
    async mounted() {
      await this.getCameras();
    },
    methods: {
      async getCameras() {
        try {
          const devices = await navigator.mediaDevices.enumerateDevices();
          this.cameras = devices.filter(device => device.kind === 'videoinput');
        } catch (error) {
          console.error('Error enumerating devices:', error);
        }
      },
      async startCamera() {
        const deviceId = this.selectedCamera;
        if (!deviceId) return;
  
        const constraints = { video: { deviceId: { exact: deviceId } } };
  
        try {
          const stream = await navigator.mediaDevices.getUserMedia(constraints);
          const videoElement = this.$refs.cameraFeed;
          videoElement.srcObject = stream;
        } catch (error) {
          console.error('Error accessing camera:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  select {
    margin-bottom: 10px;
  }
  </style>
  