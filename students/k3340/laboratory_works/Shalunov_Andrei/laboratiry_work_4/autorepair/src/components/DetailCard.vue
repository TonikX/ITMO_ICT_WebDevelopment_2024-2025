<template>
  <v-card>
    <v-card-title>{{ detail.name }}</v-card-title>
    <v-card-text>
      <p><strong>Price:</strong> ${{ detail.price }}</p>
      <p><strong>Country of Manufacturer:</strong> {{ detail.country_of_manufacturer }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['detail'],
};
</script>
