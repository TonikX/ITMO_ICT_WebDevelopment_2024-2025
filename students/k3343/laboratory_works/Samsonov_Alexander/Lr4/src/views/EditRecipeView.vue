<script setup>
import {onMounted, ref} from "vue";
import {canEdit} from "@/composables/serverActions.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {isAuthenticated} from "@/composables/useAuth.js";
import axiosInstance from "@/services/axios.js";


const recipeId = useRoute().params.recipeId;
const recipeInfo = ref(null)
const errors = ref(null)

onMounted(async () => {
  if (! isAuthenticated.value ||!await canEdit(recipeId)) {
    router.push({path: '/', replace: true});
  }
  const response = await axiosInstance.get(`recipes/${recipeId}/`);
  let value = response.data;
  delete value.tags;
  delete value.author;
  recipeInfo.value = value;
})

const addIngredient = () => {
  recipeInfo.value.ingredients.push({
    ingredient_name: "",
    quantity_si: 0,
    unit_si: "",
  });
};

const removeIngredient = (index) => {
  recipeInfo.value.ingredients.splice(index, 1);
};

const submitRecipe = async () => {
  const response = axiosInstance.patch(`recipes/${recipeId}/`, recipeInfo.value )
  if (await response.success) {
    router.push({path: '/account', replace: true});
  }
  console.log(await response);
}

</script>

<template>
  <div class="container mt-4" v-if="recipeInfo">
    <!-- Recipe Header -->
    <div class="mb-3">
      <label for="recipe-header" class="form-label">Recipe Header</label>
      <input
          type="text"
          id="recipe-header"
          class="form-control"
          v-model="recipeInfo.header"
          placeholder="Enter the recipe header"
      />
    </div>

    <!-- Recipe Thumbnail -->
    <div class="mb-3">
      <label for="thumbnail-link" class="form-label">Thumbnail Link</label>
      <input
          type="url"
          id="thumbnail-link"
          class="form-control"
          v-model="recipeInfo.thumbnail_link"
          placeholder="Enter the image URL"
      />
    </div>

    <!-- Recipe Content -->
    <div class="mb-3">
      <label for="recipe-content" class="form-label">Content</label>
      <textarea
          id="recipe-content"
          class="form-control"
          rows="6"
          v-model="recipeInfo.content_json.text"
          placeholder="Enter the recipe content"
      ></textarea>
    </div>

    <!-- Time and Difficulty -->
    <div class="row mb-3">
      <div class="col">
        <label for="time-takes" class="form-label">Time Takes</label>
        <input
            type="time"
            id="time-takes"
            class="form-control"
            v-model="recipeInfo.time_takes"
        />
      </div>
      <div class="col">
        <label for="difficulty" class="form-label">Difficulty</label>
        <select id="difficulty" class="form-select" v-model="recipeInfo.difficulty">
          <option value="Easy">Easy</option>
          <option value="Normal">Normal</option>
          <option value="Hard">Hard</option>
        </select>
      </div>
    </div>

    <!-- Ingredients -->
    <div class="mb-4">
      <h5>Ingredients</h5>
      <table class="table table-bordered">
        <thead>
        <tr>
          <th>Ingredient Name</th>
          <th>Quantity (SI)</th>
          <th>Unit (SI)</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(ingredient, index) in recipeInfo.ingredients" :key="index">
          <td>
            <input
                type="text"
                class="form-control"
                v-model="ingredient.ingredient_name"
                placeholder="Ingredient Name"
            />
          </td>
          <td>
            <input
                type="number"
                class="form-control"
                v-model.number="ingredient.quantity_si"
                placeholder="Quantity"
            />
          </td>
          <td>
            <select name="unit_si" v-model="ingredient.unit_si">
              <option label="liters">liters</option>
              <option label="grams">grams</option>
              <option label="units">units</option>
              <option label="pinches">pinches</option>
            </select>
          </td>
          <td>
            <button class="btn btn-danger btn-sm" @click="removeIngredient(index)">
              -
            </button>
          </td>
        </tr>
        </tbody>
      </table>
      <button class="btn btn-success btn-sm" @click="addIngredient">+ Add Ingredient</button>
    </div>

    <button @click.prevent="submitRecipe" class="btn btn-primary">Submit</button>
  </div>
</template>



<style scoped>

</style>