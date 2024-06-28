import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://localhost:5000/',
});

const token = localStorage.getItem('authToken');
if (token) {
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default instance;