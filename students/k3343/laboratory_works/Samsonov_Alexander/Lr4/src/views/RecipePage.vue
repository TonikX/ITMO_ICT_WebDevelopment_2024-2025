<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {fetchAndReturn} from "@/composables/fetchAndReturn.js"
import RecipeBanner from "@/components/RecipeBanner.vue";
import Loremipsum from "@/components/loremipsum.vue";
import IngredientsTable from "@/components/IngredientsTable.vue";


const recipeId = useRoute().params.recipeId;
const RecipeData = ref(null)
const rLoading = ref(true);
const rError = ref(null);
const CommentsData = ref(null)
const cLoading = ref(true);
const cError = ref(null);

onMounted(async () => {
  // get recipe data
  await fetchAndReturn(`recipes/${recipeId}`, RecipeData, rLoading, rError)
  // get comments
  await fetchAndReturn(`comments/?recipe_id=${recipeId}`, CommentsData, cLoading, cError)
})

</script>

<template>
  <div v-if="rLoading">Loading recipe...</div>
  <div v-else-if="rError">{{ rError }}</div>
  <div v-else>
    <RecipeBanner :recipeInfo="RecipeData" class="my-3"/>
    <div class="d-block d-lg-none">
      <!--      here will be the table of ingredients for small screens -->
      <IngredientsTable :recipe-info="RecipeData"/>
    </div>
    <hr>
    <div class="container-fluid">
      <div class="row">
        <div class="d-none d-lg-block col-4">
          <div class="sticky-top" style="top: 5%;">
            <!--            here is the table of ingredients for big screens -->
            <IngredientsTable :recipe-info="RecipeData"/>
          </div>
        </div>
        <div class="col">
          <!--          place for contents-->
          <loremipsum/>
        </div>
      </div>
    </div>
  </div>

  <div v-if="cLoading">Loading comments...</div>
  <div v-else-if="cError">{{ cError }}</div>

  <div v-else>
    <h1>Success comments</h1>
    {{ CommentsData }}
  </div>

</template>

<style scoped>

</style>