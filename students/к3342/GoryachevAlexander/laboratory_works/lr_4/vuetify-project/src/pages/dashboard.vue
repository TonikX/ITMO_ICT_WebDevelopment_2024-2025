<template>
  <v-container v-if="user">
    <h1>Личный кабинет Fitness App</h1>
    <div class="d-flex ga-6 mb-6 align-center justify-sm-start">
      <div>
        <h2>Имя: {{ user.username }}</h2>
        <h2>Почта: {{ user.email }}</h2>
        <p class= "workout-progress" v-if="user">Вы выполнили: {{completedWorkouts.length}} из запланированных {{ user.level }} тренировок</p>
        <p v-if="user"> {{(completedWorkouts.length/user.level *100).toFixed(2)}} %</p>

        <ProgressBar :progress="(completedWorkouts.length / user.level) * 100" color="green"/>      </div>



    </div>
    <v-row>
      <v-col>
        <h2>Мои тренировки</h2>
        <div cols="5" class="d-flex flex-wrap ga-4" v-if="userWorkouts.length">
          <div v-for="userWorkout in userWorkouts.slice().reverse()" :key="userWorkout.started_at">
            <UserWorkoutCard
              dark
              :workout="userWorkout"
            />
          </div>
        </div>
        <div v-else><p>Здесь пока нет тренировок</p></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAppStore } from '../stores/app'
import { useRouter } from 'vue-router'
import UserWorkoutCard from '@/components/user-workout-card.vue'
import ProgressBar from "@/components/progress-bar.vue";
const store = useAppStore()
const router = useRouter()

const userWorkouts = computed(() => store.userWorkouts)

const completedWorkouts = computed(() =>
  userWorkouts.value.filter(workout => workout.completed_at !== null)
)

if (!store.isAuthenticated) {
  router.push('/login');
}

const user = computed(() => JSON.parse(store.user))

onMounted(store.fetchUserWorkouts)
</script>

<style scoped>
h1 {
  margin: 24px 0;
}

h2 {
  margin: 16px 0;
}

</style>
