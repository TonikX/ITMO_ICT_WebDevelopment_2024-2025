<script setup>
import HenCard from '@/components/hens/HenCard.vue';
import HenCreatePopup from '@/components/hens/HenCreatePopup.vue';
import Navigation from '@/components/Navigation.vue';
import { ref, onMounted, provide, computed } from 'vue';
import { mapState, useStore } from 'vuex';
import getAPI from '../axios-api.js';

const store = useStore();

const createPopup = ref(null);
const hens = computed(() => store.state.HenStore.hens);

const fetchHens = async () => {
  try {
    await store.dispatch('HenStore/fetchHens');
  } catch (error) {
    console.error('Error fetching hens:', error);
  }
};

onMounted(() => {
  if (store.state.accessToken) {
    fetchHens();
  } else {
    console.error('Access token is missing');
  }
});
</script>

<template>
  <h1>Hens</h1>
  <Navigation />
  <div class="header-container">
    <button class="add-hen-button" @click="createPopup.showModal()">+ Add hen</button>
    <HenCreatePopup ref="createPopup"/>
  </div>
  <ul class="hens-list">
    <li v-for="hen in hens" :key="hen.id">
      <HenCard :hen="hen" />
    </li>
  </ul>
</template>

<style>
.hens-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  list-style: none;
  padding: 8px;
}

.header-container {
  display: flex;
  justify-content: flex-end;
  margin: 8px 0;
}

.add-hen-button {
  background-color: white;
  color: black;
  border: 1px solid #ccc;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.add-hen-button:hover {
  background-color: #f9f9f9;
}
</style>
