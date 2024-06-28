<template>
  <div class="register-form-container">
    <form @submit.prevent="handleRegister">
      <p class="header">Panel rejestracji</p>
      <div class="form-group">
        <label for="username">Nazwa użytkownika:</label>
        <input type="text" id="username" v-model="registerForm.user_Username" required>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="password">Hasło:</label>
          <input type="password" id="password" v-model="registerForm.user_Password" required>
        </div>
        <div class="form-group">
          <label for="confirmPassword">Potwierdź hasło:</label>
          <input type="password" id="confirmPassword" v-model="registerForm.confirmPassword" required>
        </div>
      </div>
      <button type="submit" class="register-button">Zarejestruj się</button>
      <p class="login-button" @click="$emit('login')">Powrót do logowania</p>
    </form>
  </div>
</template>

<script>
  import { useAuthStore } from '../stores/authStore';

  export default {
    name: 'RegisterForm',
    data() {
      return {
        registerForm: {
          user_Username: '',
          user_Password: ''
        },
      };
    },
    methods: {
      async handleRegister() {
        if (this.registerForm.user_Password !== this.registerForm.confirmPassword) 
        {
          alert('Hasła nie są takie same!');
          return;
        }
        const authStore = useAuthStore();
        try 
        {
          await authStore.register({
            user_Username: this.registerForm.user_Username,
            user_Password: this.registerForm.user_Password
          });
          alert("Rejestracja przebiegła pomyślnie. Powrót do logowania");
          this.$emit('login');
        } 
        catch (error) 
        {
          console.error('Rejestracja nie powiodła się:', error.response.data);
        }
      }
    }
  };
</script>


<style scoped>
.register-form-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #242424;
    padding: 3vh;
    padding-top: 0;
    border-radius: 2vh;
  }
  .header{
    font-size: 24px;
    margin-left: -3vh;
    margin-right: -3vh;
    margin-top: 0;
    margin-bottom: 3vh;
    padding: 1vh;
    width: -webkit-fill-available;
    border-top-left-radius: 2vh;
    border-top-right-radius: 2vh;
    text-align: center;
    font-weight: 600;
    background-color:#181818;
    border-bottom: 1px solid green;
  }
  .form-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .form-group label {
    box-sizing: border-box;
    margin-bottom: 5px;
    margin-left: 1vw;
  }
  
  .form-group input {
    height: 5vh;
    width: 100% auto;
    min-width: 10vw;
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
  
  .register-button {
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
  .form-row{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100%;
    gap:2vh;
    margin-bottom: 2vh;
  }
  .form-row:last-of-type{
    margin-bottom: 5vh;
  }
  .login-button{
    margin-top: 2vh;
    margin-bottom: 0;
    font-size: 14px;
    float: right;
    margin-right: 1vw;
    transition: transform 0.2s ease
  }
  .register-button:hover, .login-button:hover{
    cursor: pointer;
    transform: scale(1.05);
  }

  .register-button:focus{
    outline: none;
  }

  @media (max-width: 700px) {
    .register-form-container{
      width: 70vw;
    }
  }
</style>
