<template>
  <CustomHeader/>

  <router-view/>

  <CustomFooter/>
</template>

<script>
import CustomHeader from "@/components/genericInterface/CustomHeader.vue";
import CustomFooter from "@/components/genericInterface/CustomFooter.vue";

export default {
  name: 'App',
  components: {CustomFooter, CustomHeader},
};
</script>
