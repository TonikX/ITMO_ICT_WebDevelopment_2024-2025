<template>
  <div class="col-md-4 mb-4">
    <div class="card-article card h-100">
      <img
        v-if="post.image"
        :src="getImageUrl(post.id)"
        class="card-img-top"
        :alt="post.title"
        :aria-label="`Image for ${post.title}`"
        @error="onImageError"
      />
      <div class="card-body">
        <h2 class="card-title">{{ post.title }}</h2>
        <p class="card-text">
          {{ truncatedContent }}
        </p>
        <a href="#" class="btn btn-primary" @click.prevent="onReadMore">
          Read More
        </a>
      </div>
      <div class="card-footer text-muted">
        Published: {{ formattedDate }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogCard",
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedDate() {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(this.post.created_at).toLocaleDateString("ru-RU", options);
    },
    truncatedContent() {
      return this.post.content.length > 100
        ? this.post.content.substring(0, 100) + "..."
        : this.post.content;
    },
  },
  methods: {
    onReadMore() {
      this.$emit("readMore", this.post.id);
    },
    async getImageUrl(postId) {
      try {
        const image = await import(`@/assets/${postId}.jpg`);
        return image.default || require('@/assets/3.jpg');
      } catch (error) {
        console.error(`Image not found for post ${postId}, using fallback.`);
        return require('@/assets/3.jpg');
      }
    },
    onImageError(event) {
      event.target.src = require("@/assets/3.jpg");
    },
  },
};
</script>

<style scoped>
:root {
  --background-color: #fbeaff;
  --text-color: #333;
  --card-background: #fff;
  --heading-color: #6a0dad;
  --button-background: #ff85c0;
  --button-border: #ff85c0;
  --modal-background: rgba(0, 0, 0, 0.5);
}

.card-article {
  display: flex;
  flex-direction: column;
  background-color: var(--card-background);
  border-radius: 15px;
  margin-bottom: 20px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card-footer {
  background-color: var(--card-background);
  border-top: 1px solid #ddd;
  font-size: 0.9rem;
}

.btn-primary {
  margin-top: auto;
  background-color: var(--button-background);
  border-color: var(--button-border);
  color: var(--text-color);
  width: 120px;
  height: 40px;
}

h2.card-title {
  color: var(--heading-color);
}
</style>

