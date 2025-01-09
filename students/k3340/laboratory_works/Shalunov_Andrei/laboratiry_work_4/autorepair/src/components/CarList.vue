<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6" lg="4" v-for="car in cars" :key="car.id" class="mb-3">
        <v-card>
          <v-card-title>{{ car.auto_model.car_brand }} {{ car.auto_model.model }}</v-card-title>
          <v-card-subtitle>{{ car.colour }} - {{ car.state_number }}</v-card-subtitle>
          <v-card-text>
            <p>Year: {{ car.year_of_vehicle }}</p>
            <p>Client: {{ car.client.full_name }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: ['cars'],
};
</script>
