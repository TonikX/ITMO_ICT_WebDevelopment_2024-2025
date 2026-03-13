<template>
  <v-container>
    <v-row v-if="animal">
      <v-col cols="12">
        <v-btn icon @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <h1>{{ animal.name }}</h1>
        <v-card>
          <v-card-text>
            <p><strong>Уникальный номер:</strong> {{ animal.unique_number }}</p>
            <p><strong>Дата рождения:</strong> {{ animal.birth_date }}</p>
            <p><strong>Пол:</strong> {{ animal.gender === 'M' ? 'Самец' : 'Самка' }}</p>
            <p><strong>Тип:</strong> {{ animal.animal_type }}</p>
            <p><strong>Отдел:</strong> {{ animal.department_name }}</p>
            <p><strong>Вольер:</strong> {{ animal.enclosure_number }}</p>
            <p><strong>Зона обитания:</strong> {{ animal.habitat_name }}</p>
            <p v-if="animal.ownership_type === 'lease'"><strong>Арендован у:</strong> {{ animal.owner_zoo_name }}</p>
            <p v-else><strong>Собственность зоопарка</strong></p>
          </v-card-text>
          <v-card-actions v-if="userStore.isAuthenticated">
            <v-btn color="warning" :to="`/animals/${animal.id}/edit`">Редактировать</v-btn>
            <v-btn color="error" @click="deleteAnimal">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { animalService } from '@/services/animals'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const animal = ref(null)
const userStore = useUserStore()

onMounted(async () => {
  const id = route.params.id
  try {
    animal.value = await animalService.getById(id)
  } catch (error) {
    console.error('Ошибка загрузки:', error)
  }
})

const deleteAnimal = async () => {
  if (confirm('Вы уверены?')) {
    await animalService.delete(animal.value.id)
    router.push('/animals')
  }
}
</script>