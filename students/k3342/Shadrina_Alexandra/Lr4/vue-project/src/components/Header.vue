<script setup>
import {useRouter} from "vue-router";
import {ref} from "vue";

const router = useRouter();
const showModal = ref(false);
const modalMessage = ref('');

const showSuccessModal = (message) => {
  modalMessage.value = message;
  showModal.value = true;
};

const logout = () => {
  localStorage.removeItem("auth_token");
  showSuccessModal("Вы успешно вышли из профиля.");
  setTimeout(() => {
    router.push("/");
  }, 1000);
};
function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}
const SearchFilters = () => {
  router.push("/search");
};

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
    <div class="search-bar w-50">
    <input
      type="text"
      class="form-control"
      placeholder="Поиск рецептов..."
      @focus="SearchFilters"
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
      <button id="logout-btn" type="button" class="icons" aria-label="Выйти" @click="logout">
        <svg>
          <use xlink:href="../assets/icons/icons-sprite.svg#box-arrow-in-right"></use>
        </svg>
      </button>
    </nav>
    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-content" @click.stop>
        <h3 class="modal-title">Уведомление</h3>
        <div class="modal-body">
          {{ modalMessage }}
        </div>
        <button class="btn register-btn" @click="showModal = false">Закрыть</button>
      </div>
    </div>
  </header>
</template>

<style>

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
  z-index: 1050;
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

.register-btn {
  background-color: var(--btn-bg-color);
  color: white;
}

.register-btn :hover {
  background-color: var(--btn-hover-color);
  color: white;
}

.search-bar {
  flex: 1 1 33%;
  max-width: 500px;
  min-width: 150px;
  margin: 10px;
}
</style>
