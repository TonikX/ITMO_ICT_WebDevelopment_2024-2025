<script setup>
import {ref} from "vue";

const props = defineProps(['recipe'])
const recipe = ref(props.recipe)
const rating = ref(recipe.value.stars_sum / recipe.value.number_ratings || 0)
</script>

<template>
  <div class="card my-2 mx-2" style="max-width: 540px;">
    <RouterLink :to="`recipe/${recipe.id}`">
      <div class="row g-0">
        <div class="col-md-4">
          <img :src="recipe.thumbnail_link" class="img-fluid rounded-start" :alt="recipe.header"/>
        </div>
        <div class="col-md-8">
          <div class="card-body">
            <h5 class="card-title">{{ recipe.header }}</h5>
            <p class="card-text custom-text">{{ recipe.content_json.text }}</p>
            <p class="card-text d-flex justify-content-between">
              <small class="text-body-secondary"> {{ rating.toFixed(1) }} /10 </small>
              <small>
                <RouterLink :to="`recipe/${recipe.id}/edit`">
                  <button class="btn btn-primary">Edit</button>
                </RouterLink>
                <RouterLink :to="`recipe/${recipe.id}/delete`">
                  <button class="btn btn-danger">Delete</button>
                </RouterLink>
              </small>
            </p>
          </div>
        </div>
      </div>
    </RouterLink>
  </div>
</template>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}

.custom-text {
  width: 300px;
  height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>