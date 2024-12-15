<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const readingrooms = ref([])

function getReadingrooms(){
  instance.get('/library/reading-room/', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          readingrooms.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteReadingroom(id){
  instance.delete(`/library/reading-room/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 204){
          getReadingrooms()
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {getReadingrooms()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Читальные залы</h2>
    <template v-for="readingroom in readingrooms" :key="readingroom.id">
      <v-card
          width="600"
          :title="readingroom.name"
          :capacity="readingroom.capacity"
      ><v-card-actions>
        <v-btn @click="router.push('/readingrooms/' + readingroom.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteReadingroom(readingroom.id)">
          Удалить
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="router.push('/add-readingroom')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
