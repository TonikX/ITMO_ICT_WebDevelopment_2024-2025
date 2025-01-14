<template>
  <div>
    <h2>Тренеры СШ №1</h2>
    <CoachesAddNew />
    <div class="coach-info" v-for="coach in coaches" :key="coach.id">
      <img v-if="coach.gender === 'f'" src="../../assets/images/coaches/coach-icon-f.png" />
      <img v-else src="../../assets/images/coaches/coach-icon-m.png" />
      <div class="coach-details">
        <div class="coach-full-information">
          <h3>{{ coach.last_name }} {{ coach.first_name }} {{ coach.middle_name }}</h3>
          <p>Дата рождения: {{ coach.date_of_birth }}</p>
          <p>Квалификация: {{ coach.qualification.toLowerCase() }}</p>
          <p>Опыт работы: {{ coach.experience }}</p>
        </div>
        <hr>
        <div class="coach-sections">
          <h4>Секции тренера</h4>
          <ul>
            <li v-for="section in coach.sections" :key="section.id" v-if="coach.sections.length>0">
              {{ section.title }}
            </li>
            <li v-else>
              Нет секций
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CoachesAddNew from "@/components/coaches/CoachesAddNew.vue";

export default {
  components: {
    CoachesAddNew,
  },
  data() {
    return {
      coaches: [],
    };
  },
  methods: {
    async fetchCoaches() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/coaches/");
        this.coaches = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке тренеров:", error);
      }
    },
  },
  mounted() {
    this.fetchCoaches();
  },
};
</script>

<style scoped>
div {
  margin: 3%;
}

hr {
  border: none;
  border-left: 2px solid #596dff;
  margin: 0 20px;
}

h2 {
  text-align: center;
  color: #596dff;
}

.coach-info {
  margin-left: auto;
  margin-right: auto;
  display: flex;
  border: 2px solid #596dff;
  border-radius: 20px;
}

.coach-details {
  display: flex;
  flex-direction: row;
  flex: 1;
}

.coach-full-information {
  flex: 1;
}

.coach-sections {
  flex: 0 0 20%;
  padding: 10px;
}

img {
  width: 15%;
  height: 15%;
  border-radius: 50%;
  margin: 2%;
  object-fit: cover;
}

.coach-details h1 {
  margin-bottom: 1%;
}

.coach-details p {
  color: #555555;
  margin: 0.5% 0;
}

.coach-sections ul {
  list-style-type: none;
  padding: 0;
}
</style>
