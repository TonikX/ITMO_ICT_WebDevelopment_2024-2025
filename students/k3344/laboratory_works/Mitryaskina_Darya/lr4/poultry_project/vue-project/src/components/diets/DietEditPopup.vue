<script setup>
import { ref, inject } from 'vue';
import { useStore } from 'vuex';
import PopupDefault from '../PopupDefault.vue';

const props = defineProps(['diet'])

const store = useStore();

const season = ref(props.diet.season);
const composition = ref(props.diet.composition);

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();  // Показывает модальное окно
  }
};

const save = async () => {
  try {
    await store.dispatch('DietStore/updateDiet',
    { id: props.diet.id,
      diet: {
        "season": season.value,
        "composition": composition.value,
    }});
  } catch (error) {
    console.error('Error creating diet:', error);
  }
  popup.value.close();
};

const cancel = () => {
  popup.value.close()
  season.value = props.diet.season
  composition.value = props.diet.composition
}

defineExpose({
  showModal
});
</script>

<template>
  <PopupDefault ref='popup' title="Update diet">
  <form @submit.prevent="save">
    <label>
      <span>Season:</span>
      <input type="text" v-model="season" required />
    </label>
    <label>
      <span>Composition:</span>
      <input type="text" v-model="composition" required />
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
