<template>
  <v-container class="page-wrapper">
    <v-row justify="center">
      <v-col cols="12" md="9" lg="8" xl="7">
        <slot></slot>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'PageWrapper'
}
</script>

<style scoped>
.page-wrapper {
  width: 100%;
  max-width: 100% !important;
  padding: 16px;
}
</style> 