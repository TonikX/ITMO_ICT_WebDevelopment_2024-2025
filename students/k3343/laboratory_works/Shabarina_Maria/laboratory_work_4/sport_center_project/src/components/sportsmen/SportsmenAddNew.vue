<template>
  <div class="add-student-form">
    <form @submit.prevent="addSportsmen">
      <div class="form-row">
        <div class="form-group">
          <label for="first_name">Имя</label>
          <input type="text" id="first_name" v-model="newSportsman.first_name" required />
        </div>
        <div class="form-group">
          <label for="last_name">Фамилия</label>
          <input type="text" id="last_name" v-model="newSportsman.last_name" required />
        </div>
        <div class="form-group">
          <label for="middle_name">Отчество</label>
          <input type="text" id="middle_name" v-model="newSportsman.middle_name" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="gender">Пол</label>
          <select id="gender" v-model="newSportsman.gender" required>
            <option value="m">Мужской</option>
            <option value="f">Женский</option>
          </select>
        </div>
        <div class="form-group">
          <label for="date_of_birth">Дата рождения</label>
          <input type="date" id="date_of_birth" v-model="newSportsman.date_of_birth" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="phone_number">Телефон</label>
          <input type="tel" id="phone_number" v-model="newSportsman.phone_number" required />
        </div>
        <div class="form-group">
          <label for="email">Почта</label>
          <input type="email" id="email" v-model="newSportsman.email" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label for="registration_date">Дата зачисления</label>
          <input type="date" id="registration_date" v-model="newSportsman.registration_date" required />
        </div>
      </div>
      <button type="submit">Добавить ученика</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      newSportsman: {
        first_name: "",
        last_name: "",
        middle_name: "",
        gender: "m",
        date_of_birth: "",
        phone_number: "",
        email: "",
        registration_date: "",
      },
    };
  },
  methods: {
    async fetchSportsmen() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/sportsmen/");
        this.students = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке учеников:", error);
      }
    },
    async addSportsmen() {
      try {
        await axios.post("http://127.0.0.1:8000/sportsmen/", this.newSportsman);
        alert("Спортсмен успешно добавлен в базу");
        this.clearForm();
        await this.fetchSportsmen();
      } catch (error) {
        alert("Произошла ошибка при добавлении спортсмена");
      }
    },
    clearForm() {
      this.newSportsman = {
        first_name: "",
        last_name: "",
        middle_name: "",
        gender: "m",
        date_of_birth: "",
        phone_number: "",
        email: "",
        registration_date: "",
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
