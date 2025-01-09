<script setup>
import router from "@/router/index.js";

function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}

import { ref, computed, onMounted, watch } from 'vue';
import { useRecipes } from '@/composables/useRecipes';

const { recipes, loading, error, fetchRecipes } = useRecipes('http://localhost:8000/recipes/');

const searchQuery = ref('');
const selectedTag = ref('');
const selectedDifficulty = ref('');

const dropdownVisible = ref(false);
const toggleDropdown = () => {
  router.push("/search");
  dropdownVisible.value = !dropdownVisible.value;
};

const tags = ref([]);
const fetchTags = async () => {
  try {
    const response = await fetch('http://localhost:8000/tags/');
    tags.value = await response.json();
  } catch (err) {
    console.error('Ошибка загрузки тегов:', err);
  }
};

const filteredRecipes = computed(() => {
  return recipes.value.filter((recipe) => {
    const matchesSearch = recipe.title.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesTag = selectedTag.value ? recipe.tags.includes(selectedTag.value) : true;
    const matchesDifficulty = selectedDifficulty.value
      ? recipe.complexity === selectedDifficulty.value
      : true;
    return matchesSearch && matchesTag && matchesDifficulty;
  });
});

onMounted(async () => {
  await fetchRecipes();
  await fetchTags();
});

watch([searchQuery, selectedTag, selectedDifficulty], () => {
  toggleDropdown(false);
});
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
      v-model="searchQuery"
      @focus="toggleDropdown"
    />
    <div v-if="dropdownVisible" class="filter-dropdown">
      <div class="filter-item">
        <label for="tagSelect">Фильтр по тегу:</label>
        <select
          id="tagSelect"
          v-model="selectedTag"
          class="form-select"
        >
          <option value="">Все</option>
          <option v-for="tag in tags" :key="tag.id" :value="tag.name">{{ tag.name }}</option>
        </select>
      </div>
      <div class="filter-item">
        <label for="difficultySelect">Фильтр по уровню сложности:</label>
        <select
          id="difficultySelect"
          v-model="selectedDifficulty"
          class="form-select"
        >
          <option value="">Все</option>
          <option value="легкий">Легкий</option>
          <option value="средний">Средний</option>
          <option value="сложный">Сложный</option>
        </select>
      </div>
    </div>
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

.search-bar {
  position: relative;
}

.filter-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background-color: var(--card-bg-color);
  color: var(--card-text-color);
  border: 1px solid var(--card-text-color);
  border-radius: 10px;
  width: 100%;
  padding: 10px;
}

.form-select {
  margin-top: 8px;
  background-color: var(--card-bg-color);
  border: 1px solid var(--card-text-color);
  border-radius: 8px;
  color: var(--card-text-color);
}

.filter-dropdown label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

.filter-dropdown button {
  display: block;
  margin-top: 10px;
  width: 100%;
}

</style>
