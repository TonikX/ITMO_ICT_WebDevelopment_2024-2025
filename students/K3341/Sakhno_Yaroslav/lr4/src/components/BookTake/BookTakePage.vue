<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  book_copy: "",
  reader: "",
  take_date: "",
  return_date : "",

})

function getPaper(){
  instance.get(`/library/book-taken/${router.currentRoute.value.params.id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          form.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function savePaper(){
  const {id, ...rest} = form.value
  instance.patch(`/library/book-taken/${router.currentRoute.value.params.id}/`, rest, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          router.push('/book-takes')
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {
  getPaper()
})

</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Взятая книга</h2>
      <v-text-field label="Экземпляр книги" v-model="form.book_copy"></v-text-field>
      <v-text-field label="Читатель" v-model="form.reader"></v-text-field>
      <v-text-field label="Дата получения" v-model="form.take_date"></v-text-field>
      <v-text-field label="Дата возврата" v-model="form.return_date"></v-text-field>
      <v-btn @click="savePaper">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
