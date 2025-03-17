<template>
  <div class="profile-page">
    <h2 class="profile-title">Профиль клиента</h2>

    <!-- Отображение данных профиля -->
    <div v-if="!isEditing" class="profile-info">
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Имя:</strong> {{ client.first_name }}</p>
      <p><strong>Фамилия:</strong> {{ client.last_name }}</p>
      <p><strong>Контактное лицо:</strong> {{ client.contact_person }}</p>
      <p><strong>Телефон:</strong> {{ client.phone }}</p>
      <button @click="isEditing = true" class="edit-button">Редактировать</button>
    </div>

    <!-- Форма для редактирования данных -->
    <form v-if="isEditing" @sub!mit.prevent="updateProfile" class="profile-form">
      <div class="form-group">
        <label for="email">Email:</label>
        <input v-model="user.email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="firstName">Имя:</label>
        <input v-model="client.first_name" type="text" id="firstName" required />
      </div>

      <div class="form-group">
        <label for="lastName">Фамилия:</label>
        <input v-model="client.last_name" type="text" id="lastName" required />
      </div>

      <div class="form-group">
        <label for="contactPerson">Контактное лицо:</label>
        <input v-model="client.contact_person" type="text" id="contactPerson" required />
      </div>

      <div class="form-group">
        <label for="phone">Телефон:</label>
        <input v-model="client.phone" type="tel" id="phone" required />
      </div>

      <button type="submit" class="save-button">Сохранить</button>
      <button type="button" @click="cancelEdit" class="cancel-button">Отменить</button>
    </form>

    <p v-if="message" class="success-message">{{ message }}</p>
  </div>
</template>

<script>
import api from "@/api";

export default {
  name: "ProfilePage",
  data() {
    return {
      user: {},
      client: {},
      isEditing: false,
      message: "",
    };
  },
  async created() {
    try {
      // Получаем данные пользователя
      const userResponse = await api.get("/auth/users/me/");
      this.user = userResponse.data;

      // Получаем данные клиента, привязанного к пользователю
      const clientResponse = await api.get("/client-info/");
      this.client = clientResponse.data;
    } catch (error) {
      console.error("Ошибка загрузки профиля:", error.response ? error.response.data : error.message);
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          console.error("Токен не найден");
          return;
        }
        const headers = { Authorization: `Bearer ${token}` };

        // Обновляем данные пользователя
        await api.patch("/auth/users/me/", {
          email: this.user.email,
        }, { headers });

        // Обновляем данные клиента
        await api.patch(`/auth/clients/${this.client.id}/`, {
          first_name: this.client.first_name,
          last_name: this.client.last_name,
          contact_person: this.client.contact_person,
          phone: this.client.phone,
        }, { headers });

        this.message = "Данные успешно обновлены!";
        this.isEditing = false;
      } catch (error) {
        console.error("Ошибка обновления профиля:", error.response ? error.response.data : error.message);
        this.message = "Ошибка при обновлении профиля.";
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.message = "";
      // Можно добавить перезагрузку данных для отмены изменений
    },
  },
};
</script>

<style scoped>
/* Стили остаются прежними */
.profile-page {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-title {
  text-align: center;
  font-size: 32px;
  margin-bottom: 20px;
  color: #333;
}

.profile-info {
  font-size: 18px;
  margin-bottom: 20px;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

label {
  font-size: 16px;
  color: #555;
}

input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

.save-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: #0056b3;
}

.cancel-button {
  padding: 12px 20px;
  background-color: #f0f0f0;
  color: #333;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #ddd;
}

.success-message {
  color: green;
  margin-top: 15px;
  text-align: center;
}

.edit-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 20px;
}

.edit-button:hover {
  background-color: #0056b3;
}
</style>
