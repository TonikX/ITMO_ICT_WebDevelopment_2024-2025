<script setup>
import { ref, computed } from 'vue';
import PopupDefault from '../PopupDefault.vue';
import { useStore } from 'vuex';

const store = useStore()
const props = defineProps(['cage'])

const workshops = computed(() => store.state.WorkshopStore.workshops);

const workshop = ref(props.cage.workshop.id);
const row_number = ref(props.cage.row_number);
const cage_number = ref(props.cage.cage_number);

const popup = ref(null);

const showModal = () => {
  if (popup.value) {
    popup.value.showModal();
  }
};

const save = async () => {
  try {
    store.dispatch('CageStore/updateCage', {
      id: props.cage.id,
      cage:
        {
          "workshop": workshop.value,
        "row_number": row_number.value,
        "cage_number": cage_number.value,
        }
     });
  } catch (error) {
    console.error('Error updating cage:', error);
  }
  popup.value.close();
};

const cancel = () => {
  popup.value.close()
  workshop.value = null
  row_number.value = null
  cage_number.value = null
}

defineExpose({
  showModal
});
</script>


<template>
  <PopupDefault ref='popup' title="Add cage">
  <form @submit.prevent="save">
    <label>
      <span>Workshop:</span>
      <select v-model="workshop" required>
        <option v-for='workshop in workshops' :value="workshop.id">{{ `Workshop ${workshop.id}` }}</option>
      </select>
    </label>
    <label>
      <span>Row:</span>
      <input type="number" v-model="row_number" required />
    </label>
    <label>
      <span>Cage:</span>
      <input type='number' v-model="cage_number" required />
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
  appearance: none;
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
  font-size: 0.8rem;
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
