<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
const  readers = ref([])


function getReaders(){
  instance.get('/library/reader/youngest', {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 200){
          readers.value = response.data
        }
      }
  ).catch(error => console.log(error))
}

function deleteReader(id){
  instance.delete(`/library/reader/${id}/`, {
    headers: {
      'Authorization': `Token ${Token.token}`
    }
  }).then(response => {
        if (response.status === 204){
          getReaders()
        }
      }
  ).catch(error => console.log(error))
}


function buf(){
  getReaders()
}
onMounted(() => {buf()})

</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h2>Читатели</h2>
    <template v-for="reader in readers" :key="reader.id">
      <v-card
          width="400"
          :title="reader.full_name"
          :subtitle="reader.reading_room.name"
          :text = "`Пасспорт ${reader.passport},
          Номер телефона ${reader.phone_number},
          Дата рождения ${reader.birth_date},
          Дата регитсрации${reader.registration_date},`"
      ><v-card-actions>
        <v-btn @click="router.push('/readers/' + reader.id)">
          Изменить
        </v-btn>
        <v-btn @click="deleteReader(reader.id)">
          Удалить
        </v-btn>
        <v-btn @click="router.push('/readers/' + reader.id + '/show-books-taken')">
          Прочитанное
        </v-btn>
      </v-card-actions></v-card>
    </template>
    <v-btn @click="router.push('/add-reader')">Добавить</v-btn>
  </div>
</template>

<style scoped>
</style>
