<template>
    <h1>All Assignments</h1>
    <hr class="h">
    <div v-for="assignment in Assignments" :key="assignment.id">
        <h3> {{ assignment.copy.book.name }}</h3>
        <h4>{{ assignment.reader.surname }} {{ assignment.reader.name }}</h4>
        <button @click="pushRouter(assignment.id)" class="btn">Full assignemnt information</button>
        <hr class="h">
    </div>
</template>

<script>
import api from '@/services/api'
import router from '@/router'
export default {
    data() {
        return {
            Assignments: [],
        }
    },
    methods: {
        pushRouter(id) {
            const url = '/assignments/' + id.toString();
            router.push(url);
        }
    },
    mounted () {
        api.get('/assignments/')
                .then(response => {
                    this.Assignments = response.data;
                })
                .catch(error => {
                    console.error(error);
                })
    }
}
</script>
<style scoped>

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
