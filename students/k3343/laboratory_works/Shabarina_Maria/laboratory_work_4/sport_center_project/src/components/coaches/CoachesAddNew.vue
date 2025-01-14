<template>
  <div class="add-student-form">
    <form @submit.prevent="addCoach">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input type="text" id="first_name" v-model="newCoach.first_name" required />
        </div>
        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input type="text" id="last_name" v-model="newCoach.last_name" required />
        </div>
        <div class="form-group">
          <label for="middle_name">Отчество</label>
          <input type="text" id="middle_name" v-model="newCoach.middle_name" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="gender">Пол</label>
          <select id="gender" v-model="newCoach.gender" required>
            <option value="m">Мужской</option>
            <option value="f">Женский</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date_of_birth">Дата рождения</label>
          <input type="date" id="date_of_birth" v-model="newCoach.date_of_birth" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="qualification">Квалификация</label>
          <input type="text" id="qualification" v-model="newCoach.qualification" required />
        </div>
        <div class="form-group">
          <label for="experience">Опыт работы</label>
          <input type="number" id="experience" v-model="newCoach.experience" required />
        </div>
      </div>
      <button type="submit">Добавить тренера</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newCoach: {
        first_name: "",
        last_name: "",
        middle_name: "",
        gender: "m",
        date_of_birth: "",
        qualification: "",
        experience: "",
      },
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
    async addCoach() {
      try {
        await axios.post("http://127.0.0.1:8000/coaches/", this.newCoach);
        alert("Тренер успешно добавлен в базу");
        this.clearForm();
        await this.fetchCoaches();
      } catch (error) {
        alert("Произошла ошибка при добавлении нового тренера");
      }
    },
    clearForm() {
      this.newCoach = {
        first_name: "",
        last_name: "",
        middle_name: "",
        gender: "m",
        date_of_birth: "",
        qualification: "",
        experience: "",
      };
    },
  },
};
</script>

<style scoped>

.add-student-form {
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  border: 1px solid #ddd;
}

h5 {
  color: #596dff;
  text-align: center;
}

.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.form-group {
  flex: 1;
  min-width: 100px;
}

label {
  display: block;
  font-weight: bold;
}

input,
select,
button {
  width: 100%;
  padding: 5px;
  margin: 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #596dff;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #4759d1;
}
</style>
