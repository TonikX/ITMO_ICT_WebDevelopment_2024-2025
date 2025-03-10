<template>
  <div class="container mt-4">
    <h1>Blog Posts</h1>
    <hr/>

    <div v-if="blogPosts.length > 0">
      <div class="list-group">
        <div
            v-for="post in blogPosts"
            :key="post.id"
            class="list-group-item mb-3"
        >
          <h2>{{ post.title }}</h2>
          <p class="text-muted">
            Posted by <strong>{{ post.author.username }}</strong> on
            {{ formatDate(post.created_at) }}
          </p>
          <p>{{ post.content }}</p>
          <p class="text-muted">
            Last updated: {{ formatDate(post.updated_at) }}
          </p>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info">
      No blog posts found.
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from "vue";
import api from "@/services/axios.ts";

const blogPosts = ref<BlogPost[]>([]);

export interface Author {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  is_superuser: boolean;
}

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: Author;
  created_at: string;
  updated_at: string;
}


onMounted(async () => {
  try {
    const response = await api.get("/fitness/blog-posts/");
    blogPosts.value = response.data;
  } catch (error) {
    console.error("Failed to fetch blog posts:", error);
  }
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};
</script>

<style scoped>
.list-group-item {
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 1rem;
  margin-bottom: 1rem;
}
</style>