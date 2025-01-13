<script setup>
import { computed, inject, ref } from 'vue';
import EmployeeEditPopup from './EmployeeEditPopup.vue';
import DeletePopup from '../DeletePopup.vue';
import { useStore } from 'vuex';

const store = useStore();


const props = defineProps(['employee'])
const editPopup = ref(null)
const deletePopup = ref(null)

const displayedName = computed(() => {
  if (props.employee.name) {
    return props.employee.name
  } else {
    return `Employee ${props.employee.id}`
  }
})

const deleteEmployee = async (id) => {
  try {
    await store.dispatch('EmployeeStore/deleteEmployee', props.employee.id);
  } catch (error) {
    console.error('Error deleting Employee:', error);
  }
}
</script>


<template>
  <div class="employee-card">
    <!-- Название -->
    <div class="employee-title-block">
      <span class="employee-title">{{ displayedName }}</span>
    </div>

    <!-- Атрибуты -->
    <div class="attributes-block">
      <div class="attribute">
        <span class="attribute-name">Passport:</span>
        <span class="attribute-value">{{ employee.passport }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Salary:</span>
        <span class="attribute-value">${{ employee.salary }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Contract:</span>
        <span class="attribute-value">{{ employee.contract }}</span>
      </div>
      <div class="attribute">
        <span class="attribute-name">Termination:</span>
        <span class="attribute-value">{{ employee.termination }}</span>
      </div>
      <!-- <div class="attribute">
        <span class="attribute-name">Assigned cages:</span>
        <span class="attribute-value">#{{ employee.assigned_cages }}</span>
      </div> -->
      <div class="attribute">
        <span class="attribute-name">Assigned cages:</span>
        <ul class="attribute-value">
          <li v-for="cage in employee.assigned_cages" :key="cage.id">
            Cage {{ cage.cage_number }} in row {{ cage.row_number }} workshop {{ cage.workshop.id }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Кнопки -->
    <div class="actions">
      <button @click="editPopup.showModal()" type="button" class="edit-btn">Edit</button>
      <button @click="deletePopup.showModal()" type="button" class="delete-btn">Delete</button>
    </div>
  </div>
  <EmployeeEditPopup :employee="employee" ref="editPopup"/>
  <DeletePopup @delete="deleteEmployee" :title="`Delete employee #${employee.id}`" ref="deletePopup"/>
</template>



<style scoped>
.employee-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 24px;
  padding: 16px;
  height: 100%;
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.employee-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.employee-title-block {
  margin-bottom: 8px;
}

.employee-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-text);
}

.attributes-block {
  flex-grow: 1; /* Заставляет этот блок занимать все оставшееся пространство */
}

.attribute {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
  color: #555;
}

.attribute-name {
  font-weight: 500;
  color: #777;
}

.attribute-value {
  color: hsla(160, 100%, 37%, 1); /* Зеленый цвет для значений */
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: auto; /* Прижимает блок с кнопками к низу */
}

button {
  padding: 8px 12px;
  font-size: 0.9rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}

button:focus {
  outline: none;
}

.edit-btn {
  background: hsla(160, 100%, 37%, 1);
  color: #fff;
}

.edit-btn:hover {
  background: rgb(5, 165, 112);
}

.delete-btn {
  background: #f44336;
  color: #fff;
}

.delete-btn:hover {
  background: #e53935;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  color: hsla(160, 100%, 37%, 1); /* Зеленый цвет для значений */
  font-size: 0.95rem;
}
</style>
