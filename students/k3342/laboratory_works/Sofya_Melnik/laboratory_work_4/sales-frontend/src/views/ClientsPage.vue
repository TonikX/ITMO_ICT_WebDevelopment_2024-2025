<template>
  <div class="container">
    <h1>👥 Клиенты</h1>

    <section v-if="clients.length" class="client-list">
      <div v-for="client in clients" :key="client.id" class="client-card">
        <h3>{{ client.first_name }} {{ client.last_name }}</h3>
        <p><strong>📞 Телефон:</strong> {{ client.phone }}</p>
        <p><strong>📧 Email:</strong> {{ client.email || "Не указан" }}</p>
        <p><strong>📍 Контактное лицо:</strong> {{ client.contact_person || "Не указан" }}</p>
      </div>
    </section>

    <p v-else class="no-data">❌ Клиенты не найдены</p>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return { clients: [] };
  },
  async mounted() {
    try {
      const { data } = await api.get("clients/");
      this.clients = data;
    } catch (error) {
      console.error("Ошибка загрузки клиентов:", error);
    }
  },
};
</script>

<style scoped>
/* Основной контейнер */
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

/* Заголовок */
h1 {
  margin-bottom: 20px;
  color: #333;
}

/* Список клиентов */
.client-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  justify-content: center;
}

/* Карточка клиента */
.client-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out;
}

.client-card:hover {
  transform: scale(1.05);
}

/* Заголовок карточки */
.client-card h3 {
  margin-bottom: 10px;
  color: #007bff;
}

/* Текст в карточке */
.client-card p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

/* Сообщение, если данных нет */
.no-data {
  font-size: 18px;
  color: #888;
  margin-top: 20px;
}
</style>
