<template>
    <div class="login-form-container">
      <form @submit.prevent="handleLogin">
        <p class="header">Log In</p>
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="loginForm.username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="loginForm.password" required>
        </div>
        <button type="submit" class="login-button">Log In</button>
        <p class = "register-button" @click="$emit('register')">Register</p>
      </form>
    </div>
  </template>
  
  <script>
  import { useAuthStore } from '../stores/authStore';

  export default {
    name: 'LoginForm',
    data() {
      return {
        loginForm: {
          username: '',
          password: ''
        }
      };
    },
    methods: {
      async handleLogin() {
        const authStore = useAuthStore();
        try 
        {
          console.log(this.loginForm)
          await authStore.login(this.loginForm);
          console.log('Zalogowano pomyślnie');
        } 
        catch (error) 
        {
          console.error('Logowanie nie powiodło się:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .login-form-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #242424;
    padding: 3vh;
    padding-top: 0;
    border-radius: 2vh;
    height: auto;
  }
  .header{
    font-size: 24px;
    margin-left: -3vh;
    margin-right: -3vh;
    margin-top: 0;
    margin-bottom: 3vh;
    padding: 1vh;
    border-top-left-radius: 2vh;
    border-top-right-radius: 2vh;
    text-align: center;
    font-weight: 600;
    background-color:#181818;
    border-bottom: 1px solid green;
  }
  .form-group {
    margin-bottom: 2vh;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .form-group:last-of-type{
    margin-bottom: 5vh;
  }

  .form-group label {
    display: block;
    float: left;
    margin-left: 1vw;
    box-sizing: border-box;
    margin-bottom: 5px;
  }
  .form-group input {
    width: 100%;
    height: 5vh;
    max-height: 50px;
    min-height: 40px;
    padding-left: 1vw;
    border-radius: 5vh;
    border-style: none;
    box-sizing: border-box;
  }

  .form-group input:focus{
    outline: 2px solid green;
  }
  
  .login-button {
    width: 100%;
    padding: 1vh;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5vh;
    height: 5vh;
    max-height: 50px;
    min-height: 40px;
    transition: transform 0.2s ease;
    background-color: green;
  }

  .register-button{
    margin-top: 2vh;
    margin-bottom: 0;
    margin-right: 1vw;
    font-size: 14px;
    float: right;
    transition: transform 0.2s ease
  }
  .register-button:hover, .login-button:hover{
    cursor: pointer;
    transform: scale(1.05);
  }

  .login-button:focus{
    outline: none;
  }
  @media (max-width: 700px) {
    .login-form-container{
      width: 70vw;
    }
  }
  </style>
  