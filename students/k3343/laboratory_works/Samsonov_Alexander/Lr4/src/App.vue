<template>
  <CustomHeader/>

  <router-view/>

  <CustomFooter/>
</template>

<script>
import CustomHeader from "@/components/CustomHeader.vue";
import CustomFooter from "@/components/CustomFooter.vue";

export default {
  name: 'App',
  components: {CustomFooter, CustomHeader},
};
</script>
