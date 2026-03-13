<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Животные в зоопарке</h1>
        <v-btn color="primary" to="/animals/create" v-if="userStore.isAuthenticated">Добавить животное</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="animal in animals" :key="animal.id" cols="12" md="4">
        <v-card>
          <v-card-title>{{ animal.name }}</v-card-title>
          <v-card-subtitle>{{ animal.unique_number }}</v-card-subtitle>
          <v-card-text>
            <p>Вид: {{ animal.animal_type }}</p>
            <p>Отдел: {{ animal.department_name }}</p>
            <p>Вольер: {{ animal.enclosure_number }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn :to="`/animals/${animal.id}`">Подробнее</v-btn>
            <v-btn :to="`/animals/${animal.id}/edit`" v-if="userStore.isAuthenticated">Редактировать</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { animalService } from '@/services/animals'
import { useUserStore } from '@/stores/user'

const animals = ref([])
const userStore = useUserStore()

onMounted(async () => {
  try {
    animals.value = await animalService.getAll()
  } catch (error) {
    console.error('Ошибка загрузки животных:', error)
  }
})
</script>