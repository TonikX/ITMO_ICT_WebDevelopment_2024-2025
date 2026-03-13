<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Новое животное</h1>
        <v-form ref="form" v-model="valid">
          <v-text-field v-model="animal.unique_number" label="Уникальный номер" required :rules="[rules.required]"></v-text-field>
          <v-text-field v-model="animal.name" label="Имя" required :rules="[rules.required]"></v-text-field>
          <v-select v-model="animal.gender" :items="genderOptions" label="Пол" required></v-select>
          <v-text-field v-model="animal.birth_date" label="Дата рождения" type="date"></v-text-field>
          <v-select v-model="animal.animal_type" :items="typeOptions" label="Тип животного" required></v-select>
          <v-select
            v-model="animal.department"
            :items="departments"
            item-title="name"
            item-value="id"
            label="Отдел"
            required
          ></v-select>
          <v-select
            v-model="animal.current_enclosure"
            :items="enclosures"
            item-title="number"
            item-value="id"
            label="Вольер"
            required
          ></v-select>
          <v-select
            v-model="animal.habitat"
            :items="habitats"
            item-title="name"
            item-value="id"
            label="Зона обитания"
            required
          ></v-select>
          <v-select v-model="animal.ownership_type" :items="ownershipOptions" label="Тип собственности" required></v-select>
          <v-text-field
            v-if="animal.ownership_type === 'lease'"
            v-model="animal.owner_zoo"
            label="ID зоопарка-владельца"
            type="number"
          ></v-text-field>
          <v-text-field
            v-if="animal.ownership_type === 'lease'"
            v-model="animal.lease_cost"
            label="Стоимость аренды"
            type="number"
          ></v-text-field>
          <v-btn color="primary" @click="save" :disabled="!valid">Сохранить</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { animalService } from '@/services/animals'
import { api } from '@/services/api'

const router = useRouter()
const valid = ref(false)
const form = ref(null)

const animal = ref({
  unique_number: '',
  name: '',
  gender: 'M',
  birth_date: '',
  animal_type: 'mammal',
  department: null,
  current_enclosure: null,
  habitat: null,
  ownership_type: 'own',
  owner_zoo: null,
  lease_cost: null,
})

const genderOptions = [
  { title: 'Самец', value: 'M' },
  { title: 'Самка', value: 'F' },
]

const typeOptions = [
  { title: 'Млекопитающее', value: 'mammal' },
  { title: 'Птица', value: 'bird' },
  { title: 'Рептилия', value: 'reptile' },
]

const ownershipOptions = [
  { title: 'Собственность', value: 'own' },
  { title: 'Аренда', value: 'lease' },
]

// Справочники
const departments = ref([])
const enclosures = ref([])
const habitats = ref([])

onMounted(async () => {
  try {
    const [deptRes, encRes, habRes] = await Promise.all([
      api.get('departments/'),
      api.get('enclosures/'),
      api.get('habitats/'),
    ])
    departments.value = deptRes.data
    enclosures.value = encRes.data
    habitats.value = habRes.data
  } catch (error) {
    console.error('Ошибка загрузки справочников:', error)
  }
})

const rules = {
  required: v => !!v || 'Обязательное поле',
}

const save = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return
  try {
    await animalService.create(animal.value)
    router.push('/animals')
  } catch (error) {
    console.error('Ошибка сохранения:', error)
  }
}
</script>