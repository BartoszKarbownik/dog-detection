<template>
  <div>
    <Navbar />
  </div>
  <div class="pt-24 pb-5">
    <div class="flex justify-center mb-10">
      <button 
        @click="startDetection" 
        :disabled="cameraStore.status !== 'idle'" 
        class="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed">
        Start Detection
      </button>
      <button 
        @click="stopDetection" 
        :disabled="cameraStore.status === 'idle'" 
        class="ml-4 px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed">
        Stop Detection
      </button>
    </div>

    <div class="flex justify-center mb-4">
      <span class="px-4 py-2 text-lg font-semibold rounded-lg" 
            :class="statusClass">
        Status: {{ statusText }}
      </span>
    </div>

    <p v-if="cameraStore.error" class="text-center text-red-600 font-bold">
      Error: {{ cameraStore.error }}
    </p>

    <!-- Cleaned-up Notifications Section -->
    <div class="max-w-2xl mx-auto mt-8 p-4 bg-white rounded-lg shadow">
      <h2 class="text-2xl font-bold mb-4 text-gray-800">Recent Notifications</h2>
      <ul class="space-y-2">
        <li v-for="notification in cameraStore.notifications" :key="notification.id" 
            class="p-2 bg-blue-50 rounded">
          {{ notification.message }}
        </li>
      </ul>
    </div>
  </div>
  <div>
    <Dashboard />
  </div>
</template>

<script setup>
import { useCameraStore } from '../stores/cameraStore';
import { computed, onMounted, onUnmounted } from 'vue';
import Navbar from '../components/Navbar.vue';
import Dashboard from '../components/Dashboard.vue';

const cameraStore = useCameraStore();

// Status computation for UI
const statusText = computed(() => {
  switch (cameraStore.status) {
    case 'idle': return 'Idle';
    case 'starting': return 'Starting...';
    case 'running': return 'Running';
    case 'error': return 'Error';
    default: return 'Unknown';
  }
});

const statusClass = computed(() => {
  switch (cameraStore.status) {
    case 'idle': return 'bg-gray-200 text-gray-800';
    case 'starting': return 'bg-yellow-100 text-yellow-800';
    case 'warming_up': return 'bg-yellow-100 text-yellow-800';
    case 'running': return 'bg-green-100 text-green-800';
    case 'error': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-200 text-gray-800';
  }
});

const startDetection = () => {
  cameraStore.startDetection();
};

const stopDetection = () => {
  cameraStore.stopDetection();
};

// Setup notification system
const setupNotifications = () => {
  const eventSource = new EventSource('http://localhost:5000/camera/notifications');
  eventSource.onmessage = (event) => {
    const notification = JSON.parse(event.data);
    showNotification(notification);
    cameraStore.addNotification(notification);
  };
  return eventSource;
};

// Request permission to show notifications if necessary
const requestNotificationPermission = () => {
  if (!("Notification" in window)) {
    console.log("This browser does not support desktop notification");
    return;
  }

  if (Notification.permission !== "granted" && Notification.permission !== "denied") {
    Notification.requestPermission().then((permission) => {
      if (permission !== "granted") {
        console.log("Permission for notifications was denied or not granted.");
      }
    });
  }
};

// Show browser notification
const showNotification = (notification) => {
  if (Notification.permission === "granted") {
    new Notification(notification.message);
  }
};

let statusCheckInterval;
let notificationEventSource;

onMounted(() => {
  statusCheckInterval = cameraStore.startStatusChecks();
  notificationEventSource = setupNotifications();

  // Request permission to show notifications when the app starts
  requestNotificationPermission();
});

onUnmounted(() => {
  if (statusCheckInterval) clearInterval(statusCheckInterval);
  if (notificationEventSource) notificationEventSource.close();
});
</script>