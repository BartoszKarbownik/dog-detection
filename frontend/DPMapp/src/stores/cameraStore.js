import { defineStore } from 'pinia';
import axios from '../axios';

export const useCameraStore = defineStore('camera', {
  state: () => ({
    isDetecting: false,
    screenshots: [],  
    error: null,
  }),
  actions: {
    async startDetection() {
      console.log('startDetection action called');
      try {
        console.log('Sending request to start detection');
        await axios.get('camera/start_detection');
        this.isDetecting = true;
        this.error = null;
      } catch (error) {
        this.error = 'Failed to start detection';
        console.error('Error starting detection:', error);
      }
    },
    async stopDetection() {
      try {
        await axios.get('camera/stop_detection');
        this.isDetecting = false;
        this.error = null;
      } catch (error) {
        this.error = 'Failed to stop detection';
        console.error('Error stopping detection:', error);
      }
    },
    async fetchScreenshots() {
      try {
        const response = await axios.get('camera/screenshots');
        this.screenshots = response.data;
        this.error = null;
      } catch (error) {
        this.error = 'Failed to fetch screenshots';
        console.error('Error fetching screenshots:', error);
      }
    },
    async refreshScreenshots(interval = 10000) {
      this.fetchScreenshots();
      setInterval(this.fetchScreenshots, interval);
    },
  },
});
