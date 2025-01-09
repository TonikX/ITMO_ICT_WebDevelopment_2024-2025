<template>
  <v-card>
    <v-card-title>{{ service.type_of_repair }}</v-card-title>
    <v-card-text>
      <p><strong>Category:</strong> {{ service.category_repair }}</p>
      <p><strong>Price:</strong> ${{ service.price }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['service'],
};
</script>
