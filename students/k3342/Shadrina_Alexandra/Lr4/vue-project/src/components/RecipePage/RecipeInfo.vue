<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import placeholderImage from '@/assets/images/cooking.png';
import placeholderVideo from '@/assets/videos/default-video.mp4';


const route = useRoute();
const recipe = ref(null);
const followersCount = ref(0);
const isSubscribed = ref(false);

const fetchRecipe = async (id) => {
  try {
    const response = await axios.get(`http://localhost:8000/recipes/${id}/`);
    recipe.value = response.data;
    if (recipe.value.author?.id) {
      await fetchFollowersCount(recipe.value.author.id);
      await checkSubscription(recipe.value.author.id);
    }
  } catch (error) {
    console.error("Ошибка при загрузке рецепта:", error);
  }
};

const fetchFollowersCount = async (userId) => {
  try {
    const response = await axios.get(`http://localhost:8000/users/${userId}/subscribers/`);
    followersCount.value = response.data.subscriber_count;
  } catch (error) {
    console.error("Ошибка при получении количества подписчиков:", error);
  }
};

const getCurrentUserId = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) return null;

    const response = await axios.get('http://localhost:8000/auth/users/me/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data.id;
  } catch (error) {
    console.error('Ошибка при получении данных о пользователе:', error);
    return null;
  }
};

const checkSubscription = async (authorId) => {
  try {
    const response = await axios.get('http://localhost:8000/subscriptions/');
    const subscriptions = response.data;
    const userId = await getCurrentUserId();
    isSubscribed.value = subscriptions.some(
      (sub) => sub.subscriber === userId && sub.chef === authorId
    );
  } catch (error) {
    console.error("Ошибка при проверке подписки:", error);
  }
};

const subscribeToAuthor = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      alert("Вы не авторизованы! Пожалуйста, войдите в систему.");
      return;
    }

    const userId = await getCurrentUserId();
    if (!userId || !recipe.value?.author?.id || userId === recipe.value.author.id) {
      alert("Нельзя подписаться на себя.");
      return;
    }

    if (isSubscribed.value) {
      console.log("Вы уже подписаны на этого автора.");
      return;
    }

    await axios.post('http://localhost:8000/subscriptions/', {
      subscriber: userId,
      chef: recipe.value.author.id,
    });

    isSubscribed.value = true;
    followersCount.value += 1;
  } catch (error) {
    console.error("Ошибка при подписке на автора:", error);
  }
};


onMounted(() => {
  const recipeId = route.params.id;
  fetchRecipe(recipeId);
});
</script>

<template>
  <div v-if="recipe">
    <h1 class="recipe-title">{{ recipe.title }}</h1>

    <p class="recipe-author">
      Автор: <strong>{{ recipe.author.username }}</strong>, подписчики: {{ followersCount || 0 }}
      <button
      v-if="!isSubscribed"
      @click="subscribeToAuthor"
      class="subscribe-button"
    >
      Подписаться
    </button>
    <button v-else class="subscribe-button">Вы подписаны</button>
    </p>


    <div class="recipe-content">
      <img :src="recipe.image || placeholderImage" :alt="recipe.title" class="recipe-image"/>


      <div class="recipe-details">
        <section class="instructions-section">
          <h3>Ингредиенты</h3>
          <p class="text-recipe">{{ recipe.description }}</p>
        </section>

        <section class="instructions-section">
          <h3>Описание по шагам</h3>
          <p>{{ recipe.instructions }}</p>
        </section>
      </div>
    </div>

    <section class="video-section">
      <h3>Видео-рецепт</h3>
      <video controls>
        <source :src="recipe.video || placeholderVideo" type="video/mp4" />
        Ваш браузер не поддерживает видео.
      </video>
    </section>
  </div>

  <div v-else>
    <p>Загрузка...</p>
  </div>
</template>


<style scoped>

.recipe-title {
  font-size: 2.5rem;
  color: var(--divider-color);
  text-align: center;
  margin-bottom: 0.5rem;
}

.recipe-author {
  text-align: center;
  font-size: 1rem;
  color: var(--text-color);
}

.recipe-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.recipe-image {
  flex: 0 0 40%;
  max-width: 100%;
  min-width: 300px;
}

.recipe-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 20px;
}

.instructions-section h3 {
  font-size: 1.5rem;
  color: var(--h3-text-color);
  border-bottom: 2px solid #c77951;
  margin-bottom: 10px;
}

.instructions-section p {
  line-height: 1.6;
  color: var(--text-color);
}

.video-section {
  margin-top: 40px;
  clear: both;
}

.video-section h3 {
  font-size: 1.5rem;
  color: var(--h3-text-color);
  border-bottom: 2px solid #c77951;
  margin-bottom: 10px;
}

video {
    width: 100%;
    height: 400px;
    border-radius: 20px;
    object-fit: cover;
    margin-top: 20px;
}

@media (max-width: 768px) {
  .recipe-content {
    flex-direction: column;
  }

  .recipe-image {
    width: 100%;
  }
}

.subscribe-button {
  display: inline-block;
  background-color: var(--divider-color);
  color: var(--bg-color);
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 10px;
}
.subscribe-button:hover {
  background-color: var(--btn-hover-color);
}

</style>
