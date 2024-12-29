<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";

const statistics = ref(null);
const error = ref(null);
const selectedMonth = ref(new Date().getMonth() + 1);

async function fetchStatistics() {
  console.log(selectedMonth.value);
  await axios.get("broker/statistics/", {
    params: {month: selectedMonth.value},
  }).then(response => {
        statistics.value = response.data["Your monthly stats"];
        error.value = null;
      }
  ).catch(err => {
    error.value = "Не удалось загрузить статистику.";
    statistics.value = null;
    console.error(err);
  });

}

onMounted(async () => await fetchStatistics());
</script>

<template>
  <div class="broker-statistics">
    <h1>Статистика брокера</h1>
    <div class="month-selector">
      <label for="month">Выберите месяц:</label>
      <select id="month" v-model="selectedMonth" @change="fetchStatistics">
        <option v-for="month in 12" :key="month" :value="month">
          {{ new Date(0, month - 1).toLocaleString("ru", {month: "long"}) }}
        </option>
      </select>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="statistics" class="statistics">
      <p><strong>Куплено:</strong> {{ statistics.bought || 0 }}</p>
      <p><strong>Оплачено:</strong> {{ statistics.paid || 0 }}</p>
    </div>

    <div v-else class="loading">
      Загрузка...
    </div>
  </div>
</template>

<style scoped>
.broker-statistics {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  color: #fff;
  background-color: #2a2a2a;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.month-selector {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

select {
  padding: 5px 10px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #fff;
}

.statistics p {
  margin: 10px 0;
  font-size: 18px;
}

.error {
  color: #f00;
  font-weight: bold;
  text-align: center;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #aaa;
}
</style>
