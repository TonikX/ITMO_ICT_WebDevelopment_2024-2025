<template>
  <div>
    <h2>Расписание тренировок</h2>
    <coach-filter :coaches="allCoaches" @filter-by-coach="filterScheduleByCoach" />
    <table>
      <thead>
      <tr>
        <th>День недели</th>
        <th>Зал</th>
        <th>Секция</th>
        <th>Время</th>
        <th>Тренеры</th>
      </tr>
      </thead>
      <tbody>
      <template v-for="day in daysOfWeek" :key="day">
        <tr v-if="!filteredSchedule[day].length">
          <td>{{ dayNames[day] }}</td>
          <td colspan="4">Нет тренировок</td>
        </tr>
        <tr v-for="training in filteredSchedule[day]" :key="training.id">
          <td v-if="filteredSchedule[day].indexOf(training) === 0">
            {{ dayNames[day] }}
          </td>
          <td v-else></td>
          <td>{{ training.sport_hall }}</td>
          <td>{{ training.sport_section }}</td>
          <td>{{ training.start_time }} - {{ training.end_time }}</td>
          <td>
            <ul>
              <li v-for="coach in training.coaches" :key="coach.id">
                {{ coach.name }}
              </li>
            </ul>
          </td>
        </tr>
      </template>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import CoachFilter from "./ScheduleCoachesFilter.vue";

export default {
  components: {
    CoachFilter,
  },
  data() {
    return {
      schedule: {
        monday: [],
        tuesday: [],
        wednesday: [],
        thursday: [],
        friday: [],
        saturday: [],
        sunday: [],
      },
      filteredSchedule: {
        monday: [],
        tuesday: [],
        wednesday: [],
        thursday: [],
        friday: [],
        saturday: [],
        sunday: [],
      },
      allCoaches: [],
      daysOfWeek: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
      dayNames: {
        monday: "Понедельник",
        tuesday: "Вторник",
        wednesday: "Среда",
        thursday: "Четверг",
        friday: "Пятница",
        saturday: "Суббота",
        sunday: "Воскресенье",
      },
    };
  },
  methods: {
    async fetchSchedule() {
      try {
        const { data } = await axios.get("http://127.0.0.1:8000/schedule/");
        const groupedSchedule = {
          monday: [],
          tuesday: [],
          wednesday: [],
          thursday: [],
          friday: [],
          saturday: [],
          sunday: [],
        };
        const coachesSet = new Set();
        data.forEach((training) => {
          const day = Object.keys(this.dayNames).find((key) => this.dayNames[key] === training.weekday);
          if (day) {
            groupedSchedule[day].push({
              id: training.id,
              sport_section: training.sport_section.title,
              sport_hall: training.sport_hall.name,
              start_time: training.start_time,
              end_time: training.end_time,
              coaches: training.coaches,
            });
            training.coaches.forEach((coach) => coachesSet.add(coach.name));
          }
        });

        this.schedule = groupedSchedule;
        this.filteredSchedule = { ...groupedSchedule };
        this.allCoaches = Array.from(coachesSet);
      } catch (error) {
        console.error("Ошибка загрузки расписания:", error);
      }
    },
    filterScheduleByCoach(coachName) {
      if (!coachName) {
        this.filteredSchedule = { ...this.schedule };
        return;
      }
      const filtered = {};
      Object.keys(this.schedule).forEach((day) => {
        filtered[day] = this.schedule[day].filter((training) =>
          training.coaches.some((coach) => coach.name === coachName)
        );
      });
      this.filteredSchedule = filtered;
    },
  },
  mounted() {
    this.fetchSchedule();
  },
};
</script>

<style scoped>
div {
  margin: 3%;
}

h2 {
  text-align: center;
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

table tr:nth-child(even) td {
  background-color: #f4f4f4;
}

table tr:hover {
  background-color: #ddd;
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
