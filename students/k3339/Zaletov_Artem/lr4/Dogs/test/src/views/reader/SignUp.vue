<template>
  <div class="sign-up-container">
    <h2 class="title">Sign Up</h2>
    <form @submit.prevent="signUp" ref="signUpForm" class="sign-up-form">
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
      <button type="submit" class="sign-up-button">Sign Up</button>
    </form>
    <p class="signin-link">
      <router-link to="/show/signin">I already have an account</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SignUp",
  data() {
    return {
      login: '',
      password: '',
    };
  },
  methods: {
    async signUp() {
      try {
        await axios.post("http://127.0.0.1:8000/auth/users/", {
          username: this.login,
          password: this.password,
        });
        alert("Sign up succeeded");
        this.$router.push({ name: "signin" });
      } catch (error) {
        alert("Error during sign up");
      }
    }
  }
};
</script>

<style scoped>
.sign-up-container {
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

.sign-up-form {
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

.sign-up-button {
  padding: 10px;
  background-color: #283593;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: 0.3s;
}

.sign-up-button:hover {
  background-color: #1a237e;
}

.signin-link {
  margin-top: 15px;
}

.signin-link a {
  text-decoration: none;
  color: #283593;
  font-weight: bold;
}
</style>
