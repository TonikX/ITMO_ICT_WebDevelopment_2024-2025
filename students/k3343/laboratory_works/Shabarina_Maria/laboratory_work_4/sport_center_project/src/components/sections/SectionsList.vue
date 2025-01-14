<template>
  <div class="main">
    <h2>Секции СШ №1</h2>
    <div v-for="section in sections" :key="section.id" class="section-info">
      <div class="section-details">
        <div class="section-full-information">
          <h4>{{ section.title }} </h4>
          <p>Описание: {{ section.description }}</p>
          <p>Тренер: {{ section.coach ? section.coach : "Нет тренера" }}</p>
          <p>Свободных мест: {{ section.free_places }}</p>
        </div>
        <hr>
        <div class="section-sportsmen">
          <strong>Спортсмены:</strong>
          <ol>
            <li v-for="sportsman in section.sportsmen" :key="sportsman.FIO">
              {{ sportsman.FIO }}
            </li>
            <li v-if="section.sportsmen.length === 0">Нет спортсменов в этой секции.</li>
          </ol>
          <div v-if="section.free_places > 0">
            <label for="sportsman">Добавить спортсмена: </label>
            <select v-model="selectedSportsman[section.id]">
              <option value="">Выберите спортсмена</option>
              <option v-for="sportsman in sportsmen" :key="sportsman.id" :value="sportsman.id">
                {{ sportsman.first_name }} {{ sportsman.last_name }} {{ sportsman.middle_name }}
              </option>
            </select>
            <button @click="addSportsmanToSection(section.id)">
              Добавить
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      sections: [],
      sportsmen: [],
      selectedSportsman: {},
    };
  },
  methods: {
    async fetchSections() {
      const response = await axios.get("http://127.0.0.1:8000/sections/");
      this.sections = response.data;
    },
    async fetchSportsmen() {
      const response = await axios.get("http://127.0.0.1:8000/sportsmen/");
      this.sportsmen = response.data;
    },
    async addSportsmanToSection(sectionId) {
      const sportsmanId = this.selectedSportsman[sectionId];
      if (sportsmanId) {
        try {
          await axios.post(`http://127.0.0.1:8000/sections/${sectionId}/add_sportsman/`, {
            sportsman_id: sportsmanId,
          });
          alert("Спортсмен добавлен");
          await this.fetchSections();
        } catch (error) {
          console.error("Ошибка при добавлении спортсмена:", error);
        }
      } else {
        alert("Выберите спортсмена");
      }
    },
  },
  mounted() {
    this.fetchSections();
    this.fetchSportsmen();
  },
};
</script>


<style scoped>
.main {
  margin: 3%;
}

h2 {
  text-align: center;
  color: #596dff;
}

hr {
  border: none;
  border-left: 2px solid #596dff;
  margin: 0 20px;
}

.section-info {
  margin-left: auto;
  margin-right: auto;
  padding: 3%;
  margin-top: 2%;
  display: flex;
  border: 2px solid #596dff;
  border-radius: 20px;
}

.section-details {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.section-full-information {
  flex: 1;
}

.section-sportsmen {
  flex: 0 0 35%;
  padding: 10px;
}

.section-details p {
  color: #555555;
}

label {
  margin-left: 2%;
}

button {
  background-color: #596dff;
  color: white;
  cursor: pointer;
  width: 100%;
  padding: 5px;
  margin: 2%;
  border: none;
  border-radius: 5px;
}

button:hover {
  background-color: #4759d1;
}
</style>
