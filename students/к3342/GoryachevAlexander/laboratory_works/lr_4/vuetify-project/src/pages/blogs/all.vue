<template>
  <v-item-group selected-class="bg-primary">
    <v-container>
      <h1 class="my-6">Статьи</h1>

      <v-btn
        color="indigo-darken-3"
        class="mb-4"
        @click="openCreatePost"
      >
        Добавить статью
      </v-btn>

      <v-row dense no-gutters class="my-3 gr-4">
        <v-col cols="4" class="pr-4" v-for="post in store.posts" :key="post.id">
          <postCard :post="post" class="w-100" />
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup>
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import postCard from '@/components/post-card.vue';

const store = useAppStore();
const router = useRouter();

// Метод для открытия страницы создания статьи
const openCreatePost = () => {
  router.push('/blogs/create');
};
onMounted(store.fetchPosts);
</script>
