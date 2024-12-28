<script setup>
import {ref} from "vue";

const props = defineProps(["recipeInfo"])
const ingredientsRaw = ref(props.recipeInfo.ingredients)
</script>

<template>
  <table class="table table-striped table-hover table-bordered">
    <thead class="table-dark">
    <tr>
      <th>Ingredient</th>
      <th>Quantity</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(ingredient, index) in ingredientsRaw" :key="index">
      <td>{{ ingredient.ingredient_name }}</td>
      <td>{{ ingredient.quantity_si + ' ' + ingredient.unit_si }}</td>
    </tr>
    </tbody>
  </table>
</template>

<style scoped>

</style>