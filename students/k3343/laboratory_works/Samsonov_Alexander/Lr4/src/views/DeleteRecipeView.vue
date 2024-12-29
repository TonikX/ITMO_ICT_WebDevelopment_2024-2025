<script setup>
import {onMounted} from "vue";
import {canEdit} from "@/composables/serverActions.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import axiosInstance from "@/services/axios.js";
import {isAuthenticated} from "@/composables/useAuth.js";


const recipeId = useRoute().params.recipeId;

onMounted(async () => {
  if (! isAuthenticated.value ||!await canEdit(recipeId)) {
    router.push({path: '/', replace: true});
  }
})

const deleteRecipe = async () => {
  const result = await axiosInstance.delete(`/recipes/${recipeId}/`)
  if (result.status === 200) {
    router.push({path: "/account", replace: true});
  }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <h4 class="card-title text-danger mb-3">Are you sure you want to delete this?</h4>
            <p class="card-text">
              This action cannot be undone. If you delete this item, it will be permanently removed from the system.
            </p>
            <div class="d-flex justify-content-around mt-4">
              <RouterLink to="/account" class="btn btn-secondary">Cancel</RouterLink>
              <button class="btn btn-danger" @click.prevent="deleteRecipe">Yes, Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>

</style>