<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>Газета</th>
          <th>Почтовое отделение</th>
          <th>Количество</th>
          <th>Дата доставки</th>
          <th>Статус</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="delivery in deliveries" :key="delivery.id">
          <td>{{ delivery.newspaper.name }}</td>
          <td>{{ delivery.post_office.address }}</td>
          <td>{{ delivery.quantity }}</td>
          <td>{{ delivery.delivery_date }}</td>
          <td>{{ delivery.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { getDeliveries } from "../api/api"

export default {
  data() {
    return {
      deliveries: [],
    };
  },
  async created() {
    try {
      const response = await getDeliveries();
      this.deliveries = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных о доставках:", error);
    }
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}
</style>
