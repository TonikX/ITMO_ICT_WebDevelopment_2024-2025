<script setup>
</script>

<template>


  <div class="p-5 mb-4 bg-body-tertiary rounded-3">
    <div class="container-fluid py-5">
      <h1 class="display-5 fw-bold">Renting website</h1>
      <p class="col-md-8 fs-4">ooking for a place to live or rent out your property? 🏠✨ Our platform connects owners and
        renters with just a few clicks. We make finding your next home—or filling it with happy tenants—simple, fast,
        and totally stress-free (well, mostly 😉). Browse, list, and live your best life!</p>
      <a class="btn btn-primary btn-lg" type="button" href="https://github.com/">Check out souce code</a>
    </div>
  </div>
  <div class="row align-items-md-stretch">
    <div class="col-md-6">
      <div class="h-100 p-5 text-bg-dark rounded-3">
        <h2>Want to earn some steady income?</h2>
        <p>Got a property? 🏡💼 Why let it sit empty? List it with us and reach thousands of renters looking for their
          next home! It’s quick, easy, and your first step to earning stress-free income. Start renting out today!</p>
        <RouterLink class="btn btn-outline-light" type="button" to="/landlord/me/">Landlord menu here</RouterLink>
      </div>
    </div>
    <div class="col-md-6">
      <div class="h-100 p-5 bg-body-tertiary border rounded-3">
        <h2>Want to find your new home?</h2>
        <p>Find your dream place 🏠✨ without the headaches! Browse hundreds of listings, from cozy apartments to spacious
          homes. Use our site to discover the perfect fit and get ready to move in—fast and hassle-free!</p>
        <router-link class="btn btn-outline-secondary" type="button" to="tenant">Leaser menu here</router-link>
      </div>
    </div>
  </div>
</template>
