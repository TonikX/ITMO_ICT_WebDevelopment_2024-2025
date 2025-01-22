<script setup>
import {clearAuthToken, isAuthenticated} from "@/composables/tokenActions.js";
</script>

<template>
  <header class="p-3 mb-3 border-bottom">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <router-link :to="`/`" class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none">
          <svg fill="#000000" xmlns="http://www.w3.org/2000/svg"
               width="40" height="40" viewBox="0 0 485.535 485.535"
               xml:space="preserve">
<g>
	<g id="_x35__13_">
		<g>
			<path d="M55.465,123.228c-15.547,0-28.159,12.608-28.159,28.161v56.673C11.653,211.908,0,225.928,0,242.765
				c0,16.842,11.652,30.861,27.306,34.707v56.666c0,15.555,12.612,28.16,28.159,28.16c15.546,0,28.16-12.605,28.16-28.16V151.389
				C83.625,135.837,71.011,123.228,55.465,123.228z"/>
      <path d="M334.498,65.278c-23.092,0-41.811,18.719-41.811,41.812v93.864h-12.801h-60.585h-19.625l-6.827-0.163V107.09
				c0-23.092-18.72-41.812-41.813-41.812c-23.091,0-41.812,18.719-41.812,41.812v271.355c0,23.093,18.721,41.812,41.812,41.812
				c23.094,0,41.813-18.719,41.813-41.812v-93.653c0,0,4.501-0.211,6.827-0.211h19.625h60.585h12.801v93.864
				c0,23.093,18.719,41.812,41.811,41.812c23.094,0,41.812-18.719,41.812-41.812V107.089
				C376.311,83.998,357.592,65.278,334.498,65.278z"/>
      <path d="M458.229,208.062v-56.673c0-15.552-12.613-28.161-28.158-28.161c-15.547,0-28.16,12.608-28.16,28.161v182.749
				c0,15.555,12.613,28.16,28.16,28.16c15.545,0,28.158-12.605,28.158-28.16v-56.666c15.654-3.846,27.307-17.865,27.307-34.707
				C485.535,225.927,473.883,211.908,458.229,208.062z"/>
		</g>
	</g>
</g>
</svg>
        </router-link>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <router-link :to="`/`"
                       class="nav-link px-2 link-secondary">home
          </router-link>
          <router-link :to="`/workouts`"
                       class="nav-link px-2 link-secondary">workouts
          </router-link>
          <router-link :to="`/workouts/random`"
                       class="nav-link px-2 link-secondary">random workout
          </router-link>


        </ul>

        <div class="dropdown text-end">
          <a href="#" class="d-block link-body-emphasis text-decoration-none dropdown-toggle" data-bs-toggle="dropdown"
             aria-expanded="false">
            <img src="@/assets/user.png" alt="mdo" width="32" height="32" class="rounded-circle">
          </a>

          <div class="dropdown-menu text-small">
            <div v-if="isAuthenticated">
              <router-link class="dropdown-item" :to="`/favorites`">Favorites</router-link>
              <router-link class="dropdown-item" :to="`/done`">Done</router-link>
              <router-link class="dropdown-item" :to="`/comments`">Your comments</router-link>
              <router-link class="dropdown-item" :to="`/account/posts`">Your posts</router-link>
              <hr class="dropdown-divider">
              <a class="dropdown-item" href="#" @click="clearAuthToken">Log out</a>
            </div>
            <div v-else>
              <router-link class="dropdown-item" :to="`/login`">Sign in</router-link>
              <router-link class="dropdown-item" to="/register">Register</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>

</style>