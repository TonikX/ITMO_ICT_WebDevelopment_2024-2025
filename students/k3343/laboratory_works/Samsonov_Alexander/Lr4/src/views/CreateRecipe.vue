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

const removeIngredient = (index) => {
  newRecipe.ingredients.splice(index, 1);
};

const addTag = (tag) => {
  if (tag.trim() && !newRecipe.tags.includes(tag)) {
    newRecipe.tags.push(tag.trim());
    newTag.value = "";
  }
};

const removeTag = (index) => {
  newRecipe.tags.splice(index, 1);
};

const submitRecipe = async () => {
  console.log("creating new recipe...");
  const response = await axiosInstance.post("/recipes/", newRecipe);
  if (response.status === 200) {
    setTimeout(router.push({path: "/recipe", replace: true}), 300)
  }
};

onMounted(async () => {
  if (!isAuthenticated.value) {
    router.push({path: "/", replace: true})
  }
});
</script>

<template>
  <form class="container mt-4">
    <div class="form-group mb-3">
      <label for="header">Header:</label>
      <input id="header" v-model="newRecipe.header" type="text" class="form-control"/>
    </div>

    <div class="form-group mb-3">
      <label for="thumbnail_link">Thumbnail Link:</label>
      <input id="thumbnail_link" v-model="newRecipe.thumbnail_link" type="url" class="form-control"/>
    </div>

    <div class="form-group mb-3">
      <label for="time_takes">Time Takes:</label>
      <input id="time_takes" v-model="newRecipe.time_takes" type="text" class="form-control"/>
    </div>

    <div class="form-group mb-3">
      <label for="difficulty">Difficulty:</label>
      <select id="difficulty" v-model="newRecipe.difficulty" class="form-select">
        <option value="Easy">Easy</option>
        <option value="Normal">Normal</option>
        <option value="Hard">Hard</option>
      </select>
    </div>

    <div class="form-group mb-3">
      <label for="content_text">Content:</label>
      <textarea id="content_text" v-model="newRecipe.content_json.text" class="form-control" rows="5"></textarea>
    </div>

    <div class="form-group mb-3">
      <h3>Ingredients</h3>
      <table class="table table-bordered">
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
          <td><input v-model="ingredient.ingredient_name" class="form-control"/></td>
          <td><input v-model.number="ingredient.quantity_si" type="number" class="form-control"/></td>
          <td>
            <select v-model="ingredient.unit_si" class="form-select">
              <option label="liters">liters</option>
              <option label="grams">grams</option>
              <option label="units">units</option>
              <option label="pinches">pinches</option>
            </select>
          </td>
          <td>
            <button type="button" @click="removeIngredient(index)" class="btn btn-danger btn-sm">Remove</button>
          </td>
        </tr>
        </tbody>
      </table>
      <button type="button" @click="addIngredient" class="btn btn-primary">Add Ingredient</button>
    </div>

    <div class="form-group mb-3">
      <h3>Tags</h3>
      <div class="d-flex flex-wrap gap-2">
    <span
        v-for="(tag, index) in newRecipe.tags"
        :key="index"
        class="badge bg-secondary d-flex align-items-center gap-1"
    >
      {{ tag }}
      <button type="button" @click="removeTag(index)" class="btn-close btn-close-white btn-sm"></button>
    </span>
      </div>
      <div class="input-group mt-2">
        <input
            v-model="newTag"
            placeholder="Add tag"
            class="form-control"
        />
        <button
            type="button"
            @click="addTag(newTag)"
            class="btn btn-primary"
        >
          Add Tag
        </button>
      </div>
    </div>

    <button type="submit" class="btn btn-success" @click.prevent="submitRecipe">Save Recipe</button>
  </form>
</template>

<style scoped>

</style>