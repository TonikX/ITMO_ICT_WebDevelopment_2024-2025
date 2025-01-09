<template>
  <v-card>
    <v-card-title>Contract #{{ contract.id }}</v-card-title>
    <v-card-text>
      <p><strong>Client:</strong> {{ contract.client.full_name }}</p>
      <p><strong>Automobile:</strong> {{ contract.auto.auto_model.car_brand }} {{ contract.auto.auto_model.model }}</p>
      <p><strong>Status:</strong> {{ contract.order_status }}</p>
      <p><strong>Payment:</strong> {{ contract.payment_status }}</p>
      <p><strong>Total Payment:</strong> ${{ contract.total_payment }}</p>
      <p><strong>Start Date:</strong> {{ contract.date_of_acceptance_for_repair }}</p>
      <p><strong>Scheduled End:</strong> {{ contract.scheduled_date_end_of_repair }}</p>
      <p><strong>Actual End:</strong> {{ contract.actual_date_end_of_repair }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ['contract'],
};
</script>
