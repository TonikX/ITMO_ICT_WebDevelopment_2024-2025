<template>
  <div>
    <button @click="$router.push('/main')" class="back-button">Назад на главную страницу</button>
    <h1>Список клиентов</h1>
    <button @click="$router.push('/add-customer')" class="add-button">Добавить клиента</button>
    <ul v-if="customers.length">
      <li v-for="customer in customers" :key="customer.customer_id">
        <router-link :to="`/customer/${customer.customer_id}`">{{ customer.name }}</router-link>
      </li>
    </ul>
    <p v-else>Клиенты не найдены.</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      customers: [],
    };
  },
  async created() {
    try {
      const response = await apiClient.get('/customers/');
      this.customers = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке списка клиентов:', error);
    }
  },
};
</script>

<style scoped>
.back-button,
.add-button {
  margin: 10px 0;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button {
  background-color: #2196f3;
  color: white;
}

.add-button {
  background-color: #4caf50;
  color: white;
}

.back-button:hover {
  background-color: #1976d2;
}

.add-button:hover {
  background-color: #45a049;
}

h1 {
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

router-link {
  text-decoration: none;
  color: #2196f3;
}

router-link:hover {
  text-decoration: underline;
}
</style>
