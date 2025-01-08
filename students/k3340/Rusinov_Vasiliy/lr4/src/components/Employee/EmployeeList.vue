<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import {Api} from "@/services/api";

const Token = Api()
const  bookcopys = ref([])

function getBooks(){
  instance.get('/library/book-copy/', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          bookcopys.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteBook(id){
  instance.delete(`/library/book-copy/${id}/`, {
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
    <h2>Экземпляры книг</h2>
    <template v-for="bookcopy in bookcopys" :key="bookcopy.id">
      <v-card
          width="400"
          :title="bookcopy.book.name"
          :subtitle="bookcopy.cipher"
          :text = "bookcopy.publishing_year"
      ><v-card-actions>
        <v-btn @click="index.push('/book-copies/' + bookcopy.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteBook(bookcopy.id)">
          Удалить
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="index.push('/add-book-copy')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
