<script setup>
import {onMounted, reactive, ref} from "vue";
import router from "@/router/index.js";
import {isAuthenticated} from "@/composables/useAuth.js";
import axiosInstance from "@/services/axios.js";

const newRecipe = reactive({
  header: "",
  thumbnail_link: "",
  content_json: {
    text: "",
  },
  time_takes: "",
  difficulty: "",
  tags: [],
  ingredients: [],
});
const newTag = ref("");

const addIngredient = () => {
  newRecipe.ingredients.push({
    ingredient_name: "",
    quantity_si: 0,
    unit_si: "",
  });
};

const addTag = (tag) => {
  if (!newRecipe.tags.includes(tag)) {
    newRecipe.tags.push(tag);
  }
};


const submitRecipe = async () => {
  console.log(newRecipe);
  const response = await axiosInstance.post("/recipes/", newRecipe);
}


onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push('/');
  }
})
</script>

<template>
  <form @submit.prevent="submitRecipe">
    <div>
      <label for="header">Header:</label>
      <input id="header" v-model="newRecipe.header" type="text"/>
    </div>

    <div>
      <label for="thumbnail_link">Thumbnail Link:</label>
      <input id="thumbnail_link" v-model="newRecipe.thumbnail_link" type="url"/>
    </div>

    <div>
      <label for="time_takes">Time Takes:</label>
      <input id="time_takes" v-model="newRecipe.time_takes" type="text"/>
    </div>

    <div>
      <label for="difficulty">Difficulty:</label>
      <select id="difficulty" v-model="newRecipe.difficulty">
        <option value="Easy">Easy</option>
        <option value="Normal">Normal</option>
        <option value="Hard">Hard</option>
      </select>
    </div>

    <div>
      <h3>Ingredients</h3>
      <table>
        <thead>
        <tr>
          <th>Name</th>
          <th>Quantity</th>
          <th>Unit</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(ingredient, index) in newRecipe.ingredients" :key="index">
          <td><input v-model="ingredient.ingredient_name"/></td>
          <td><input v-model.number="ingredient.quantity_si" type="number"/></td>
          <td><select name="unit_si" v-model="ingredient.unit_si">
            <option label="liters">liters</option>
            <option label="grams">grams</option>
            <option label="units">units</option>
            <option label="pinches">pinches</option>
          </select></td>
          <td>
            <button type="button" @click="removeIngredient(index)">Remove</button>
          </td>
        </tr>
        </tbody>
      </table>
      <button type="button" @click="addIngredient">Add Ingredient</button>
    </div>

    <div>
      <h3>Tags</h3>
      <div>
        <span v-for="(tag, index) in newRecipe.tags" :key="index">
          {{ tag }}
          <button type="button" @click="removeTag(index)">x</button>
        </span>
      </div>
      <input v-model="newTag" @keyup.enter="addTag(newTag)" placeholder="Add tag"/>
    </div>

    <button type="submit">Save Recipe</button>
  </form>
</template>

<style scoped>

</style>