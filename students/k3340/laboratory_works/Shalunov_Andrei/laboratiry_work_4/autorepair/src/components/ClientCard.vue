<template>
  <v-card>
    <v-card-title>{{ client.full_name }}</v-card-title>
    <v-card-subtitle>{{ client.email }}</v-card-subtitle>
    <v-card-text>{{ client.phone }}</v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['client'],
};
</script>
