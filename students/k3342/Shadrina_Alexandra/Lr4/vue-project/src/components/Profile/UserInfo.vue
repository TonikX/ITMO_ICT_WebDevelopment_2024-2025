<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const placeholderImage = "src/assets/images/profile.jpg";
const showModal = ref(false);
const showEModal = ref(false);
const modalMessage = ref('');
const newBio = ref("");
const followersCount = ref(0);

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const showEditModal = (message) => {
  modalMessage.value = message;
  showEModal.value = true;
};

const user = ref({
  username: "",
  email: "",
  bio: "",
  date_joined: "",
  profile_image: null,
});

const profileImage = ref(null);

const getUserIdFromToken = async () => {
  try {
    const token = localStorage.getItem("auth_token");
    if (!token) throw new Error("Токен не найден.");

    const response = await axios.get("http://localhost:8000/auth/users/me/", {
      headers: { Authorization: `Token ${token}` },
    });
    return response.data.id;
  } catch (error) {
    console.error("Ошибка получения ID пользователя:", error);
    throw error;
  }
};

const getUserData = async (userId) => {
  try {
    const response = await axios.get(`http://localhost:8000/users/${userId}/`);
    user.value = response.data;
    profileImage.value = response.data.profile_image;
  } catch (error) {
    console.error("Ошибка при получении данных пользователя:", error);
  }
};

const uploadProfileImage = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("profile_image", file);

  try {
    const token = localStorage.getItem("auth_token");
    const response = await axios.patch(`http://localhost:8000/users/${user.value.id}/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${token}`,
      },
    });
    showSuccessModal("Изображение профиля обновлено.");
    profileImage.value = response.data.profile_image;
  } catch (error) {
    console.error("Ошибка при загрузке изображения:", error);
  }
};

const deleteProfile = async () => {
  try {
    const token = localStorage.getItem("authToken");
    await axios.delete(`http://localhost:8000/users/${user.value.id}/`, {
      headers: { Authorization: `Token ${token}` },
    });
    showSuccessModal("Профиль удалён.");
  } catch (error) {
    console.error("Ошибка при удалении профиля:", error);
  }
};

const editProfileModal = () => {
  newBio.value = user.value.bio || "";
  showEModal.value = true;
};

const submitEdit = async () => {
  try {
    const token = localStorage.getItem("auth_token");
    const response = await axios.patch(
      `http://localhost:8000/users/${user.value.id}/`,
      { bio: newBio.value },
      {
        headers: { Authorization: `Token ${token}` },
      }
    );
    showEditModal("Bio обновлено");
    user.value.bio = response.data.bio;
    showModal.value = false;
  } catch (error) {
    console.error("Ошибка при редактировании профиля:", error);
  }
};

const getFollowersCount = async (userId) => {
  try {
    const response = await axios.get(`http://localhost:8000/users/${userId}/subscribers/`);
    followersCount.value = response.data.subscriber_count;
  } catch (error) {
    console.error("Ошибка при получении количества подписчиков:", error);
  }
};


onMounted(async () => {
  try {
    const userId = await getUserIdFromToken();
    await getUserData(userId);
    await getFollowersCount(userId);
  } catch (error) {
    console.error("Ошибка инициализации компонента:", error);
  }
});


const formattedDate = computed(() =>
  new Date(user.value.date_joined).toLocaleDateString()
);
</script>


<template>
  <section class="profile-section">
    <div class="text-center">
      <h1 class="profile-title">Профиль пользователя</h1>
    </div>
    <div class="profile-container">
      <div class="profile-image-container">
        <img
          :src="profileImage || placeholderImage"
          alt="Изображение профиля"
          class="profile-image"
        />
        <label for="profileImageUpload" class="form-label mt-2">
          Загрузить изображение
        </label>
        <input
          id="profileImageUpload"
          type="file"
          accept="image/*"
          @change="uploadProfileImage"
          class="form-control"
        />
      </div>
      <div class="user-info">
        <h3>Личная информация</h3>
        <p><strong>Имя:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Дата регистрации:</strong> {{ formattedDate }}</p>
        <p><strong>Подписчики:</strong> {{ followersCount }}</p>
        <p><strong>Bio:</strong> {{ user.bio || "Био не указано" }}</p>
        <div class="mt-4">
          <button class="btn btn-warning" @click="editProfileModal">Редактировать профиль</button>
          <button class="btn btn-danger" @click="deleteProfile">Удалить профиль</button>
        </div>
      </div>
    </div>
  </section>

  <div v-if="showEModal" class="modal-overlay" @click="showEModal = false">
    <div class="modal-content" @click.stop>
      <h3 class="modal-title">Редактировать био</h3>
      <div class="modal-body">
        <textarea v-model="newBio" class="modal-textarea" placeholder="Введите новое био..."></textarea>
        <button class="btn modal-btn" @click="submitEdit">Сохранить изменения</button>
        <button class="btn cancel-btn" @click="showEModal = false">Отменить</button>
      </div>
    </div>
  </div>
  <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">Уведомление</h3>
        <div class="modal-body">
          {{ modalMessage }}
        </div>
        <button class="btn register-btn" @click="showModal = false">Закрыть</button>
      </div>
  </div>

</template>



<style scoped>

.profile-title {
  font-family: "Quicksand", sans-serif;
  color: var(--divider-color);
  font-weight: bold;
  font-size: 36px;
  text-align: center;
  margin-top: 20px;
}

.profile-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 20px;
  max-width: 900px;
  margin: 40px auto 0;
  padding: 20px;
  background-color: var(--card-bg-color);
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.profile-image-container {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.profile-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 50%;
  border: 2px solid #c0a68f;
}

.user-info {
  flex: 1;
  color: var(--card-text-color);
}

.user-info h3 {
  font-family: "Quicksand", sans-serif;
  color: var(--header-text-color);
  font-size: 24px;
  margin-bottom: 15px;
}

.user-info p {
  font-size: 16px;
  margin-bottom: 10px;
}

.btn-warning {
  background-color: #e8d2ae;
  color: #5B4D42;
  font-weight: bold;
  border: none;
  margin-right: 10px;
}

.btn-danger {
  background-color: #a6433f;
  color: #ffffff;
  border: none;
}

label {
  font-size: 16px;
  color: var(--divider-color);
}

.form-control {
  width: 100%;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #FFFAF3;
  border-radius: 10px;
  border: 1px solid #946A49;
  padding: 20px;
  width: 300px;
  text-align: center;
  animation: fadeIn 0.3s ease-in;
}

.modal-title {
  font-family: Quicksand, sans-serif;
  font-size: 20px;
  font-weight: bold;
  color: #946A49;
}

.modal-body {
  font-family: Quicksand, sans-serif;
  color: #9C7F68;
  padding: 20px;
}

.modal-textarea {
  width: 100%;
  height: 80px;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #946A49;
  background-color: #FFFAF3;
  margin-bottom: 20px;
}

.modal-btn {
  background-color: #e8d2ae;
  border: none;
  padding: 10px 20px;
  margin-right: 10px;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #a6433f;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

