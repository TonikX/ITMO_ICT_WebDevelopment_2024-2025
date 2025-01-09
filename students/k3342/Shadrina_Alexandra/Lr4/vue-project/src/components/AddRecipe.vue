<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}

const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const router = useRouter();

const recipe = ref({
  title: '',
  description: '',
  instructions: '',
  complexity: '',
  image: null,
  video: null,
  tags: [],
});

const tags = ref([]);

const loadTags = async () => {
  try {
    const response = await axios.get('http://localhost:8000/tags/');
    console.log(response);
    tags.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки тегов:', error);
  }
};

const handleFileUpload = (e, field) => {
  recipe.value[field] = e.target.files[0];
};

const addRecipe = async () => {
  const formData = new FormData();
  for (const key in recipe.value) {
    if (key === 'tags') {
      recipe.value[key].forEach((tagId) => {
        formData.append('tags', tagId);
      });
    } else {
      formData.append(key, recipe.value[key]);
    }
  }

  try {
    const response = await axios.post('http://localhost:8000/recipes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data' },
        'Authorization': `Token ${localStorage.getItem('token')}`,
    });
    console.log('Рецепт добавлен:', response.data);
    showSuccessModal('Рецепт успешно добавлен!');
    Object.keys(recipe.value).forEach((key) => {
      recipe.value[key] = key === 'tags' ? [] : '';
    });
  } catch (error) {
    console.error('Ошибка добавления рецепта:', error);
    showSuccessModal('Ошибка добавления рецепта.');
  }
};

const cancel = () => {
  router.push('/');
};

loadTags();

</script>

<template>
  <header class="header">
    <div class="brand d-flex align-items-center">
      <a href="/" class="d-flex align-items-center logo-link">
        <img src="../assets/icons/recipe-book.png" alt="Logo" class="logo me-2" />
        <span>Culinarity</span>
      </a>
    </div>
    <div class="theme-switcher">
        <label for="themeToggle" class="form-check-label">Тема</label>
        <input
          type="checkbox"
          id="themeToggle"
          class="form-check-input"
          @change="toggleTheme"
          aria-label="Переключатель темы"
        />
      </div>
    <nav class="icons">
      <a href="/profile" aria-label="Профиль пользователя">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#person-circle"></use>
        </svg>
      </a>
      <a href="/add/recipe" aria-label="Добавить рецепт">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#plus-circle-fill"></use>
        </svg>
      </a>
    </nav>
  </header>
  <div class="container">
    <div class="registration-container">
      <h1 class="text-center">Добавить рецепт</h1>
      <form @submit.prevent="addRecipe">
        <div class="form-group">
          <label for="title" class="form-label"><strong>Название</strong></label>
          <input
            type="text"
            id="title"
            v-model="recipe.title"
            class="form-control"
            required
          />
        </div>

        <div class="form-group">
          <label for="description" class="form-label"><strong>Ингредиенты</strong></label>
          <textarea
            id="description"
            v-model="recipe.description"
            class="form-control"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="instructions" class="form-label"><strong>Инструкции</strong></label>
          <textarea
            id="instructions"
            v-model="recipe.instructions"
            class="form-control"
            rows="5"
            required
          ></textarea>
        </div>

        <div class="form-group">
          <label for="complexity" class="form-label"><strong>Сложность</strong></label>
          <select
            id="complexity"
            v-model="recipe.complexity"
            class="form-control"
            required
          >
            <option value="easy">Легко</option>
            <option value="medium">Средне</option>
            <option value="hard">Трудно</option>
          </select>
        </div>

        <div class="form-group">
          <label for="tags" class="form-label"><strong>Теги</strong></label>
          <select
            id="tags"
            v-model="recipe.tags"
            class="form-control"
            multiple
          >
            <option v-if="tags.length === 0" disabled>Нет доступных тегов</option>
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="image" class="form-label"><strong>Изображение</strong></label>
          <input
            type="file"
            id="image"
            @change="(e) => handleFileUpload(e, 'image')"
            class="form-control-file"
          />
        </div>

        <div class="form-group">
          <label for="video" class="form-label"><strong>Видео</strong></label>
          <input
            type="file"
            id="video"
            @change="(e) => handleFileUpload(e, 'video')"
            class="form-control-file"
          />
        </div>

        <button type="submit" class="btn register-btn">Добавить рецепт</button>
      </form>

      <button @click="cancel" class="btn btn-secondary mt-2">Отменить</button>
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
  </div>
</template>

<style scoped>

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: var(--header-bg-color) ;
    color: var(--header-text-color);
    flex-wrap: wrap;
}


header .brand {
    font-family: Quicksand, sans-serif;
    font-size: 24px;
    font-weight: bold;
    color: var(--header-text-color);
}

.icons svg {
    width: 30px;
    height: 30px;
    fill: currentColor;
    cursor: pointer;
    transition: transform 0.2s ease;
    margin-right: 20px;
}


.icons a {
    color: var(--header-text-color);
}

.icons svg:hover {
  transform: scale(1.1);
}

.icons button {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
}

.logo {
    width: 40px;
    height: auto;
}

.logo-link {
    text-decoration: none;
    color: inherit;
}

.logo-link:hover {
    text-decoration: none;
    color: inherit;
}

body {
  font-family: Quicksand, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.registration-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background-color: var(--form-bg-color);
  border-radius: 15px;
  box-shadow: 0 0 10px var(--form-border-color);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: var(--text-center-color);
}

.form-group {
  margin-bottom: 15px;
}

textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  resize: vertical;
}

button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.register-btn {
  background-color: var(--btn-bg-color);
  color: #fff;
}

.register-btn:hover {
  background-color: var(--btn-hover-color);
}

.register-btn:focus {
  background-color: var(--btn-hover-color);
}

.btn-secondary {
  background-color: #f0ad4e;
}

.btn-secondary:hover {
  background-color: #ec971f;
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
</style>
