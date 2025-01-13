<script setup>
import { ref, computed } from 'vue';
import PopupDefault from '../PopupDefault.vue';
import { useStore } from 'vuex';


const store = useStore();

const diets = computed(() => store.state.DietStore.diets);

const props = defineProps(['breed'])

const name = ref(props.breed.name);
const avgEggsPerMonth = ref(props.breed.avg_eggs_per_month);
const avgWeight = ref(props.breed.avg_weight);
const diet = ref(props.breed.diet.id);

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();  // Показывает модальное окно
  }
};

const save = async () => {
  try {
    store.dispatch('BreedStore/updateBreed', {
      "id": props.breed.id,
      breed: {
        "name": name.value,
        "avg_eggs_per_month": avgEggsPerMonth.value,
        "avg_weight": avgWeight.value,
        "diet": diet.value
      }
    })
  } catch (error) {
    console.error(error);
  }

  popup.value.close();
};

const cancel = () => {
  popup.value.close()
}

defineExpose({
  showModal
});
</script>

<template>
  <PopupDefault ref='popup' title="Create breed">
  <form @submit.prevent="save">
    <label>
      <span>Name:</span>
      <input type="text" v-model="name" required />
    </label>
    <label>
      <span>Eggs/month average:</span>
      <input type="number" v-model="avgEggsPerMonth" required />
    </label>
    <label>
      <span>Weight average:</span>
      <input type="number" v-model="avgWeight" required />
    </label>
    <label>
      <span>Diet:</span>
      <select v-model="diet" required>
        <option v-for='diet in diets' :value="diet.id">{{ `${diet.composition} (${diet.season})` }}</option>
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
  /* background-color: #fff; */
  /* color: #333; */
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
