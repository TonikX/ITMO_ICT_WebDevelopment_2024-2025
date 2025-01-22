<template>
  <CustomHeader/>

  <router-view class="container"/>

  <CustomFooter/>
</template>

<script>
import CustomHeader from "@/components/navigation/CustomHeader.vue";
import CustomFooter from "@/components/navigation/CustomFooter.vue";

export default {
  name: 'App',
  components: {CustomFooter, CustomHeader},
};
</script>
