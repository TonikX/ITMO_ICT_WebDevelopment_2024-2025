<template>
  <div class="signup-page">
    <div aria-labelledby="signupTitle" class="signup-container" role="form">
      <h1 id="signupTitle" class="signup-title">Sign up</h1>
      <form @submit.prevent="registerUser">
        <label class="visually-hidden" for="email">Email</label>
        <input
            id="email"
            v-model="email"
            aria-required="true"
            class="form-control"
            placeholder="Email"
            type="email"
        />
        <label class="visually-hidden" for="password">Password</label>
        <input
            id="password"
            v-model="password"
            aria-required="true"
            class="form-control"
            placeholder="Password"
            type="password"
        />
        <label class="visually-hidden" for="re_password">Confirm Password</label>
        <input
            id="re_password"
            v-model="re_password"
            aria-required="true"
            class="form-control"
            placeholder="Confirm Password"
            type="password"
        />
        <button aria-label="Sign up" class="signup-button" type="submit">Sign up</button>
      </form>
      <p class="login-text">
        Already have an account?
        <router-link class="login-link" to="/login">Log in!</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import {useAuthStore} from "@/stores/auth"; // Import Pinia store
import {ref} from "vue";
import router from "@/router";

export default {
  name: "SignUp",
  setup() {
    const email = ref("");
    const password = ref("");
    const re_password = ref("");
    const authStore = useAuthStore();

    const registerUser = async () => {
      if (password.value !== re_password.value) {
        alert("Passwords do not match!");
        return;
      }
      try {
        await authStore.register(email.value, password.value, re_password.value);
        alert("Registration successful! Redirecting to login...");
        await router.push("/login");
      } catch (error) {
        alert("Registration failed: " + (error.response?.data?.detail || error.message));
      }
    };

    return {
      email,
      password,
      re_password,
      registerUser,
    };
  },
};
</script>

<style scoped>
body {
  margin: 0;
  font-family: "Tenor Sans", sans-serif;
  background-color: var(--background-color);
}

.signup-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
}

.signup-container {
  width: 100%;
  max-width: 400px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  border-radius: 20px;
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
}

.signup-title {
  font-family: "Limelight", sans-serif;
  font-size: 36px;
  color: var(--text-color);
  margin-bottom: 20px;
}

.form-control {
  width: 100%;
  max-width: 360px;
  height: 50px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  font-size: 18px;
  color: var(--text-color);
  margin-bottom: 20px;
  padding-left: 15px;
}

.form-control::placeholder {
  color: var(--text-color);
}

.signup-button {
  width: 100%;
  max-width: 360px;
  height: 55px;
  background-color: var(--blue-color);
  border: none;
  color: var(--background-color);
  font-family: "Limelight", sans-serif;
  font-size: 22px;
  border-radius: 10px;
  cursor: pointer;
  margin-bottom: 15px;
  transition: background-color 0.3s, color 0.3s;
}

.signup-button:hover {
  background-color: var(--text-color);
  color: var(--blue-color);
}

.login-text {
  color: var(--text-color);
  font-size: 16px;
}

.login-link {
  color: var(--blue-color);
  text-decoration: none;
  font-weight: bold;
}

.login-link:hover {
  text-decoration: underline;
}
</style>