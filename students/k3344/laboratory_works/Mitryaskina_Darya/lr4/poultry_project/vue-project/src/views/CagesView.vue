<script setup>
import Navigation from '@/components/Navigation.vue';
import CageCard from '@/components/cages/CageCard.vue';
import WorkshopCard from '@/components/cages/WorkshopCard.vue';
import CageCreatePopup from '@/components/cages/CageCreatePopup.vue';
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const workshops = computed(() => store.state.WorkshopStore.workshops);
const cages = computed(() => store.state.CageStore.cages);

const fetchWorkshops = async () => {
  try {
    await store.dispatch('WorkshopStore/fetchWorkshops');
  } catch (error) {
    console.error(error);
  }
}

const fetchCages = async () => {
  if (cages.value.length !== 0) return

  try {
    await store.dispatch('CageStore/fetchCages');
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  fetchCages();
  fetchWorkshops();
})


const createCagePopup = ref(null)
</script>

<template>
  <h1>Workshops and cages</h1>
  <Navigation />
  <div class="header-container">
    <button class="add-button" @click="createCagePopup.showModal()">+ Add cage</button>
  </div>
  <CageCreatePopup ref="createCagePopup"/>
  <div class="container">
    <WorkshopCard
      v-for="workshop in workshops"
      :key="workshop.id"
      :workshop="workshop"
      :cages="cages.filter(c => c.workshop.id === workshop.id)"
    />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

p {
  margin: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.header-container {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  list-style: none;
  padding: 0;
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
  background-color: #e6e6e6;
}

.edit-workshop-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 16px;
  margin: 0 10px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.edit-workshop-button:hover {
  background-color: #0056b3;
}
</style>

