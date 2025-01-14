<template>
  <div class="today_trainings_table">
    <h2>Расписание на {{current_day.toLowerCase() }}, {{ current_date }} </h2>
    <div v-if="todaySchedule.length > 0">
      <table>
        <thead>
        <tr>
          <th v-for="(trainings, gym) in groupedSchedule" :key="gym">
            {{ gym }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="rowIndex in maxRows" :key="rowIndex">
          <td v-for="(trainings, gym) in groupedSchedule">
            <div v-if="trainings[rowIndex - 1]">
              <strong> {{ trainings[rowIndex - 1].start_time }} - {{ trainings[rowIndex - 1].end_time }} </strong>
              <br>
              <p> {{ trainings[rowIndex - 1].sport_section.title }} </p>
              <strong class="coach_name"> {{ trainings[rowIndex - 1].coaches[0].name}} </strong>
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <table>
        <thead>
        <tr>
          <th v-for="(trainings, gym) in groupedSchedule" :key="gym">
            {{ gym }}
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="rowIndex in maxRows" :key="rowIndex">
          <td> Нет тренировок</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      schedule: [],
      todaySchedule: [],
      current_day: "",
      current_date: "",
    };
  },
  computed: {
    groupedSchedule() {
      const grouped = {};
      this.todaySchedule.forEach((training) => {
        const gymName = training.sport_hall.name;
        if (!grouped[gymName]) {
          grouped[gymName] = [];
        }
        grouped[gymName].push({
          sport_section: training.sport_section,
          start_time: training.start_time,
          end_time: training.end_time,
          coaches: training.coaches,
        });
      });
      return grouped;
    },
    maxRows() {
      return Math.max(
        ...Object.values(this.groupedSchedule).map((trainings) => trainings.length),
        0
      );
    },
  },
  mounted() {
    this.fetchSchedule();
  },
  methods: {
    async fetchSchedule() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/schedule/");
        this.schedule = Object.values(response.data).flat();
        const date = new Date();
        this.current_date = date.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
        });

        const todayName = this.getTodayName();
        this.todaySchedule = this.schedule.filter(
          (item) => item.weekday === todayName
        );
      } catch (error) {
        console.error("Ошибка при получении расписания:", error);
      }
    },
    getTodayName() {
      const dayNames = [
        "Воскресенье",
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
      ];
      this.current_day = dayNames[new Date().getDay()];
      return dayNames[new Date().getDay()];
    },
  },
};
</script>

<style scoped>
h2 {
  text-align: left;
  color: #596dff;
}
.today_trainings_table {
  margin: 3%;
}

.coach_name {
  color: #596dff;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

table th {
  background-color: #596dff;
  color: white;
  font-weight: bold;
}

table td {
  background-color: #f8f8f8;
}

table td, table th {
  text-align: center;
}

table td ul {
  list-style-type: none;
  padding: 0;
}

table td ul li {
  margin: 5px 0;
  color: #596dff;
}
</style>
