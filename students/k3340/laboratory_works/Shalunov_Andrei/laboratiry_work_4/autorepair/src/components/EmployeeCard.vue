<template>
  <v-card>
    <v-card-title>{{ employee.full_name }}</v-card-title>
    <v-card-subtitle>{{ employee.email }}</v-card-subtitle>
    <v-card-text>
      <p>Job Position: {{ employee.job_position.name }}</p>
      <p>Workshop: {{ employee.car_workshop.city }}, {{ employee.car_workshop.address }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['employee'],
};
</script>
