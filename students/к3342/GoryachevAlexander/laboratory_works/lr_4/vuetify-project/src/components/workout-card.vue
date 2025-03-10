<template>
  <v-card class="my-4"
          variant="elevated"
          :to="`/workouts/${workout.id}`"
          color="indigo-darken-3"
          >
    <v-card-item>
      <div class="text-overline mb-1">
        {{ workout.type }}
      </div>
      <v-card-title>{{ workout.title }}</v-card-title>
      <v-card-subtitle class="mt-3">{{ workout.description }}</v-card-subtitle>
      <v-divider></v-divider>
      <v-card-subtitle class="mt-3">
        <span>Длительность: {{ workout.duration }} минут</span><br>
        <span>Сложность: {{ workout.difficulty }}</span><br>
        <span>Оборудование: {{ equipment }}</span><br>
      </v-card-subtitle>
    </v-card-item>
  </v-card>
</template>


<script setup>
import { computed } from 'vue';


const props = defineProps({
  workout: {
    type: Object,
    required: true
  }
})

const equipment = computed(() => props.workout.equipment ? props.workout.equipment.join(', ') : 'Нет')
</script>

