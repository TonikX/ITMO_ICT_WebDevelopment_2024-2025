<template>
  <div class="session-board">
    <h2>Киносеансы</h2>
    <div v-if="isLoading" class="loading">Загрузка...</div>
    <div class="session-grid" v-else>
      <SessionPoster
          v-for="session in sessions"
          :key="session.id"
          :session="session"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, computed, onMounted, ref } from 'vue';
import SessionPoster from './SessionPoster.vue';
import { useSessionStore } from "@/stores/session.js";
import { useMovieStore } from "@/stores/movie.js";
import { useHallStore } from "@/stores/hall.js";

export default defineComponent({
  name: 'SessionBoard',
  components: {
    SessionPoster,
  },
  setup() {
    const sessionStore = useSessionStore();
    const isLoading = ref(true);
    const sessions = computed(() => sessionStore.sessions);
    onMounted(async () => {
      if (sessionStore.sessions.length === 0) {
        await sessionStore.fetchSessions();
      }
      isLoading.value = false;
    });

    return {
      sessions,
      isLoading,
    };
  },
});
</script>

<style>
.session-board {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
  text-align: center;
  min-height: 100vh;
}

.session-board h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

.loading {
  font-size: 24px;
  color: #800020;
  font-family: 'Great Vibes', cursive;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.session-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 40px;
  justify-items: center;
  align-items: start;
  padding-top: 20px;
}

.session-poster {
  background-color: #FFF8DC;
  border: 2px solid #800020;
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 300px;
}
</style>
