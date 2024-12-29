<template>
  <div class="edit-profile-container">
    <div class="form-card">
      <h1>Редактировать профиль</h1>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="username">Имя пользователя</label>
          <input
            v-model="user.username"
            id="username"
            type="text"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="user.email"
            id="email"
            type="email"
            required
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="passport_data">Паспортные данные</label>
          <input
            v-model="user.passport_data"
            id="passport_data"
            type="text"
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="contact_info">Контактная информация</label>
          <input
            v-model="user.contact_info"
            id="contact_info"
            type="text"
            class="form-control"
          />
        </div>

        <div class="form-actions">
          <button
            type="button"
            @click.prevent="goToChangePassword"
            class="secondary-btn"
          >
            Сменить пароль
          </button>

          <button
            type="button"
            @click.prevent="goToDashboard"
            class="cancel-btn"
          >
            Отмена
          </button>

          <button
            type="submit"
            class="primary-btn"
          >
            Сохранить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/UserService';

export default {
  data() {
    return {
      user: {
        username: '',
        email: '',
        passport_data: '',
        contact_info: '',
      },
    };
  },
  async mounted() {
    try {
      this.user = await UserService.getProfile();
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error);
    }
  },
  methods: {
    async updateProfile() {
      try {
        await UserService.updateProfile(this.user);
        alert('Профиль успешно обновлён');
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('Ошибка обновления профиля:', error);
      }
    },
    goToChangePassword() {
      this.$router.push('/profile/change-password');
    },
    goToDashboard() {
      this.$router.push('/dashboard');
    },
  },
};
</script>

<style scoped>
.edit-profile-container {
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
  max-width: 600px;
  width: 100%;
}
.form-card h1 {
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
.form-actions {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
}
.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.primary-btn:hover {
  background-color: #0056b3;
}
.secondary-btn {
  background-color: #6c757d;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.secondary-btn:hover {
  background-color: #5a6268;
}
.cancel-btn {
  background-color: #e0e0e0;
  color: #333;
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.cancel-btn:hover {
  background-color: #c9c9c9;
}
</style>
