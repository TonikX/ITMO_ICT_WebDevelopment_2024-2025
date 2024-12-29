<script setup>
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {fetchAndReturn} from "@/composables/serverActions.js"
import RecipeBanner from "@/components/recipeComponents/RecipeBanner.vue";
import IngredientsTable from "@/components/recipeComponents/IngredientsTable.vue";
import RecipeText from "@/components/recipeComponents/RecipeText.vue";
import CommentForm from "@/components/commentComponents/commentForm.vue";
import CommentCard from "@/components/commentComponents/commentCard.vue";
import {isAuthenticated} from "@/composables/useAuth.js";


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

const onCommentSubmitted = async (result) => {
  await fetchAndReturn(`comments/?recipe_id=${recipeId}`, CommentsData, cLoading, cError)
  CommentsData.value.push(await result)
}
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
          <RecipeText :recipeInfo="RecipeData"/>
        </div>
      </div>
    </div>
  </div>

  <hr class="my-3"/>
  <div v-if="cLoading">Loading comments...</div>
  <div v-else-if="cError">{{ cError }}</div>
  <div v-else>
    <h1 class="custom-text">Комментарии</h1>
    <comment-form v-if="isAuthenticated" @submit-comment="onCommentSubmitted" />
    <comment-card v-for="Comment in CommentsData" :key="Comment.id" :commentInfo="Comment"/>
  </div>

</template>

<style scoped>
.custom-text {
  position: relative;
  left: -270px;
  text-align: center;
}
</style>