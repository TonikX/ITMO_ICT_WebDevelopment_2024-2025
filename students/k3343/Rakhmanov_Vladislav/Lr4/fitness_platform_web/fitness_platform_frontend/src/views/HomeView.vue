<script setup lang="ts">
</script>

<template>
  <main>
    <div class="container px-4 py-5" id="featured-3">
      <h2 class="pb-2 border-bottom">To use the website please log in</h2>
      <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
        <div class="feature col">
          <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
            <svg class="bi" width="1em" height="1em"><use xlink:href="#collection"></use></svg>
          </div>
          <h3 class="fs-2 text-body-emphasis">Read Blogposts</h3>
          <p>Stay informed and inspired with our expert-written blog posts. Explore topics on fitness, nutrition, and wellness to gain valuable insights and tips that support your healthy lifestyle.</p>
          <router-link to="/blogposts" class="icon-link">
            Check it out
            <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
          </router-link>
        </div>
        <div class="feature col">
          <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
            <svg class="bi" width="1em" height="1em"><use xlink:href="#people-circle"></use></svg>
          </div>
          <h3 class="fs-2 text-body-emphasis">Workouts</h3>
          <p>Discover personalized workout plans tailored to your fitness goals. Whether you're a beginner or an experienced athlete, our guided exercises and structured routines will help you stay on track and maximize results.</p>
          <router-link to="/workouts" class="icon-link">
            Check it out
            <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
          </router-link>
        </div>
        <div class="feature col">
          <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
            <svg class="bi" width="1em" height="1em"><use xlink:href="#toggles2"></use></svg>
          </div>
          <h3 class="fs-2 text-body-emphasis">Track progress</h3>
          <p>Monitor your fitness journey with our intuitive progress tracking system. Log workouts, set goals, and analyze your improvements over time to stay motivated and achieve new milestones.</p>
          <router-link to="/progress" class="icon-link">
            Check it out
            <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>
