<template>
  <div class="registration-container">
    <div class="registration-box">
      <h2 class="registration-title">Регистрация</h2>
      <form @submit.prevent="register">
        <div class="input-group">
          <input v-model="first_name" class="input" placeholder="Имя" required />
        </div>
        <div class="input-group">
          <input v-model="last_name" class="input" placeholder="Фамилия" required />
        </div>
        <div class="input-group">
          <input v-model="contact_person" class="input" placeholder="Контактное лицо" required />
        </div>
        <div class="input-group">
          <input v-model="phone" type="tel" class="input" placeholder="Телефон" required />
        </div>
        <div class="input-group">
          <input v-model="email" type="email" class="input" placeholder="Email" required />
        </div>
        <div class="input-group">
          <input v-model="username" class="input" placeholder="Логин" required />
        </div>
        <div class="input-group">
          <input v-model="password" type="password" class="input" placeholder="Пароль" required />
        </div>
        <div class="input-group">
          <input v-model="rePassword" type="password" class="input" placeholder="Подтвердите пароль" required />
        </div>
        <button type="submit" class="register-button">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      first_name: "",
      last_name: "",
      contact_person: "",
      phone: "",
      email: "",
      username: "",
      password: "",
      rePassword: "",
    };
  },
  methods: {
    async register() {
      try {

        if (this.password !== this.rePassword) {
          alert("Пароли не совпадают!");
          return;
        }

        localStorage.removeItem("token");
        localStorage.removeItem("refreshToken");

        const registrationData = {
          first_name: this.first_name,
          last_name: this.last_name,
          contact_person: this.contact_person,
          phone: this.phone,
          email: this.email,
          username: this.username,
          password: this.password,
          re_password: this.rePassword
        };

        console.log(registrationData)
        await api.post("auth/users/", registrationData);

        const response = await api.post("auth/jwt/create/", {
          username: this.username,
          password: this.password,
        });

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;
        localStorage.setItem("token", accessToken);
        localStorage.setItem("refreshToken", refreshToken);

        api.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`;

        alert("Регистрация успешна! Вы вошли в систему.");
        this.$router.push("/");
      } catch (error) {
        console.error(error.response?.data);
        alert("Ошибка регистрации: " + (error.response?.data?.detail || "Неизвестная ошибка"));
      }
    },
  },
};
</script>

<style scoped>
/* Стиль для страницы регистрации */
.registration-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f4f7fc;
}

.registration-box {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.registration-title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333333;
}

.input-group {
  margin-bottom: 15px;
}

.input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  background-color: #f7f7f7;
  transition: border-color 0.3s ease;
}

.input:focus {
  border-color: #007bff;
  outline: none;
}

.register-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #0056b3;
}

button[type="submit"] {
  margin-top: 20px;
}

@media (max-width: 600px) {
  .registration-box {
    padding: 20px;
    width: 90%;
  }

  .registration-title {
    font-size: 22px;
  }
}
</style>
