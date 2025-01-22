<template>
  <div class="login-page">
    <img alt="CineLink Logo" class="logo" src="@/assets/images/biglogo.png"/>
    <div aria-labelledby="loginTitle" class="login-container" role="form">
      <form @submit.prevent="loginUser">
        <div id="loginTitle" class="login-title">Log in</div>
        <label class="visually-hidden" for="email">Email</label>
        <input
            id="email"
            v-model="email"
            aria-required="true"
            class="form-control"
            placeholder="Email"
            type="text"
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
        <a aria-label="Forgot your password?" class="forgot-password" href="#">Forgot password?</a>
        <button aria-label="Log in" class="login-button" type="submit">Log in</button>
        <p class="signup-text">
          Don’t have an account?
          <router-link class="signup-link" to="/signup">Sign up!</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {useAuthStore} from "@/stores/auth";
import router from "@/router";

export default {
  name: "LoginPage",
  setup() {
    const email = ref("");
    const password = ref("");
    const authStore = useAuthStore();

    const loginUser = async () => {
      try {
        await authStore.login(email.value, password.value);
        alert("Login successful! Redirecting to profile...");
        await router.push("/profile");
      } catch (error) {
        console.error("Login error:", error);
        alert("Login failed: " + (error.response?.data?.detail || error.message));
      }
    };

    return {
      email,
      password,
      loginUser,
    };
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: "Tenor Sans", sans-serif;
  background-color: var(--background-color);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  padding: 20px;
  box-sizing: border-box;
}

.logo {
  max-width: 80%;
  height: auto;
  margin-bottom: 24px;
}

.login-container {
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

.login-title {
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

.forgot-password {
  align-self: flex-end;
  margin-bottom: 15px;
  color: var(--blue-color);
  text-decoration: none;
  font-size: 14px;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  max-width: 360px;
  height: 55px;
  background-color: var(--blue-color);
  border: 2px solid var(--blue-color);
  color: var(--background-color);
  font-family: "Limelight", sans-serif;
  font-size: 22px;
  border-radius: 10px;
  cursor: pointer;
  margin-bottom: 15px;
  transition: all 0.3s;
}

.login-button:hover {
  background-color: var(--background-color);
  color: var(--blue-color);
}

.signup-text {
  color: var(--text-color);
  font-size: 16px;
}

.signup-link {
  color: var(--blue-color);
  text-decoration: none;
  font-weight: bold;
}

.signup-link:hover {
  text-decoration: underline;
}
</style>