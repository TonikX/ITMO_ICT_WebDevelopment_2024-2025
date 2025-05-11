<script>
import { computed, ref, watch } from 'vue';

import { fetchWrapper } from '@/helpers';
import { useRouter } from "vue-router";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export default {
  setup: function () {
    const router = useRouter();

    const contractTypes = [
      { text: 'Индивидуальный', value: 'individual' },
      { text: 'Коллективный', value: 'collective' }
    ];

    const contract = ref({
      contract_type: '',
      start_date: '',
      end_date: '',
      insurance_cost: 0,
      organization_id: null,
      agent_id: null,
      employees_ids: []
    });
    const organizations = ref([]);
    const agents = ref([]);
    const employees = ref([]);

    const loadData = async () => {
      organizations.value = await fetchWrapper.get(`${baseUrl}/organizations/`);
      agents.value = await fetchWrapper.get(`${baseUrl}/agents/`);
      employees.value = await fetchWrapper.get(`${baseUrl}/employees/`);
    };

    const submitContract = async () => {
      console.log('Try to add:', contract.value);
      const response = await fetchWrapper.post(`${baseUrl}/contracts/`, contract.value);
      if (response.id) {
        await router.push(`/`);
      }
    };

    const filteredEmployees = computed(() => {
      if (!contract.value.organization_id) return [];

      return employees.value.filter(
        emp => emp.organization && emp.organization.id === contract.value.organization_id
      );
    });

    // Отслеживание изменений выбранной организации
    watch(() => contract.value.organization_id, () => {
      // Здесь можно сбросить выбранных сотрудников, если организация изменена
      contract.value.employees_ids = [];
    });

    loadData();

    return {contract, contractTypes, organizations, agents, filteredEmployees, submitContract};
  }
};
</script>

<template>
  <v-container>
    <v-form @submit.prevent="submitContract">
      <v-select
        v-model="contract.contract_type"
        :items="contractTypes"
        item-title="text"
        item-value="value"
        label="Contract Type"
      ></v-select>

      <v-text-field v-model="contract.start_date" label="Start Date" type="date"></v-text-field>
      <v-text-field v-model="contract.end_date" label="End Date" type="date"></v-text-field>
      <v-text-field v-model="contract.insurance_cost" label="Insurance Cost" type="number"></v-text-field>

      <v-select
        v-model="contract.organization_id"
        :items="organizations"
        item-title="short_name"
        item-value="id"
        label="Select Organization"
      ></v-select>

      <v-select
        v-model="contract.agent_id"
        :items="agents"
        item-title="full_name"
        item-value="id"
        label="Select Agent"
      ></v-select>

      <v-select
        v-model="contract.employees_ids"
        :items="filteredEmployees"
        item-title="full_name"
        item-value="id"
        label="Select Employees"
        multiple
      ></v-select>

      <v-btn type="submit" color="primary">Create Contract</v-btn>
    </v-form>
  </v-container>
</template>

<style scoped>

</style>
