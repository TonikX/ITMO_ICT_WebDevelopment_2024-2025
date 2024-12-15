<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const form = ref({
  category_name: "",
})

function getPaper(){
  instance.get(`/library/category/${router.currentRoute.value.params.id}/`, {
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
  instance.patch(`/library/category/${router.currentRoute.value.params.id}/`, rest, {
    headers: {
    'Authorization': `Token ${Token.token}`
  }
}).then(response => {
        if (response.status === 200){
          router.push('/categories')
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
      <h2>Категория</h2>
      <v-text-field label="Имя" v-model="form.category_name"></v-text-field>
      <v-btn @click="savePaper">Сохранить</v-btn>
    </div>
  </v-app>
</template>

<style scoped>

</style>
