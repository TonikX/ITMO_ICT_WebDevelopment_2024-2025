<template>
  <div>
    <Header />
    <h3 class="table-header">Отчеты по производительности</h3>
    <div class="tabs">
      <button
        v-for="(report, index) in reportTypes"
        :key="index"
        :class="['tab', { active: activeTab === index }]"
        @click="activeTab = index"
      >
        {{ report.label }}
      </button>
    </div>

    <div class="report-content">
      <table v-if="activeTab === 0" class="styled-table">
        <thead>
          <tr>
            <th>Мастерская</th>
            <th>Порода</th>
            <th>Количество кур</th>
            <th>Общее количество яиц</th>
            <th>Средняя продуктивность</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in lastMonthData" :key="item.breed_name + item.workshop">
            <td>{{ item.workshop }}</td>
            <td>{{ item.breed_name }}</td>
            <td>{{ item.chicken_count }}</td>
            <td>{{ item.total_eggs }}</td>
            <td>{{ item.avg_performance }}</td>
          </tr>
        </tbody>
      </table>

      <table v-else-if="activeTab === 1" class="styled-table">
        <thead>
          <tr>
            <th>Сотрудник</th>
            <th>Среднее количество яиц в день</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in eggsByEmployee" :key="employee.employee">
            <td>{{ employee.employee }}</td>
            <td>{{ employee.average_eggs_per_day }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import apiClient from "@/api/axios";

export default {
  components: {
    Header,
  },
  data() {
    return {
      activeTab: 0,
      reportTypes: [
        { label: "Отчет за последний месяц" },
        { label: "Количество яиц на сотрудника" },
      ],
      lastMonthData: [],
      eggsByEmployee: [],
    };
  },
  async created() {
    await this.loadLastMonthData();
    await this.loadEggsByEmployee();
  },
  methods: {
    async loadLastMonthData() {
      try {
        const response = await apiClient.get("/manufactory/reports/");
        this.lastMonthData = response.data.last_month_data;
      } catch (error) {
        console.error("Ошибка при загрузке данных за последний месяц:", error);
        alert("Не удалось загрузить данные за последний месяц.");
      }
    },
    async loadEggsByEmployee() {
      try {
        const response = await apiClient.get("/manufactory/employees/eggs");
        this.eggsByEmployee = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке данных по сотрудникам:", error);
        alert("Не удалось загрузить данные по сотрудникам.");
      }
    },
  },
};
</script>

<style scoped>
html, body, #app {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  height: 100%;
  width: 100%;
}

.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
}

h3.table-header {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.tabs {
  display: flex;
  justify-content: space-evenly; 
  margin-bottom: 20px;
  width: 100%; 
}

.tab {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  background-color: #e9ecef;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s ease;
  text-align: center;
  flex: 1;
  min-width: 100px;
}

.tab.active {
  background-color: #04b922;
  color: white;
}

.tab:hover {
  background-color: #01720a;
  color: white;
}

.report-content {
  padding: 20px;
  width: 100%; 
  box-sizing: border-box;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  table-layout: auto; 
}

.styled-table th, .styled-table td {
  padding: 10px 15px;
  text-align: center;
  border: 1px solid #ddd;
  word-wrap: break-word;
}

.styled-table th {
  background-color: #085d88;
  color: white;
  font-weight: bold;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #e9ecef;
  transition: background-color 0.3s ease-in-out;
}
</style>