<template>
  <div class="new-reader_container">
    <h1>New Reader</h1>
    <hr class="h">
    <form @submit="addNewReader">
      <label>Name:</label><br>
      <input v-model="name" type="text" id="name" name="name"><br>

      <label>Second Name:</label><br>
      <input v-model="secondName" type="text" id="second_name" name="second_name"><br>

      <label>Surname:</label><br>
      <input v-model="surname" type="text" id="surname" name="surname"><br>

      <label>Passport:</label><br>
      <input v-model="passport" type="text" id="passport" name="passport"><br>

      <label>Birth date:</label><br>
      <input v-model="birthDate" type="date" id="birth_date" name="birth_date"><br>

      <label>Address:</label><br>
      <input v-model="address" type="text" id="address" name="address"><br>

      <label>Phone number:</label><br>
      <input v-model="phoneNumber" type="text" id="phone_number" name="phone_number"><br>

      <label>Education:</label><br>
      <select v-model="education" id="phone_number">
        <option value="0">No education</option>
        <option value="1">Elementary</option>
        <option value="2">Middle</option>
        <option value="3">Bachelor</option>
        <option value="4">Master</option>
      </select><br><br>

      <label>PhD</label>
      <input v-model="ifPhd" type="checkbox" id="if_phd"><br>

      <label>Hall:</label><br>
      <select v-model="hall" id="hall">
        <option v-for="hall in halls" :key="hall.id" :value="hall.id">{{ hall.name }}</option>
      </select><br><br>

      <button type="submit" class="btn">Submit</button>
    </form>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      name: '',
      secondName: '',
      surname: '',
      passport: '',
      birthDate: '',
      address: '',
      phoneNumber: '',
      education: '0',
      ifPhd: false,
      hall: '',
      cardNumber: '',
      halls: [],
    }
  },
  methods: {
    addNewReader(event) {
      event.preventDefault();
      const userData = {
        name: this.name,
        second_name: this.secondName,
        surname: this.surname,
        passport: this.passport,
        birth_date: this.birthDate,
        address: this.address,
        phone_number: this.phoneNumber,
        education: this.education,
        phd: this.ifPhd,
        hall: this.hall,
        library_card_number: this.phoneNumber,
      }
      api.post('/readers/new/', userData)
        .catch(error => {
          console.error(error);
        })
    }
  },
  mounted() {
    api.get('/halls/')
      .then(response => {
        this.halls = response.data;
      })
      .catch(error => {
        console.error(error);
      })
  }
}
</script>
<style scoped>
input {
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  color: #fff;
  background-color: red;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: black; /* Цвет фона кнопки при наведении */
}
</style>

<style scoped>
.h {
  width: 619px;
  margin: 10px 0px;
}
</style>
