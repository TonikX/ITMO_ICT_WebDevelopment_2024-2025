<template>
  <v-container>
    <h1 class="my-6">Создание новой статьи</h1>

    <v-form v-model="valid" @submit.prevent="submitPost">
      <v-text-field
        v-model="newPost.title"
        label="Заголовок"
        required
        :rules="[rules.required]"
      />

      <v-textarea
        v-model="newPost.content"
        label="Содержимое статьи"
        required
        :rules="[rules.required]"
        rows="10"
      />

      <v-text-field
        v-model="newPost.category"
        label="Категория"
        required
        :rules="[rules.required]"
      />

      <!-- Новое поле для ввода image_url -->
      <v-text-field
        v-model="newPost.image_url"
        label="URL изображения"
        placeholder="Введите URL изображения"
      />

      <v-btn
        class="mt-4"
        color="indigo-darken-3"
        :disabled="!valid"
        type="submit"
      >
        Создать статью
      </v-btn>
    </v-form>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/app';

const router = useRouter();
const store = useAppStore();

// Объект для хранения данных о новом посте
const newPost = ref({
  title: '',
  content: '',
  category: '',
  image_url: ''  // Новое поле для изображения
});

// Форма
const valid = ref(false);
const rules = {
  required: value => !!value || 'Это поле обязательно для заполнения',
};

// Отправка формы
const submitPost = async () => {
  try {
    // Сохраняем новый пост
    await store.createPost(newPost.value);
    router.push('/blogs/all');  // Перенаправляем на страницу со списком постов после создания
  } catch (error) {
    console.error('Ошибка при создании поста:', error);
  }
};
</script>
