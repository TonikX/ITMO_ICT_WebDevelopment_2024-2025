<script setup>
import { reactive, ref, inject } from 'vue';
import PopupDefault from '../PopupDefault.vue';
import { useStore } from 'vuex';

const store = useStore();

const props = defineProps(['employee'])


const assignedCages = ref(props.employee.assigned_cages.map(cage => cage.id));
const name = ref(props.employee.name)
const passport = ref(props.employee.passport);
const salary = ref(props.employee.salary);
const contract = ref(props.employee.contract);
const termination = ref(props.employee.termination);

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();
  }
};

const save = async () => {
  store.dispatch('EmployeeStore/updateEmployee', { id: props.employee.id, employee: {
    "assigned_cages": assignedCages.value,
    "passport": passport.value,
    "name": name.value,
    "salary": salary.value,
    "contract": contract.value,
    "termination": termination.value,
  }})
  popup.value.close();
};

const cancel = () => {
  popup.value.close()
  assignedCages.value = props.employee.assigned_cages
  passport.value = props.employee.passport
  salary.value = props.employee.salary
  contract.value = props.employee.contract
  termination.value = props.employee.termination
}

defineExpose({
  showModal
});
</script>


<template>
  <PopupDefault ref='popup' title="Update employee">
  <form @submit.prevent="save">
    <label>
      <span>Name:</span>
      <input type="text" v-model="name" required />
    </label>
    <label>
      <span>Passport:</span>
      <input type="text" v-model="passport" required />
    </label>
    <label>
      <span>Salary:</span>
      <input type="number" v-model="salary" required />
    </label>
    <label>
      <span>Contract:</span>
      <input type="text" v-model="contract" required />
    </label>
    <label>
      <span>Termination:</span>
      <input type='text' v-model="termination" />
    </label>
    <label>
      <span>Assigned cages:</span>
      <select multiple v-model="assignedCages">
        <option v-for='cage in store.state.CageStore.cages' :value="cage.id">{{ `Cage ${cage.cage_number} in row ${cage.row_number} workshop ${cage.workshop.id}` }}</option>
      </select>
    </label>
    <div class="form-actions">
      <button type="submit" class="save-btn">Save</button>
      <button type="button" @click="cancel" class="cancel-btn">Cancel</button>
    </div>
  </form>
  </PopupDefault>
</template>


<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  color: #555;
}

input {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-top: 8px;
  width: 100%;
}

input:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

select {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #fff;
  color: #333;
  width: 100%;
  cursor: pointer;
  -webkit-appearance: none; /* Для удаления стандартных стрелок в Safari */
  -moz-appearance: none;    /* Для Firefox */
  appearance: none;         /* Для всех современных браузеров */
}

select:focus {
  outline: none;
  border-color: hsla(160, 100%, 37%, 1);
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

option {
  padding: 8px;
  background-color: #fff;
  color: #333;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

button {
  padding: 10px 16px;
  font-size: 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:focus {
  outline: none;
}

.save-btn {
  background: hsla(160, 100%, 37%, 1);
  color: #fff;
  border: none;
}

.save-btn:hover {
  background: rgb(5, 165, 112);
}

.cancel-btn {
  background: #f44336;
  color: #fff;
  border: none;
}

.cancel-btn:hover {
  background: #e53935;
}
</style>

