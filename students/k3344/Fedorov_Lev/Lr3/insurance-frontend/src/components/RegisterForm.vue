<template>
  <div class="register-form-container">
    <div class="register-form">
      <h1>Регистрация</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Имя пользователя:</label>
          <input v-model="username" id="username" required />
          <p v-if="errors.username" class="error">{{ errors.username }}</p>
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input v-model="email" type="email" id="email" required />
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>

        <div class="form-group">
          <label for="password">Пароль:</label>
          <input v-model="password" type="password" id="password" required />
        </div>

        <div class="form-group">
          <label for="re_password">Повторите пароль:</label>
          <input v-model="re_password" type="password" id="re_password" required />
          <p v-if="errors.re_password" class="error">{{ errors.re_password }}</p>
        </div>

        <div class="form-group">
          <label for="role">Роль:</label>
          <select v-model="role" id="role" required>
            <option value="employee">Сотрудник</option>
            <option value="agent">Агент</option>
          </select>
        </div>

        <div class="form-group" v-if="role">
          <label for="passport_data">Паспортные данные:</label>
          <input v-model="passport_data" id="passport_data" required />
          <p v-if="errors.passport_data" class="error">{{ errors.passport_data }}</p>
        </div>

        <div class="form-group">
          <label for="organization">
            {{ role === 'employee' ? 'Организация' : 'Агентство' }}:
          </label>
          <select v-model="organization" id="organization" required>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name || org.full_name }}
            </option>
          </select>
        </div>

        <div class="form-group" v-if="role === 'employee'">
          <label for="age">Возраст:</label>
          <input v-model="age" type="number" id="age" :min="18" required />
        </div>

        <div class="form-group" v-if="role === 'employee'">
          <label for="position">Позиция:</label>
          <select v-model="position" id="position" required>
            <option v-for="pos in positions" :key="pos.id" :value="pos.id">
              {{ pos.name }}
            </option>
          </select>
        </div>

        <button class="register-button" type="submit" :disabled="loading">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
        <p class="general-error" v-if="generalError">{{ generalError }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AuthService from '@/services/AuthService';

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      re_password: '',
      role: 'employee',
      age: 18,
      passport_data: '',
      organization: '',
      position: '',
      organizations: [],
      positions: [],
      loading: false,
      errors: {},
      generalError: '',
    };
  },
  watch: {
    role() {
      this.fetchOrganizationsOrAgencies();
    },
  },
  async created() {
    await this.fetchOrganizationsOrAgencies();
    await this.fetchPositions();
  },
  methods: {
    async fetchOrganizationsOrAgencies() {
      try {
        const url =
          this.role === 'employee'
            ? 'http://localhost:8000/insurance/organizations/'
            : 'http://localhost:8000/insurance/agencies/';

        const response = await axios.get(url);
        this.organizations = response.data;
      } catch (error) {
        console.error('Ошибка загрузки организаций/агентств:', error);
      }
    },

    async fetchPositions() {
      try {
        const response = await axios.get(
          'http://localhost:8000/insurance/positions/'
        );
        this.positions = response.data;
      } catch (error) {
        console.error('Ошибка загрузки позиций:', error);
      }
    },

    async register() {
      this.errors = {};
      this.generalError = '';

      if (this.password !== this.re_password) {
        this.errors.re_password = 'Пароли не совпадают!';
        return;
      }

      this.loading = true;
      try {
        const userData = {
          username: this.username,
          email: this.email,
          password: this.password,
          re_password: this.re_password,
          role: this.role,
          passport_data: this.passport_data,
        };

        if (this.role === 'employee') {
          userData.organization = this.organization;
          userData.age = this.age;
          userData.position = this.position;
        } else if (this.role === 'agent') {
          userData.agency = this.organization;
        }

        const response = await AuthService.register(userData);
        localStorage.setItem('token', response.access);
        this.$router.push('/dashboard');
      } catch (error) {
        const responseErrors = error.response?.data;
        if (responseErrors) {
          this.errors = responseErrors;
        } else {
          this.generalError = 'Ошибка регистрации. Попробуйте позже.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.register-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: white;
}

.register-form {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

h1 {
  text-align: center;
  margin-bottom: 24px;
  font-family: 'Arial', sans-serif;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
}

.register-button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 5px;
}

.general-error {
  color: red;
  text-align: center;
  margin-top: 20px;
}
</style>
