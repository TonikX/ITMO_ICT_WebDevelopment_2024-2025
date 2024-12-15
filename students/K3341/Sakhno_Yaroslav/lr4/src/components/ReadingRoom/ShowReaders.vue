<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/router";
import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()

const readers = ref([])

const form = ref({
  full_name: "",
})

function getPaper(){
  instance.get(`/library/reading-room/${router.currentRoute.value.params.id}/show_readers`, {
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

onMounted(() => {
  getPaper()
})


</script>
<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-for="reader in readers" :key="reader.id">
      <v-card
          width="600"
          :title="reader.full_name"
      ><v-card-actions>

      </v-card-actions></v-card>
    </template>
  </div>
</template>

<style scoped>

</style>
