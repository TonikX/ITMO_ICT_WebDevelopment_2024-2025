<template>
  <v-item-group selected-class="bg-primary">
    <v-container>
      <h1 class="my-6">Тренировки</h1>

      <v-row class="mb-4" align="center">
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="searchQuery"
            label="Поиск по названию"
            prepend-icon="mdi-magnify"
            clearable
          />
        </v-col>

        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedDifficulty"
            :items="difficultyOptions"
            label="Фильтровать по сложности"
            clearable
          />
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="selectedType"
            :items="workoutTypes"
            label="Фильтровать по типу"
            clearable
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col v-for="workout in filteredWorkouts" :key="workout.id" cols="4">
          <v-item v-slot="{ selectedClass }">
            <WorkoutCard :class="[selectedClass]" dark :workout="workout" />
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup>
import WorkoutCard from '@/components/workout-card.vue';
import { useAppStore } from '@/stores/app';
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const store = useAppStore();
const router = useRouter();

if (!store.isAuthenticated) {
  router.push('/login');
}

const searchQuery = ref('');
const selectedDifficulty = ref(null);
const selectedType = ref(null);


// Список с цифрами от 1 до 5 для сложности
const difficultyOptions = [
  1, 2, 3, 4, 5
];
const workoutTypes = [
  "Flexibility", "Cardio", "Strength"
]

// Фильтрация тренировок
const filteredWorkouts = computed(() => {
  let workouts = store.workouts;

  // Фильтрация по сложности
  if (selectedDifficulty.value) {
    workouts = workouts.filter(workout => workout.difficulty === selectedDifficulty.value);
  }

  // Поиск по названию
  if (searchQuery.value) {
    workouts = workouts.filter(workout => workout.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }
  if (selectedType.value) {
        workouts = workouts.filter(workout => workout.type === selectedType.value);

  }

  return workouts;
});


const goToWorkoutDetails = (id) => {
  router.push(`/workouts/${id}`);
};

onMounted(store.fetchWorkouts);
</script>

<style scoped>
p {
  margin-top: 12px;
}
</style>
