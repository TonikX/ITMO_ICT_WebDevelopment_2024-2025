<script setup>
import { ref } from "vue";
import { useStore } from "vuex";
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const store = useStore();
const username = ref("");
const password = ref("");

const IncorrectAuth = ref(false);

const goHome = () => {
      router.push({ name: 'hens' });
    };

const login = () => {
  IncorrectAuth.value = false;
  store.dispatch("userLogin", {
    username: username.value,
    password: password.value,
  })
  .then(() => {
    goHome();
  })
  .catch(() => {
    IncorrectAuth.value = true;
  });
};
</script>

<template>
  <div class="wrapper">
    <form class="login form">
      <p>Sign in</p>
      <div class="field">
        <label for="id_username">Username</label>
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          autofocus="autofocus"
          maxlength="150"
          id="id_username"
        />
      </div>
      <div class="field">
        <label for="id_password">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          id="id_password"
        />
      </div>
      <div style="color: red" v-if="IncorrectAuth">Incorrect username or password</div>
      <button @click.prevent="login" class="button primary" type="submit">
        Sign in
      </button>
    </form>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}

.login {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  font-family: 'Arial', sans-serif;
}

.form {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: auto;
}

p {
  font-size: 1.5rem;
  font-weight: bold;
  color: hsla(160, 100%, 37%, 1);
  text-align: center;
  margin-bottom: 1rem;
}

.field {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s;
}

input:focus {
  border-color: hsla(160, 100%, 37%, 1);
  outline: none;
}

button {
  width: 70%;
  padding: 1rem;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: hsla(160, 100%, 37%, 0.8);
}

button:active {
  background-color: hsla(160, 100%, 37%, 0.6);
}

</style>

