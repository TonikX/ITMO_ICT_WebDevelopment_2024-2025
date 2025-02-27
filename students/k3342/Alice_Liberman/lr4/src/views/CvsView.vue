<template>
  <div class="container">
    <h1>Manage your CV's</h1>
    <div class="row" v-if="cvS" >
      <CVList v-for="cv in cvS" :key="cv.id" :cv="cv" class="col-4"/>
    </div>
    <CvsCreate @success="updateCvs"/>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import CVList from "@/components/CVList.vue";
import CvsCreate from "@/components/CvsCreate.vue";

const cvS = ref(null)
async function updateCvs() {
  cvS.value = (await axiosInstance.get('/cvs')).data
}

onMounted(async () => {
  updateCvs()
})
</script>