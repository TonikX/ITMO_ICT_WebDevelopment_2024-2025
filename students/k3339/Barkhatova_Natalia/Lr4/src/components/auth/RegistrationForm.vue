<template>
  <div class="registration-container">
    <h1>Присоединяйтесь к Нам!</h1>
    <p>Создайте аккаунт, чтобы начать!</p>
    <form class="registration-form" @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email</label>
        <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Введите email"
            class="form-control"
            required
            @input="clearError('email')"
        />
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Введите пароль"
            class="form-control"
            required
            @input="clearError('password')"
        />
        <p v-if="errors.password" class="error">{{ errors.password }}</p>
      </div>
      <div class="form-group">
        <label for="firstName">Имя</label>
        <input
            id="firstName"
            v-model="form.firstName"
            type="text"
            placeholder="Введите имя"
            class="form-control"
            required
            @input="clearError('firstName')"
        />
        <p v-if="errors.firstName" class="error">{{ errors.firstName }}</p>
      </div>
      <div class="form-group">
        <label for="lastName">Фамилия</label>
        <input
            id="lastName"
            v-model="form.lastName"
            type="text"
            placeholder="Введите фамилию"
            class="form-control"
            required
            @input="clearError('lastName')"
        />
        <p v-if="errors.lastName" class="error">{{ errors.lastName }}</p>
      </div>
      <div class="form-group">
        <label for="middleName">Отчество (необязательно)</label>
        <input
            id="middleName"
            v-model="form.middleName"
            type="text"
            placeholder="Введите отчество"
            class="form-control"
            @input="clearError('middleName')"
        />
        <p v-if="errors.middleName" class="error">{{ errors.middleName }}</p>
      </div>
      <button type="submit" class="btn">Зарегистрироваться</button>
    </form>
    <router-link to="/login" class="switch-page-btn">Уже зарегистрированы?</router-link>
  </div>
</template>
<script>
import {reactive, ref} from "vue";
import {useRouter} from "vue-router";
import api from "@/api/api.js";

export default {
  name: "RegistrationForm",
  setup() {
    const form = ref({
      email: "",
      password: "",
      firstName: "",
      lastName: "",
      middleName: "",
      roleId: ""
    });

    const errors = reactive({});
    const router = useRouter();

    const submitForm = async () => {
      try {
        form.value.roleId = "223e4567-e89b-12d3-a456-426614174001";
        await api.post("/auth/registration", form.value);
        alert("Регистрация прошла успешно!");
        router.push("/login");
        errors.value = {};
      } catch (error) {
        if (error.response && error.response.data) {
          const serverErrors = error.response.data;
          for (const key in serverErrors) {
            if (Object.prototype.hasOwnProperty.call(serverErrors, key)) {
              errors[key] = serverErrors[key];
            }
          }
        } else {
          console.error("Ошибка при регистрации:", error);
        }
      }
    };

    const clearError = (field) => {
      if (errors[field]) {
        delete errors[field];
      }
    };

    return {
      form,
      errors,
      submitForm,
      clearError,
    };
  },
};
</script>

<style>
/* Стили для формы регистрации */
.registration-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
}

.registration-container h1 {
  font-size: 36px;
  color: #800020;
}

.registration-container p {
  margin: 10px 0;
  font-size: 18px;
  color: #333;
}

.registration-form {
  background-color: #FFF8DC;
  padding: 30px;
  border: 2px solid #800020;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  margin-right: 30px;
  width: 100%;
}

.label {
  display: block;
  font-size: 18px;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #CCC;
  border-radius: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: border 0.3s, box-shadow 0.3s;
}

.form-control:focus {
  border-color: #800020;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.5);
  outline: none;
}

.btn {
  background-color: #FFAA33;
  color: #fff;
  padding: 10px 25px;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  width: 100%;
}

.btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}
.error {
  color: #D32F2F;
  font-size: 14px;
}

.switch-page-btn {
  margin-top: 20px;
  display: inline-block;
  color: #0066cc;
  font-size: 16px;
  text-decoration: none;
  transition: color 0.3s;
}

.switch-page-btn:hover {
  color: #800020;
}
</style>