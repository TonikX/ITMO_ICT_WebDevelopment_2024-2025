<template>
  <v-container class="py-4 ma-auto" v-if="workout">
    <v-btn
      icon
      @click="goBack"
      class="mb-4"
    >
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>

    <div class="text-overline mb-1">{{ workout.type }}</div>
    <h1 class="my-6">{{ workout.title }}</h1>
    <div class="my-3 text-subtitle-1">{{ workout.description }}</div>
    <v-divider></v-divider>
    <div class="d-flex flex-column ga-2 mt-3">
        <p><strong>Длительность:</strong> {{ workout.duration }} минут</p>
        <p><strong>Сложность:</strong> {{ workout.difficulty }}</p>
        <p><strong>Оборудование:</strong> {{ equipment }}</p>
    </div>

    <div class="d-flex align-center ga-3 mt-6 justify-start">
      <v-btn variant="outlined" color="white" @click="startWorkout">
        Начать
      </v-btn>
      <v-btn variant="outlined" color="white" :to="'/workouts/all'">
        Назад к тренировкам
      </v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const store = useAppStore();

const workout = ref(null);

const equipment = computed(() => workout.value?.equipment ? workout.value.equipment.join(', ') : 'Нет');

const fetchWorkoutData = async (id) => {
  const data = await store.fetchWorkoutData(id)
  workout.value = data;
}

const workoutId = route.params.id;

onMounted(() => {
  fetchWorkoutData(workoutId);
});

const startWorkout = () => {
  console.log('Start workout')
  store.startUserWorkout(workoutId)
  fetchWorkoutData(workoutId);
  router.push('/dashboard')
}

const goBack = () => {
  router.go(-1);
}

</script>

<style scoped>
.text-overline {
  font-size: 0.9rem !important;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.7);
}

p {
  font-size: 1rem;
}
</style>
