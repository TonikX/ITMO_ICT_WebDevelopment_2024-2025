<template>
  <div>
    <!-- Кнопка добавления поста -->
    <button
      class="btn btn-primary add-post-btn"
      data-bs-toggle="modal"
      data-bs-target="#addPostModal"
      aria-label="Add Post"
    >
      Add Post
    </button>

    <!-- Модальное окно -->
    <div
      class="modal fade"
      id="addPostModal"
      tabindex="-1"
      aria-labelledby="addPostModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addPostModalLabel">Add New Post</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitPost">
              <div class="mb-3">
                <label for="title" class="form-label">Title</label>
                <input
                  type="text"
                  id="title"
                  v-model="newPost.title"
                  required
                  class="form-control"
                />
              </div>
              <div class="mb-3">
                <label for="content" class="form-label">Content</label>
                <textarea
                  id="content"
                  v-model="newPost.content"
                  required
                  class="form-control"
                ></textarea>
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Submit</button>
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="text-center mb-4">
      <button class="btn btn-primary btn-info me-2" @click="fetchRecentPosts">
        Show Recent Posts
      </button>
      <button class="btn btn-primary" @click="resetFilter">
        Show All Posts
      </button>
    </div>

    <!-- Список блогов -->
    <div class="container blog-container" role="main">
      <h1 class="text-center mb-4">Health and Nutrition Blog</h1>

      <div class="row" role="list">
        <!-- Карточки статей -->
        <BlogCard
          v-for="(post, index) in posts"
          :key="post.id"
          :post="post"
          @readMore="goToPost"
        />
      </div>

      <div class="text-center mt-4">
        <router-link
          to="/acc"
          class="btn btn-secondary"
          aria-label="Back to profile page"
        >
          Back to Profile
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import BlogCard from "../components/Blog/BlogCard.vue";
import axios from "axios";
import { TokenStore } from "@/stores/TokenStore.js";

export default {
  name: "Blog",
  components: { BlogCard },
  data() {
    return {
      posts: [],
      allPosts: [],
      newPost: {
        title: "",
        content: "",
      },
    };
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/app/blogposts/");
        this.posts = response.data;
        this.allPosts = response.data;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    async fetchRecentPosts() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/app/recent-blogs/"
        );
        this.posts = response.data;
      } catch (error) {
        console.error("Error fetching recent posts:", error);
      }
    },
    resetFilter() {
      this.posts = [...this.allPosts];
    },
    async submitPost() {
      const tokenStore = TokenStore();

      const postData = {
        ...this.newPost,
        author: tokenStore.userId,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/app/blogposts/create/",
          postData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${tokenStore.token}`,
            },
          }
        );

        this.posts.unshift(response.data);
        this.allPosts.unshift(response.data);

        alert("Post added successfully!");

        const modalElement = document.getElementById("addPostModal");
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        setTimeout(() => {
          modalInstance.hide();
        }, 3000);

        this.newPost = {
          title: "",
          content: "",
        };
      } catch (error) {
      }
    },
    goToPost(postId) {
      this.$router.push(`/post/`);
    },
  },
  mounted() {
    this.fetchPosts();
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
}

.blue-theme {
    --background-color: #e0f7fa;
    --text-color: #333;
    --card-background: #ffffff;
    --heading-color: #00796b;
    --button-background: #00acc1;
    --button-border: #00acc1;
    --modal-background: rgba(0, 0, 0, 0.5);
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
    margin: 0;
    font-family: Arial, sans-serif;
}

.blog-container {
    padding: 20px;
}

.modal-content {
    background-color: #fff;
    border-radius: 15px;
    color: #000;
}

.modal-header,
.modal-footer {
    background-color: #f8f9fa;
}

.modal-backdrop {
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-body form input, .modal-body form textarea {
    border: 1px solid #ddd;
    padding: 10px;
    width: 100%;
    border-radius: 5px;
}

.add-post-btn {
    position: fixed;
    top: 10px;
    left: 60px;
    z-index: 1000;
}

h1, .card-title {
    color: var(--heading-color);
}

.card-article {
    background-color: var(--card-background);
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-primary {
    background-color: var(--button-background);
    border-color: var(--button-border);
    color: var(--text-color);
}

.btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
    color: #fff;
}

.theme-switcher {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    cursor: pointer;
}

.theme-switcher i {
    font-size: 2rem;
    color: #000;
    transition: color 0.3s ease;
}

.theme-switcher:hover i {
    color: #00796b;
}

.blog-container {
    margin-top: 20px;
}

.text-center {
    text-align: center;
}

.text-center button, .text-center a {
    margin: 10px 0;
}

@media (max-width: 768px) {
    .add-post-btn {
        left: 10px;
        top: 60px;
    }

    .modal-dialog {
        width: 100%;
        margin: 0;
    }

    .container.blog-container {
        padding: 10px;
    }
}
</style>
