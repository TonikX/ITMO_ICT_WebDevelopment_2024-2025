<script setup>
import DietCard from '@/components/diets/DietCard.vue';
import DietCreatePopup from '@/components/diets/DietCreatePopup.vue';
import Navigation from '@/components/Navigation.vue';
import { useStore } from 'vuex';
import { ref, computed, onMounted } from 'vue';

const store = useStore();
const diets = computed(() => store.state.DietStore.diets);

const fetchDiets = async () => {
  try {
    await store.dispatch('DietStore/fetchDiets');
  } catch (error) {
    console.error('Error fetching diets:', error);
  }
};

onMounted(() => {
  fetchDiets();
});
const createPopup = ref(null)
</script>


<template>
  <h1>Diets</h1>
  <Navigation />
  <div class="header-container">
    <button class="add-button" @click="createPopup.showModal()">+ Add diet</button>
    <DietCreatePopup ref="createPopup"/>
  </div>
  <ul class="list">
    <li v-for="diet in diets" :key="diet.id">
      <DietCard :diet="diet" />
    </li>
  </ul>
</template>

<style scoped>
.list {
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

.add-button {
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.add-button:hover {
  background-color: #f9f9f9;
}
</style>
