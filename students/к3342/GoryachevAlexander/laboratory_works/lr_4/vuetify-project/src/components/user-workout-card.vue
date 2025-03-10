<template>
  <v-card variant="elevated"
          :to="`/workouts/${workout.workout.id}`"
          color="indigo-darken-3"
          width="240"
          height="100%"
          >
    <v-card-item>
      <div class="text-overline mb-1">
        {{ workout.workout.type }}
      </div>
      <v-card-title>{{ workout.workout.title }}</v-card-title>
      <v-card-subtitle class="mt-3">{{ workout.description }}</v-card-subtitle>
      <v-divider></v-divider>
      <v-card-subtitle class="mt-3">
        <span>Длительность: {{ workout.workout.duration }} минут</span><br>
        <span>Сложность: {{ workout.workout.difficulty }}</span><br>
      </v-card-subtitle>
      <v-divider v-if="workout.started_at"></v-divider>
      <v-card-subtitle class="mt-3">
        <span v-if="workout.started_at" >Начало: {{ startedAt }}</span><br>
        <span v-if="workout.completed_at" >Завершена: {{ completedAt }}</span><br>
      </v-card-subtitle>
    </v-card-item>
    <div class="d-flex align-center ga-3 mx-3 mb-3 justify-start" @click.prevent="completeWorkout">
      <v-btn v-if="!workout.completed_at" variant="outlined" color="white">
        Завершить
      </v-btn>
    </div>
  </v-card>
</template>


<script setup>
import { computed } from 'vue';
import { useAppStore } from '@/stores/app';

const store = useAppStore();

const props = defineProps({
  workout: {
    type: Object,
    required: true
  }
})

const equipment = computed(() => props.workout.workout.equipment ? props.workout.workout.equipment.join(', ') : 'Нет')

const startedAt = computed(() => props.workout.started_at ? formatDate(props.workout.started_at) : 'Нет')
const completedAt = computed(() => props.workout.completed_at ? formatDate(props.workout.completed_at) : 'Нет')

const formatDate = (date) => {
      const d = new Date(date);
      const month = String(d.getMonth() + 1).padStart(2, '0'); // Добавляем ведущий ноль
      const day = String(d.getDate()).padStart(2, '0');
      const year = d.getFullYear();
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      return `${hours}:${minutes} ${day}-${month}-${year}`;
  }

const completeWorkout = () => {
  store.completeUserWorkout(props.workout.id)
  store.fetchUserWorkouts();
}

</script>

