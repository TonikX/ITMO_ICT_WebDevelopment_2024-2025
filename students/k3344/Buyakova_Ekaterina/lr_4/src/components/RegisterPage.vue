<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card width="400">
      <v-card-title>Регистрация</v-card-title>
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
            Регистрация
          </v-btn>
        </v-form>
        <v-btn
          block
          variant="text"
          color="secondary"
          class="mt-2"
          @click="$router.push('/login')"
        >
          Уже есть аккаунт?
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
  name: "RegisterForm",
  setup() {
    const username = ref("");
    const password = ref("");
    const valid = ref(false);

    const emailRules = [
      (v: string) => !!v || "Почта обязательна",
      (v: string) => v.length >= 3 || "Имя пользователя слишком короткое (минимум 3 символа)",
    ];
    const passwordRules = [
      (v: string) => !!v || "Пароль обязательный",
      (v: string) => v.length >= 8 || "Пароль слишком короткий (минимум 8 символов)",
    ];

    const submit = async () => {
      try {
        const response = await axiosApi.post("auth/users/", {
          username: username.value,
          password: password.value,
        });
        router.push('/login')

      } catch (error: any) {
        console.error(error);
        const passwordErrors = error.response.data.password?.join('\n') || '';
        const usernameErrors = error.response.data.username?.join('\n') || '';
        alert("Ошибка при регистрации\n" + usernameErrors + passwordErrors);
      }
    };

    return { username, password, valid, emailRules, passwordRules, submit };
  },
});
</script>
