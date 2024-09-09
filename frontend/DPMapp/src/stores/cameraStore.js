import { defineStore } from 'pinia';
import axios from '../axios';

export const useCameraStore = defineStore('camera', {
  state: () => ({
    status: 'idle', 
    error: null,
    screenshots: [],
  }),
  actions: {
    async startDetection() {
      try {
        await axios.get('camera/start_detection');
        this.status = 'starting';
        this.error = null;
      } catch (error) {
        this.status = 'error';
        this.error = 'Failed to start detection';
        console.error('Error starting detection:', error);
      }
    },
    async stopDetection() {
      try {
        await axios.get('camera/stop_detection');
        this.status = 'idle';
        this.error = null;
      } catch (error) {
        this.status = 'error';
        this.error = 'Failed to stop detection';
        console.error('Error stopping detection:', error);
      }
    },
    async fetchScreenshots() {
      try {
        const response = await axios.get('camera/screenshots');
        this.screenshots = response.data;
      } catch (error) {
        this.error = 'Failed to fetch screenshots';
        console.error('Error fetching screenshots:', error);
      }
    },
    async refreshScreenshots(interval = 10000) {
      this.fetchScreenshots();
      setInterval(this.fetchScreenshots, interval);
    },
    async checkDetectionStatus() {
      try {
        const response = await axios.get('camera/detection_status');
        const { status, error_message } = response.data;
        
        this.status = status;
        this.error = error_message || null;
      } catch (error) {
        this.status = 'error';
        this.error = 'Failed to fetch detection status';
        console.error('Error fetching detection status:', error);
      }
    },
    startStatusChecks(interval = 1000) {
      this.checkDetectionStatus(); 
      return setInterval(this.checkDetectionStatus, interval); 
    },
  },
});