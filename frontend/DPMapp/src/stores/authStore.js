import { defineStore } from 'pinia';
import axios from '../axios';
import VueJwtDecode from 'vue-jwt-decode';


export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('authToken') || null,
    username: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    initializeStore() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.token = token;
        const decodedJWTtoken = VueJwtDecode.decode(token);
        this.username = decodedJWTtoken.unique_name;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      }
    },
    async register(credentials) {
      try {
        await axios.post('auth/register', credentials);
      } catch (error) {
        console.error('An error occurred during registration:', error);
        alert(error.response.data);
        throw error;
      }
    },
    async login(credentials) {
      try {
        console.table("Login data", credentials);
        console.table("token", this.token);
        const response = await axios.post('auth/login', credentials);
        this.token = response.data.token;
        localStorage.setItem('authToken', this.token);
        const decodedJWTtoken = VueJwtDecode.decode(this.token);
        this.username = decodedJWTtoken.unique_name;
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
      } catch (error) {
        console.error('An error occurred during login:', error);
        alert("Invalid login or password. Please try again.");
        throw error;
      }
    },
    logout() {
      this.$reset();
      this.token = null;
      this.username = null;
      localStorage.removeItem('authToken');
      delete axios.defaults.headers.common['Authorization'];

    },
  },
});
