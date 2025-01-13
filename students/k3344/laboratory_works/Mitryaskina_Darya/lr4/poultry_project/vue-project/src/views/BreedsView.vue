<script setup>
import BreedCard from '@/components/breeds/BreedCard.vue';
import BreedCreatePopup from '@/components/breeds/BreedCreatePopup.vue';
import Navigation from '@/components/Navigation.vue';
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const breeds = computed(() => store.state.BreedStore.breeds);

const fetchBreeds = async() => {
  try {
    store.dispatch('BreedStore/fetchBreeds');
  } catch (error) {
    console.error(error);
  }
}

onMounted(() => {
  fetchBreeds();
})
const createPopup = ref(null)
</script>

<template>
  <h1>Breeds</h1>
  <Navigation />
  <div class="header-container">
    <button class="add-button" @click="createPopup.showModal()">+ Add breed</button>
    <BreedCreatePopup ref="createPopup"/>
  </div>
  <ul class="list">
    <li v-for="breed in breeds" :key="breed.id">
      <BreedCard :breed="breed" />
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

