<template>
  <div class="new-assignment_container">
    <h1>New Assignment</h1>
    <form @submit="addNewAssignment">

      <label>Reader:</label><br>
      <select v-model="reader" id="reader">
        <option v-for="reader in readers" :key="reader.id" :value="reader.id">{{ reader.name }}
          {{ reader.surname }}
        </option>
      </select><br><br>

      <label>Copy:</label><br>
      <select v-model="copy" id="copy">
        <option v-for="copy in copies" :key="copy.id" :value="copy.id">{{ copy.book.name }}
          {{ copy.book.author }}
        </option>
      </select><br><br>

      <label>Date Assigned:</label><br>
      <input v-model="dateAssigned" id="dateAssigned" type="date"><br>

      <label>Date Returned:</label><br>
      <input v-model="dateReturned" id="dateReturned" type="date"><br>

      <button type="submit" class="btn">Submit</button>
    </form>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      copies: [],
      readers: [],
      copy: null,
      reader: null,
      dateAssigned: null,
      dateReturned: null,
    }
  },
  methods: {
    addNewAssignment(event) {
      event.preventDefault();
      const userData = {
        reader: this.reader,
        copy: this.copy,
        date_assigned: this.dateAssigned,
        date_returned: this.dateReturned,
      }
      api.post('/assignments/new/', userData)
        .then(response => {
          this.$router.push('/assignments');
        })
        .catch(error => {
          console.error(error);
        })
    }
  },
  mounted() {
    api.get('/readers/')
      .then(response => {
        this.readers = response.data;
      })
      .catch(error => {
        console.error(error);
      })
    api.get('/copies/')
      .then(response => {
        this.copies = response.data;
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
