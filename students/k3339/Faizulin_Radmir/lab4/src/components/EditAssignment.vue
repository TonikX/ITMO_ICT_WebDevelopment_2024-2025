<template>
    <div>
      <h1>Edit Assignment</h1>
      <hr class="h">
      <form @submit.prevent="submitForm">
        <label>Reader:</label><br>
        <select v-model="selectedReader">
            <option v-for="reader in Readers" :key="reader.id" :value="reader.id">
                {{ reader.name }} {{ reader.surname }}
            </option>
        </select><br><br>

        <label>Copy:</label><br>
        <select v-model="selectedCopy">
            <option v-for="copy in Copies" :key="copy.id" :value="copy.id">
                {{ copy.id }}. {{ copy.book.name }} by {{ copy.book.author }}
            </option>
        </select><br><br>

        <label for="dateAssigned">Date Assigned:</label><br>
        <input v-model="dateAssigned" type="date" id="dateAssigned" /><br><br>

        <label for="dateReturned">Date Returned:</label><br>
        <input v-model="dateReturned" type="date" id="dateReturned" /><br><br>

        <button type="submit" class="btn">Save changes</button>
      </form>
    </div>
  </template>

  <script>
  import api from '@/services/api';
  import router from '@/router';

  export default {
    data() {
        return {
            assignmentId: null,
            Readers: [],
            Copies: [],
            selectedReader: null,
            selectedCopy: null,
            dateAssigned: null,
            dateReturned: null,
        };
    },
    methods: {
        async fetchAssignment() {
            try {
                const assignmentId = this.$route.params.assignmentId;
                const url = '/assignments/' + assignmentId.toString() + '/';
                const response = await api.get(url);
                const assignment = response.data;
                console.log(response);
                this.selectedReader = assignment.reader.id;
                this.selectedCopy = assignment.copy.id;
                this.dateAssigned = assignment.date_assigned;
                this.dateReturned = assignment.date_returned;
            } catch (error) {
                console.error(error);
            }
        },
        submitForm() {
            const url = '/assignments/update/' + this.assignmentId.toString() + '/'

            const data = {
                reader: this.selectedReader,
                copy: this.selectedCopy,
                date_assigned: this.dateAssigned,
                date_returned: this.dateReturned,
            }
            console.log(data);
            api.patch(url, data)
            .then(response => {
                const to = '/assignments/' + this.assignmentId.toString();
                router.push(to);
            })
            .catch(error => {
                console.error(error);
            });
        },
    },
    mounted() {
        this.fetchAssignment();
        this.assignmentId = this.$route.params.assignmentId;
        api.get('/readers/')
        .then(response => {
            this.Readers = response.data;
        })
        .catch(error => {
            console.error(error);
        });
        api.get('/copies/')
        .then(response => {
            this.Copies = response.data;
        })
        .catch(error => {
            console.error(error);
        });
    },
  };
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
  background-color: black;
}
</style>

<style scoped>
  .h {
    width: 619px;
    margin: 10px 0px;
  }
</style>
