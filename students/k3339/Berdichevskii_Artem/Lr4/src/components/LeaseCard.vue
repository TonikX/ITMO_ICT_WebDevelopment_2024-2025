<script setup>
import {computed} from 'vue';

const props = defineProps({
  leaseData: {
    type: Object,
    required: true,
  },
});
const leaseData = props.leaseData

const formattedStartDate = computed(() =>
    new Date(leaseData.dt_start).toLocaleDateString()
);
const formattedEndDate = computed(() =>
    new Date(leaseData.dt_end).toLocaleDateString()
);
</script>

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">{{ leaseData.rent_unit.address }}</h5>

      <p class="card-text">
        <strong>Cost:</strong> ${{ leaseData.rent_unit.cost }} / {{ leaseData.rent_unit.per_period }}
      </p>

      <p class="card-text">
        <strong>Area:</strong> {{ leaseData.rent_unit.area_sq_m }} sq.m
      </p>

      <p class="card-text">
        <strong>Lease Period:</strong> {{ formattedStartDate }} to {{ formattedEndDate }}
      </p>

      <p class="card-text">
        <strong>Status:</strong>
        <span
            class="badge"
            :class="leaseData.confirmed ? 'bg-success' : 'bg-warning text-dark'"
        >
          {{ leaseData.confirmed ? 'Confirmed' : 'Pending' }}
        </span>
      </p>
      <div class="row">
        <p class="card-link col">
          <router-link :to="`/tenant/history/${leaseData.id}/`">See details</router-link>
        </p>
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  max-width: 400px;
}
</style>
