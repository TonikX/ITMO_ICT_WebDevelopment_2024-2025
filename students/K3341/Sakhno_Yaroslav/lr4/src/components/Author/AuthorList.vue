<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const authors = ref([])

function getAuthors(){
  instance.get('/library/author/', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          authors.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteAuthor(id){
  instance.delete(`/library/author/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 204){
          getAuthors()
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {getAuthors()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Авторы</h2>
    <template v-for="author in authors" :key="author.id">
      <v-card
          width="400"
          :title="author.full_name"
      ><v-card-actions>
        <v-btn @click="router.push('/authors/' + author.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteAuthor(author.id)">
          Удалить
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="router.push('/add-author')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
