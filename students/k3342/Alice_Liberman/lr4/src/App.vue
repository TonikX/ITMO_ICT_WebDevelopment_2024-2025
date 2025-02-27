<template>
  <CustomHeader/>

  <router-view class="container"/>

  <CustomFooter/>
</template>

<script setup>
import CustomFooter from "@/components/CustomFooter.vue";
import CustomHeader from "@/components/CustomHeader.vue";
import {update} from "@/stores/globalState.js";

update()
</script>
