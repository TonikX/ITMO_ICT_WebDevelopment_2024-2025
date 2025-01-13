<script setup>
import CageCard from '@/components/cages/CageCard.vue';
import WorkshopEditPopup from './WorkshopEditPopup.vue';
import { ref, defineProps } from 'vue';

const editPopup = ref(null)

defineProps({
  workshop: Object,
  cages: Array
});
</script>

<template>
  <div class="workshop">
    <div class="header">
      <div>
        <h2>Workshop #{{ workshop.id }}</h2>
        <p>Info: {{ workshop.info }}</p>
        <p>Rows: {{ workshop.rows }}</p>
      </div>
      <div class="workshop-actions">
        <button @click='editPopup.showModal()' class="edit-workshop-button">Edit</button>
      </div>
    </div>
    <ul class="list">
      <li v-for="cage in cages" :key="cage.id">
        <CageCard :cage="cage" />
      </li>
    </ul>
  </div>
  <WorkshopEditPopup :workshop="workshop" ref="editPopup"/>
</template>

<style>

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  list-style: none;
  padding: 0;
}

.edit-workshop-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 16px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
}

.edit-workshop-button:hover {
  background-color: #0056b3;
}
</style>
