<script setup>
import { ref, inject } from 'vue';
import { useStore } from 'vuex';
import PopupDefault from '../PopupDefault.vue';

const props = defineProps(['hen'])

const store = useStore();
store.dispatch('BreedStore/fetchBreeds');
store.dispatch('CageStore/fetchCages');

const weight = ref(props.hen.weight);
const age = ref(props.hen.age);
const eggsPerMonth = ref(props.hen.eggs_per_month);
const breed = ref(props.hen.breed.id);
const cage = ref(props.hen.cage?.id);

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();  // Показывает модальное окно
  }
};

const save = async () => {
  store.dispatch('HenStore/updateHen', { id: props.hen.id, hen: {
      "weight": weight.value,
      "age": age.value,
      "eggs_per_month": eggsPerMonth.value,
      "breed": breed.value,
      "cage": cage.value
    } })
  popup.value.close();
}

const cancel = () => {
  popup.value.close()
  weight.value = props.hen.weight
  age.value = props.hen.age;
  eggsPerMonth.value = props.hen.eggs_per_month;
  breed.value = props.hen.breed.name;
  cage.value = props.hen.cage.id;
}


defineExpose({
  showModal
});
</script>

<template>
  <PopupDefault ref='popup' title="Edit hen">
  <form @submit.prevent="save">
    <label>
      <span>Weight (kg):</span>
      <input type="number" v-model="weight" required />
    </label>
    <label>
      <span>Age (years):</span>
      <input type="number" v-model="age" required />
    </label>
    <label>
      <span>Eggs per month:</span>
      <input type="number" v-model="eggsPerMonth" required />
    </label>
    <label>
      <span>Breed:</span>
      <select v-model="breed" required>
        <option v-for="breed in store.state.BreedStore.breeds" :value="breed.id">{{ breed.name }}</option>
      </select>
    </label>
    <label>
      <span>Cage:</span>
      <select v-model="cage" required>
        <option v-for="cage in store.state.CageStore.cages" :value="cage.id">{{ `Cage ${cage.cage_number} in row ${cage.row_number} workshop ${cage.workshop.id}` }}</option>
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
