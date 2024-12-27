<template>
  <div class="change-password-container">
    <div class="form-card">
      <h2>Смена пароля</h2>
      <form @submit.prevent="changePassword">
        <div class="form-group">
          <label for="old_password">Старый пароль</label>
          <input
            v-model="form.old_password"
            type="password"
            id="old_password"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="new_password">Новый пароль</label>
          <input
            v-model="form.new_password"
            type="password"
            id="new_password"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="re_password">Подтвердите пароль</label>
          <input
            v-model="form.re_password"
            type="password"
            id="re_password"
            required
            class="form-control"
          />
        </div>

        <button type="submit" class="primary-btn">Изменить пароль</button>
      </form>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/UserService';

export default {
  data() {
    return {
      form: {
        old_password: '',
        new_password: '',
        re_password: '',
      },
    };
  },
  methods: {
    async changePassword() {
      if (this.form.new_password !== this.form.re_password) {
        alert('Пароли не совпадают');
        return;
      }
      try {
        await UserService.changePassword(this.form);
        alert('Пароль успешно изменён');
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Ошибка смены пароля:', error);
        alert('Ошибка: ' + (error.response?.data?.old_password || 'Произошла ошибка'));
      }
    },
  },
};
</script>

<style scoped>
.change-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  background-color: #f4f7f6;
}

.form-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.form-card h2 {
  margin-bottom: 25px;
  font-size: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 14px 30px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.primary-btn:hover {
  background-color: #0056b3;
}
</style>
