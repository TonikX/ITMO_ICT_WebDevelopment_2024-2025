<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <button @click="$router.push('/customers')" class="custom-button">Назад к списку клиентов</button>
    <h1 class="page-title">Информация о клиенте</h1>

    <div v-if="customer" class="customer-info">
      <div class="info-item">
        <strong>Имя:</strong> {{ customer.name }}
      </div>
      <div class="info-item">
        <strong>Телефон:</strong> {{ customer.phone }}
      </div>
      <div class="info-item">
        <strong>Email:</strong> {{ customer.email }}
      </div>
      <div class="info-item">
        <strong>Адрес:</strong> {{ customer.address }}
      </div>
      <button @click="$router.push(`/customer-cars/${this.$route.params.id}`)" class="custom-button">Автомобили клиента</button>
    </div>

    <div v-else>
      <p>Загрузка информации...</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  props: ['id'],
  data() {
    return {
      customer: null,
    };
  },
  async created() {
    const customerId = this.$route.params.id; // Получаем ID клиента из URL
    try {
      const response = await apiClient.get(`/clients/${customerId}/`);
      this.customer = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке данных клиента:', error);
    }
  },
};
</script>

<style scoped>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

.page-title {
  text-align: center;
  margin-top: 20px;
  font-size: 28px;
  color: darkslategray;
}

/* Customer Info Styles */
.customer-info {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  width: 90%;
  max-width: 600px;
}

.info-item {
  margin: 10px 0;
  font-size: 18px;
}

button.custom-button {
  background-color: darkslategray !important;
  color: white !important;
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 16px;
  text-transform: none !important;
  border-radius: 5px;
  cursor: pointer;
  display: block;
  width: 100%;
}

button.custom-button:hover {
  background-color: #2f4f4f;
}
</style>
