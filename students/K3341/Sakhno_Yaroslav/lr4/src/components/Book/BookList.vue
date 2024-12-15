<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const  books = ref([])

function getBooks(){
  instance.get('/library/book/', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          books.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteBook(id){
  instance.delete(`/library/book/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 204){
          getBooks()
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {getBooks()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Книги</h2>

    <template v-for="book in books" :key="book.id">
      <v-card
          width="400"
          :title="book.name"
          :subtitle="book.publisher"
          :text = "`Категория ${book.category}, Автор ${book.authors}`"
      ><v-card-actions>
        <v-btn @click="router.push('/books/' + book.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteBook(book.id)">
          Удалить
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="router.push('/add-book')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
