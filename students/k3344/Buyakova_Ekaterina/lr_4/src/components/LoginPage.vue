<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card width="400">
      <v-card-title>Вход</v-card-title>
      <v-card-text>
        <v-form v-model="valid">
          <v-text-field
            v-model="username"
            :rules="emailRules"
            label="Имя пользователя"
            required
            outlined
          ></v-text-field>
          <v-text-field
            v-model="password"
            :rules="passwordRules"
            label="Пароль"
            type="password"
            required
            outlined
          ></v-text-field>
          <v-btn
            :disabled="!valid"
            block
            color="primary"
            class="mt-4"
            @click="submit"
          >
            Вход
          </v-btn>
        </v-form>
        <v-btn
          block
          variant=text
          color="secondary"
          class="mt-2"
          @click="$router.push('/register')"
        >
          Ещё нет аккаунта?
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import axiosApi from "@/plugins/axios";
import router from "@/router";
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "LoginForm",
  setup() {
    const username = ref("");
    const password = ref("");
    const valid = ref(false);

    const emailRules = [
      (v: string) => !!v || "Имя пользователя обязательно",
      (v: string) => v.length >= 3 || "Имя пользователя слишком короткий (минимум 3 символа)",
    ];
    const passwordRules = [
      (v: string) => !!v || "Пароль обязателен",
      (v: string) => v.length >= 8 || "Пароль слишком короткий (минимум 8 символов)",
    ];

    const submit = async () => {
      try {
        const response = await axiosApi.post("auth/token/login/", {
          username: username.value,
          password: password.value,
        });
        localStorage.setItem('authToken', response.data.auth_token);
        console.log(response.data.auth_token);
        router.push('/')
        alert("Вход успешный");
      } catch (error: any) {
        console.error(error);
        const nonFieldErrors = error.response.data.non_field_errors ? 'Неверное имя или пароль' : '';
        alert("Ошибка при входе\n" +nonFieldErrors);
      }
    };

    return { username, password, valid, emailRules, passwordRules, submit };
  },
});
</script>
