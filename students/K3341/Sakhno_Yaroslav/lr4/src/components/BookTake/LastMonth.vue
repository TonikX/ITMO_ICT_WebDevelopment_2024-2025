<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const  booktakes = ref([])

function getBooktakes(){
  instance.get('/library/book-taken/take_last_month', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          booktakes.value = response.data
        }
      }
  ).catch(error => console.log(error))
}


onMounted(() => {getBooktakes()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Книги, взятые более месяца назад</h2>
    <template v-for="booktake in booktakes" :key="booktake.id">
      <v-card
          width="400"
          :title="`${booktake.book_copy} взята ${booktake.reader}`"
          :text = "`${booktake.take_date} - ${booktake.return_date}`"
      ></v-card>
    </template>
  </div>
</template>

<style scoped>
</style>
