import { defineStore } from 'pinia';
import axios from '../axios';

export const useCameraStore = defineStore('camera', {
    state: () => ({
      isDetecting: false,
      error: null,
    }),
    actions: {
      async startDetection() {
        console.log('startDetection action called');
        try {
            console.log('Sending request to start detection');
          await axios.get('camera/start_detection')
          this.isDetecting = true
          this.error = null
        } catch (error) {
          this.error = 'Failed to start detection'
          console.error('Error starting detection:', error)
        }
      },
      async stopDetection() {
        try {
          await axios.get('camera/stop_detection')
          this.isDetecting = false
          this.error = null
        } catch (error) {
          this.error = 'Failed to stop detection'
          console.error('Error stopping detection:', error)
        }
      },
    },
  })