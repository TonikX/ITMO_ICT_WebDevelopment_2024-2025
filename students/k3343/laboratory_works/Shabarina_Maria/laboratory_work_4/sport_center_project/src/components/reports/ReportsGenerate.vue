<template>
  <div class="report-generation">
    <h2>Генерация отчетности</h2>
    <div class="coach-selection">
      <select v-model="coachId" id="coachSelect" required>
        <option disabled value="">Выберите тренера</option>
        <option v-for="coach in coaches" :key="coach.id" :value="coach.id">
          {{ coach.name }}
        </option>
      </select>
      <button @click="generateReport">Сгенерировать отчет</button>
    </div>
    <hr>
    <div v-if="report" class="coach-report">
      <h3>Отчет по тренеру: {{ report.coach_info.name }}</h3>
      <hr>
      <h4>Общая информация: </h4>
      <p><strong>Квалификация:</strong> {{ report.coach_info.qualification }}</p>
      <p><strong>Опыт работы:</strong> {{ report.coach_info.experience }} лет</p>
      <p><strong>Общее количество тренировок в неделю:</strong> {{ report.training_count }}</p>
      <hr>
      <h4>Секции:</h4>
      <div v-for="section in report.sections" :key="section.section_title">
        <h6> <strong>{{ section.section_title }} </strong> </h6>
        <p>Расписание:</p>
        <ul>
          <li v-for="schedule in section.schedule" :key="schedule.start_time">
            {{ schedule.weekday }}: {{ schedule.start_time }} - {{ schedule.end_time }} в зале {{ schedule.sport_hall }}
          </li>
        </ul>
        <p>Состав секции: </p>
        <ul>
          <li v-for="sportsman in section.sportsmen" :key="sportsman.name">
            {{ sportsman.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      coachId: null,
      coaches: [],
      report: null,
    };
  },
  methods: {
    async fetchCoaches() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/coaches/");
        this.coaches = response.data.map(coach => ({
          id: coach.id,
          name: `${coach.first_name} ${coach.last_name}`,
        }));
      } catch (error) {
        console.error("Ошибка загрузки тренеров:", error);
      }
    },

    async generateReport() {
      try {
        if (!this.coachId) {
          alert("Пожалуйста, выберите тренера ");
          return;
        }
        const url = `http://127.0.0.1:8000/coaches/${this.coachId}/report/`;
        const response = await axios.get(url);
        this.report = response.data;
      } catch (error) {
        console.error("Ошибка при генерации отчета:", error);
      }
    },
  },
  mounted() {
    this.fetchCoaches();
  },
};
</script>

<style scoped>
h2 {
  text-align: center;
  color: #596dff;
}

h3 {
  color: #596dff;
}

hr {
  border: 1px solid #596dff;
  margin-top: 2%;
  margin-bottom: 2%;
}

.semi-hr {
  border: 1px solid white;
  margin-top: 2%;
  margin-bottom: 2%;
  width: 50%;
}

input,
select,
button {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.report-generation {
  margin: 3%;
}

.coach-selection {
  display: flex;
  flex-direction: column;
  margin-left: 35%;
  width: 30%;
  margin-top: 1%;
}

button {
  background-color: #596dff;
  color: white;
  cursor: pointer;
  margin-top: 2%;
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button:hover {
  background-color: #4150c7;
}


</style>
