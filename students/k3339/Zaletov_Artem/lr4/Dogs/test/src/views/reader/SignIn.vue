<template>
  <div class="sign-in-container">
    <h2 class="title">Sign In</h2>
    <form @submit.prevent="setLogin" ref="signInForm" class="sign-in-form">
      <input
        type="text"
        placeholder="Login"
        v-model="login"
        name="login"
        class="input-field"
      />
      <input
        type="password"
        placeholder="Password"
        v-model="password"
        name="password"
        class="input-field"
      />
      <button type="submit" class="sign-in-button">Sign In</button>
    </form>
    <p class="signup-link">
      <router-link to="/show/signup">I don't have an account</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AuthModals",
  data() {
    return {
      login: '',
      password: '',
    }
  },
  methods: {
    async setLogin() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/token/login", {
          username: this.login,
          password: this.password,
        });
        alert("Sign in succeeded");
        sessionStorage.setItem("auth_token", response.data.auth_token);
        sessionStorage.setItem("username", this.login);
        this.$router.push({ name: "home" });
      } catch (error) {
        if (error.response && error.response.status === 400) {
          alert("Login or password is incorrect");
        }
      }
    }
  }
}
</script>

<style scoped>
.sign-in-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.title {
  color: #283593;
  margin-bottom: 20px;
}

.sign-in-form {
  display: flex;
  flex-direction: column;
}

.input-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.sign-in-button {
  padding: 10px;
  background-color: #283593;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: 0.3s;
}

.sign-in-button:hover {
  background-color: #1a237e;
}

.signup-link {
  margin-top: 15px;
}

.signup-link a {
  text-decoration: none;
  color: #283593;
  font-weight: bold;
}
</style>
