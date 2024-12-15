<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const categories = ref([])

function getCategories(){
  instance.get('/library/category/', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          categories.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteCategory(id){
  instance.delete(`/library/category/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 204){
          getCategories()
        }
      }
  ).catch(error => console.log(error))
}

onMounted(() => {getCategories()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Категории</h2>
    <template v-for="category in categories" :key="category.id">
      <v-card
          width="400"
          :title="category.category_name"
      ><v-card-actions>
        <v-btn @click="router.push('/categories/' + category.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteCategory(category.id)">
          Удалить
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="router.push('/add-category')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
