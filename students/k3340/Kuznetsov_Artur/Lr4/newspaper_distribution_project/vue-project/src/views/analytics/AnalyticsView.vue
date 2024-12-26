<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const newspaperNameForm = ref({name: ''})
const printingHouseForm = ref({printing_house_id: ''})
const minPriceForm = ref({min_price: ''})
const maxQuantityForm = ref({max_quantity: ''})
const newspaperAndAddressForm = ref({name: '', address: ''})

const addressesResult = ref([])
const topEditorResult = ref(null)
const expensiveNewspapersResult = ref([])
const lowQuantityResult = ref([])
const destinationsResult = ref([])

const errorMessage = ref('')

function handleError(error) {
  console.error(error)
  errorMessage.value = 'Произошла ошибка. Пожалуйста, проверьте введённые данные.'
}

async function fetchAddresses() {
  errorMessage.value = ''
  addressesResult.value = []
  try {
    const response = await axiosClient.post('/newspapers/addresses/', newspaperNameForm.value)
    addressesResult.value = response.data.addresses
  } catch (error) {
    handleError(error)
  }
}

async function fetchTopEditor() {
  errorMessage.value = ''
  topEditorResult.value = null
  try {
    const response = await axiosClient.post('/printinghouses/top-editor/', printingHouseForm.value)
    topEditorResult.value = response.data
  } catch (error) {
    handleError(error)
  }
}

async function fetchExpensiveNewspapers() {
  errorMessage.value = ''
  expensiveNewspapersResult.value = []
  try {
    const response = await axiosClient.post('/postoffices/expensive-newspapers/', minPriceForm.value)
    expensiveNewspapersResult.value = response.data.offices
  } catch (error) {
    handleError(error)
  }
}

async function fetchLowQuantity() {
  errorMessage.value = ''
  lowQuantityResult.value = []
  try {
    const response = await axiosClient.post('/distributions/low-quantity/', maxQuantityForm.value)
    lowQuantityResult.value = response.data.distributions
  } catch (error) {
    handleError(error)
  }
}

async function fetchDestinations() {
  errorMessage.value = ''
  destinationsResult.value = []
  try {
    const response = await axiosClient.post('/distributions/destination-by-address/', newspaperAndAddressForm.value)
    destinationsResult.value = response.data.destinations
  } catch (error) {
    handleError(error)
  }
}
</script>

<template>
  <v-container>
    <v-card class="pa-4 mb-4">
      <v-card-title>Получение адресов, где печатается конкретная газета</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchAddresses">
          <v-text-field v-model="newspaperNameForm.name" label="Название газеты" required></v-text-field>
          <v-btn color="primary" @click="fetchAddresses">Получить адреса</v-btn>
        </v-form>
        <ul v-if="addressesResult.length">
          <li v-for="address in addressesResult" :key="address">{{ address }}</li>
        </ul>
      </v-card-text>
    </v-card>

    <v-card class="pa-4 mb-4">
      <v-card-title>Редактор, который печатается в указанной типографии самым большим тиражом</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchTopEditor">
          <v-text-field v-model="printingHouseForm.printing_house_id" label="ID типографии" required></v-text-field>
          <v-btn color="primary" @click="fetchTopEditor">Получить редактора</v-btn>
        </v-form>
        <p v-if="topEditorResult">
          Редактор: {{ topEditorResult.editor_name }} (ID: {{ topEditorResult.editor_id }}), Тираж:
          {{ topEditorResult.total_quantity }}
        </p>
      </v-card-text>
    </v-card>

    <v-card class="pa-4 mb-4">
      <v-card-title>Почтовые отделения, куда поступают газеты дороже указанной цены</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchExpensiveNewspapers">
          <v-text-field v-model="minPriceForm.min_price" label="Минимальная цена" type="number" required></v-text-field>
          <v-btn color="primary" @click="fetchExpensiveNewspapers">Получить отделения</v-btn>
        </v-form>
        <ul v-if="expensiveNewspapersResult.length">
          <li v-for="office in expensiveNewspapersResult" :key="office.post_office_address">
            Газета: {{ office.newspaper_name }} → Почтовое отделение:
            {{ office.post_office_address }}
          </li>
        </ul>
      </v-card-text>
    </v-card>


    <v-card class="pa-4 mb-4">
      <v-card-title>Газеты, которые поступают в почтовые отделения в количестве меньше указанного</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchLowQuantity">
          <v-text-field v-model="maxQuantityForm.max_quantity" label="Максимальное количество" type="number"
                        required></v-text-field>
          <v-btn color="primary" @click="fetchLowQuantity">Получить газеты</v-btn>
        </v-form>
        <ul v-if="lowQuantityResult.length">
          <li v-for="item in lowQuantityResult" :key="item.newspaper__name">
            {{ item.newspaper__name }} → Почтовое отделение №{{ item.post_office__number }}, Количество:
            {{ item.quantity }}
          </li>
        </ul>
      </v-card-text>
    </v-card>

    <v-card class="pa-4 mb-4">
      <v-card-title>Почтовые отделения, куда поступает указанная газета из указанной типографии</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchDestinations">
          <v-text-field v-model="newspaperAndAddressForm.name" label="Название газеты" required></v-text-field>
          <v-text-field v-model="newspaperAndAddressForm.address" label="Адрес типографии" required></v-text-field>
          <v-btn color="primary" @click="fetchDestinations">Получить отделения</v-btn>
        </v-form>
        <ul v-if="destinationsResult.length">
          <li v-for="destination in destinationsResult" :key="destination.post_office__address">
            {{ destination.post_office__address }}: {{ destination.quantity }} экз.
          </li>
        </ul>
      </v-card-text>
    </v-card>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </v-container>
</template>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
}
</style>
