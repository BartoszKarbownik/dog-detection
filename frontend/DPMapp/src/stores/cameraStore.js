import { defineStore } from 'pinia';
import axios from '../axios';

export const useCameraStore = defineStore('camera', {
  state: () => ({
    status: 'idle', 
    error: null,
    screenshots: [],
    stats: [
      { id: 1, name: 'Total stored detections', value: '0' },
      { id: 2, name: 'Current uptime', value: '00:00:00' },
      { id: 3, name: 'Detections today', value: '0' },
    ],
    startTime: null,
    notifications: [],
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
    async updateStats() {
      try {
        const response = await axios.get('/camera/stats');
        const { total_detections, detections_today, status } = response.data;

        this.stats[0].value = (total_detections).toString();
        this.stats[2].value = (detections_today).toString();

        if (status === 'running' && !this.startTime) {
          this.startTime = Date.now();
        } else if (status !== 'running') {
          this.startTime = null;
          this.stats[1].value = '00:00:00';
        }

        if (this.startTime) {
          const uptime = Math.floor((Date.now() - this.startTime) / 1000);
          const hours = Math.floor(uptime / 3600);
          const minutes = Math.floor((uptime % 3600) / 60);
          const seconds = uptime % 60;
          this.stats[1].value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    },
    startStatsUpdate(interval = 1000) {
      this.updateStats();
      return setInterval(this.updateStats, interval);
    },
    addNotification(notification) {
      this.notifications.unshift(notification)
      if (this.notifications.length > 10) {
        this.notifications.pop()
      }
    },
    clearNotifications() {
      this.notifications = []
    }
  }
  },
);