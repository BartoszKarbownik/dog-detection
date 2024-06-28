import axios from 'axios';

const instance = axios.create({
   baseURL: 'http://localhost:5000/',
  //baseURL: 'https://2511-78-8-93-203.ngrok-free.app/',
});

const token = localStorage.getItem('authToken');
if (token) {
  instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
}

export default instance;
