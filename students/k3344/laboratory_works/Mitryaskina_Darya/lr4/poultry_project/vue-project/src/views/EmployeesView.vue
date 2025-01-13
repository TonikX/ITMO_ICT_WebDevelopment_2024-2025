<script setup>
import Navigation from '@/components/Navigation.vue';
import EmployeeCreatePopup from '@/components/employees/EmployeeCreatePopup.vue';
import EmployeeCard from '@/components/employees/EmployeeCard.vue';
import { ref, provide, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const employees = computed(() => store.state.EmployeeStore.employees);

const fetchEmployees = async () => {
  try {
    await store.dispatch('EmployeeStore/fetchEmployees');
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
}

const fetchCages = async () => {
  if (cages.value.length !== 0) return

  try {
    await store.dispatch('CageStore/fetchCages');
  } catch (error) {
    console.error('Error fetching cages:', error);
  }
}

onMounted(() => {
  if (store.state.accessToken) {
    fetchEmployees();
    fetchCages();
  } else {
    console.error('Access token is missing');
  }
});
const createPopup = ref(null)
</script>


<template>
  <h1>Employees</h1>
  <Navigation />
  <div class="header-container">
    <button class="add-employee-button" @click="createPopup.showModal()">+ Add employee</button>
    <EmployeeCreatePopup ref="createPopup"/>
  </div>
  <ul class="employees-list">
    <li v-for="employee in employees" :key="employee.id">
      <EmployeeCard :employee="employee" />
    </li>
  </ul>
</template>


<style>
.employees-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  list-style: none;
  padding: 8px;
}

.header-container {
  display: flex;
  justify-content: flex-end;
  margin: 8px 0;
}

.add-employee-button {
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.add-employee-button:hover {
  background-color: #f9f9f9;
}
</style>

