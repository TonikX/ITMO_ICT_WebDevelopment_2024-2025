<template>
  <v-container class="d-flex justify-center align-center">
    <v-card elevation="10" class="pa-5" width="30%" min-width="400px">
      <v-card-title>Регистрация</v-card-title>
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
            v-model="form.email"
            label="Email"
            :rules="[rules.required, rules.email]"
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
          <v-text-field
            v-model="form.confirmPassword"
            label="Подтвердите пароль"
            :type="showConfirmPassword ? 'text' : 'password'"
            :append-inner-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="toggleConfirmPasswordVisibility"
            :rules="[rules.required, rules.matchPassword]"
            required
          ></v-text-field>
          <v-btn :disabled="!valid" type="submit" color="primary" block>
            Зарегистрироваться
          </v-btn>
          <v-btn class="mt-6" color="secondary" block @click="redirectToLogin">
            Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from "axios";
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const redirectToLogin = () => {
  router.push("/login");
};

const valid = ref(false);
const formRef = ref(null);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const errorMessage = ref("");
const form = reactive({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const rules = {
  required: (value) => !!value || "Обязательное поле",
  email: (value) =>
    /^[\w-.]+@[\w-]+\.+[\w-]{2,4}$/.test(value) || "Некорректный адрес",
  minLength: (length) => (value) =>
    value.length >= length || `Минимальная длина ${length} символов`,
  matchPassword: (value) =>
    value === form.password || "Пароли должны совпадать",
};

const togglePasswordVisibility = () =>
  (showPassword.value = !showPassword.value);
const toggleConfirmPasswordVisibility = () =>
  (showConfirmPassword.value = !showConfirmPassword.value);

const clearError = () => {
  errorMessage.value = "";
};

const submitForm = async () => {
  const { valid } = await formRef.value.validate();
  if (valid) {
    const registrationData = {
      password: form.password,
      username: form.name,
      email: form.email,
    };
    try {
      const response = await axios.post(
        "http://localhost:8000/auth/users/",
        registrationData
      );
      if (response.status === 201) {
        redirectToLogin();
      }
    } catch (err) {
      errorMessage.value = "Произошла ошибка регистрации";
    }
  }
};
</script>
