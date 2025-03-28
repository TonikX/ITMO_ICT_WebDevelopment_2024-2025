<template>
    <div v-if="assignment">
        <h1>Assignment Details</h1>
        <hr class="h">
        <h3>{{ assignment.copy.book.name }} {{ assignment.copy.book.author }}</h3>
        <h4>Taken by: {{ assignment.reader.name }} {{ assignment.reader.surname }}</h4>
        <p>Assigned: {{ assignment.date_assigned }}</p>
        <p v-if="assignment.date_returned">Returned: {{ assignment.date_returned }}</p>
        <p v-else>not returned yet</p>

        <button class="btn"><router-link :to="{name: 'EditAssignment', params: { assignmentId: $assignmentId } }">Edit</router-link></button><br><br>

        <router-link to="/assignments">Go back</router-link>
    </div>
    <p v-else>Loading ...</p>
</template>

<script>
import api from '@/services/api'
export default {
    data() {
        return {
            assignment: null,
            assignmentId: null,
        }
    },
    mounted() {
        this.assignmentId = this.$route.params.assignmentId;
        const url = '/assignments/' + this.assignmentId.toString() + '/';

        api.get(url)
        .then(response => {
            this.assignment = response.data;
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
    width: 619px; /* Установка ширины линии на 50% ширины родительского контейнера */
    margin: 10px 0px; /* Центрирование линии по горизонтали */
  }
</style>
