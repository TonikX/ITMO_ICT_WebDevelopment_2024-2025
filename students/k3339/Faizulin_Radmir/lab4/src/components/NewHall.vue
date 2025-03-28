<template>
    <div class="new-hall_container">
        <h1>New Hall</h1>
        <hr class="h">
        <form @submit="addNewHall">
            <label>Hall name:</label><br>
            <input v-model="name" type="text" id="name"><br>

            <label>Sequence number:</label><br>
            <input v-model="sequenceNumber" type="number" id="sequenceNumber"><br>

            <label>Capacity:</label><br>
            <input v-model="capacity" type="number" id="capacity"><br>

            <button type="submit" class="btn">Submit</button>
        </form>
    </div>
</template>

<script>
import api from '@/services/api';
export default {
    data() {
        return {
            name: null,
            sequenceNumber: null,
            capacity: null
        }
    },
    methods: {
        addNewHall(event) {
          event.preventDefault();
            const userData = {
                name: this.name,
                sequence_number: this.sequenceNumber,
                capacity: this.capacity
            }
            api.post('/halls/new/', userData)
                .then(response => {
                    this.$router.push('/halls');
                })
                .catch(error => {
                    console.error(error);
                })
        }
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

