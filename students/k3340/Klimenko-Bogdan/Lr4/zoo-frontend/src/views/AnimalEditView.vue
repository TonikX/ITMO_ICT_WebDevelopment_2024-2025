<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-btn icon @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <h1>Редактирование животного</h1>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="animal.unique_number"
            label="Уникальный номер"
            required
            :rules="[rules.required]"
          ></v-text-field>

          <v-text-field
            v-model="animal.name"
            label="Имя"
            required
            :rules="[rules.required]"
          ></v-text-field>

          <v-select
            v-model="animal.gender"
            :items="genderOptions"
            label="Пол"
            required
          ></v-select>

          <v-text-field
            v-model="animal.birth_date"
            label="Дата рождения"
            type="date"
          ></v-text-field>

          <v-select
            v-model="animal.animal_type"
            :items="typeOptions"
            label="Тип животного"
            required
          ></v-select>

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

          <v-select
            v-model="animal.ownership_type"
            :items="ownershipOptions"
            label="Тип собственности"
            required
          ></v-select>

          <!-- Поля для аренды -->
          <template v-if="animal.ownership_type === 'lease'">
            <v-select
              v-model="animal.owner_zoo"
              :items="zoos"
              item-title="name"
              item-value="id"
              label="Зоопарк-владелец"
              required
            ></v-select>

            <v-text-field
              v-model="animal.lease_cost"
              label="Стоимость аренды"
              type="number"
              required
              :rules="[rules.required, rules.number]"
            ></v-text-field>

            <v-text-field
              v-model="animal.lease_start"
              label="Начало аренды"
              type="date"
            ></v-text-field>

            <v-text-field
              v-model="animal.lease_end"
              label="Окончание аренды"
              type="date"
            ></v-text-field>
          </template>

          <!-- Поля для собственного животного -->
          <template v-else>
            <v-text-field
              v-model="animal.purchase_date"
              label="Дата покупки"
              type="date"
            ></v-text-field>

            <v-text-field
              v-model="animal.seller_organization"
              label="Организация-продавец"
            ></v-text-field>
          </template>

          <v-btn color="primary" @click="save" :disabled="!valid">Сохранить</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { animalService } from '@/services/animals'
import { api } from '@/services/api'

const route = useRoute()
const router = useRouter()
const valid = ref(false)
const form = ref(null)

// Данные животного
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
  lease_start: null,
  lease_end: null,
  purchase_date: null,
  seller_organization: '',
})

// Справочники
const departments = ref([])
const enclosures = ref([])
const habitats = ref([])
const zoos = ref([])

// Опции для селектов
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
  { title: 'Собственность зоопарка', value: 'own' },
  { title: 'Аренда', value: 'lease' },
]

// Правила валидации
const rules = {
  required: (v) => !!v || 'Обязательное поле',
  number: (v) => !v || !isNaN(v) || 'Должно быть числом',
}

// Загрузка справочников и данных животного
onMounted(async () => {
  const id = route.params.id
  try {
    // Параллельно загружаем справочники и данные животного
    const [animalData, deptRes, encRes, habRes, zooRes] = await Promise.all([
      animalService.getById(id),
      api.get('departments/'),
      api.get('enclosures/'),
      api.get('habitats/'),
      api.get('zoos/'),
    ])

    // Заполняем справочники
    departments.value = deptRes.data
    enclosures.value = encRes.data
    habitats.value = habRes.data
    zoos.value = zooRes.data

    // Заполняем данные животного
    animal.value = {
      unique_number: animalData.unique_number || '',
      name: animalData.name || '',
      gender: animalData.gender || 'M',
      birth_date: animalData.birth_date || '',
      animal_type: animalData.animal_type || 'mammal',
      department: animalData.department || null,
      current_enclosure: animalData.current_enclosure || null,
      habitat: animalData.habitat || null,
      ownership_type: animalData.ownership_type || 'own',
      owner_zoo: animalData.owner_zoo || null,
      lease_cost: animalData.lease_cost || null,
      lease_start: animalData.lease_start || null,
      lease_end: animalData.lease_end || null,
      purchase_date: animalData.purchase_date || null,
      seller_organization: animalData.seller_organization || '',
    }
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
    alert('Не удалось загрузить данные животного')
    router.push('/animals')
  }
})

// Сохранение изменений
const save = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return
  try {
    await animalService.update(route.params.id, animal.value)
    router.push(`/animals/${route.params.id}`)
  } catch (error) {
    console.error('Ошибка сохранения:', error)
    alert('Ошибка при сохранении')
  }
}
</script>