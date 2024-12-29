<template>
  <v-container class="d-flex justify-center align-center">
    <v-card elevation="10" class="pa-5" width="30%" min-width="400px">
      <v-card-title>Вход</v-card-title>
      <v-card-text>
        <v-alert
          v-if="errorMessage"
          type="error"
          dismissible
          class="mb-4"
          @click:close="clearError"
        >
          {{ errorMessage }}
        </v-alert>
        <v-form ref="formRef" v-model="valid" @submit.prevent="submitForm">
          <v-text-field
            v-model="form.name"
            label="Имя пользователя"
            :rules="[rules.required, rules.minLength(4)]"
            required
          ></v-text-field>
          <v-text-field
            v-model="form.password"
            label="Пароль"
            :type="showPassword ? 'text' : 'password'"
            :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="togglePasswordVisibility"
            :rules="[rules.required, rules.minLength(6)]"
            required
          ></v-text-field>
          <v-btn :disabled="!valid" type="submit" color="primary" block>
            Войти
          </v-btn>
          <v-btn class="mt-6" color="secondary" block @click="redirectToLogin">
            Зарегистрироваться
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const redirectToLogin = () => {
  router.push('/registration');
};

const valid = ref(false);
const formRef = ref(null);
const showPassword = ref(false);
const errorMessage = ref("");
const form = reactive({
  name: '',
  password: '',
});

const rules = {
  required: (value) => !!value || 'Обязательное поле',
  minLength: (length) => (value) => value.length >= length || `Минимальная длина ${length} символов`,
};

const togglePasswordVisibility = () => (showPassword.value = !showPassword.value);

const clearError = () => {
  errorMessage.value = "";
};

const submitForm = async () => {
  const {valid} = await formRef.value.validate();
  if (valid) {
    const loginData = {
        password: form.password,
        username: form.name,
    };
    try{
        const response = await axios.post('http://localhost:8000/auth/token/login/', loginData);
        if (response.status === 200) {
          const token = response.data.auth_token;
          localStorage.setItem('token', token);
          axios.defaults.headers.common['Authorization'] = `Token ${token}`;
          console.log('login successful');
        }
    }
    catch (err) {
        errorMessage.value = "Неверное имя пользователя или пароль";
    }
  }
};
</script>
