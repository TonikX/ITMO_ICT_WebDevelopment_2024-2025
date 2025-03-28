<template>
    <div class="new-copy_container">
        <h1>New Copy</h1>
        <hr class="h">
        <form @submit="addNewCopy">

            <label>Book:</label><br>
            <select v-model="book" id="book">
                <option v-for="book in books" :key="book.id" :value="book.id">{{ book.name }} {{ book.author }}</option>
            </select><br><br>

            <label>Hall:</label><br>
            <select v-model="hall" id="hall">
                <option v-for="hall in halls" :key="hall.id" :value="hall.id">{{ hall.sequence_number }}. {{ hall.name }}</option>
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
            books: [],
            halls: [],
            book: null,
            hall: null,
        }
    },
    methods: {
        addNewCopy(event) {
          event.preventDefault();
            const userData = {
                hall: this.hall,
                book: this.book,
            }
            api.post('/copies/new/', userData)
            .then(response => {
                this.$router.push('/copies');
            })
            .catch(error => {
                console.error(error);
            })
        }
    },
    mounted () {
        api.get('/books/')
        .then(response => {
            this.books = response.data;
        })
        .catch(error => {
            console.error(error);
        })
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
