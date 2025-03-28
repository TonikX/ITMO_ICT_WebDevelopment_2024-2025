<template>
  <div class="new-book_container">
    <h1>New Book</h1>
    <hr class="h">
    <form @submit="addNewBook">
      <label>Book name:</label><br>
      <input v-model="name" type="text" id="name" name="name"><br>

      <label>Author:</label><br>
      <input v-model="author" type="text" id="author" name="author"><br>

      <label>Publisher:</label><br>
      <input v-model="publisher" type="text" id="publisher" name="publisher"><br>

      <label>Publishing year:</label><br>
      <input v-model="publishingYear" type="date" id="publishingYear" name="publishingYear"><br>

      <label>Cipher:</label><br>
      <input v-model="cipher" type="text" id="cipher" name="cipher"><br>

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
      author: '',
      publisher: '',
      publishingYear: '',
      cipher: ''
    }
  },
  methods: {
    addNewBook(event) {
      event.preventDefault();
      const userData = {
        name: this.name,
        author: this.author,
        publisher: this.publisher,
        publishing_year: this.publishingYear,
        cipher: this.cipher
      }
      api.post('/books/new/', userData)
        .then(response => {
          this.$router.push('/books');
        })
        .catch(error => {
          console.log(userData);
          console.log(error);
          console.log('Something went wrong :(')
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

