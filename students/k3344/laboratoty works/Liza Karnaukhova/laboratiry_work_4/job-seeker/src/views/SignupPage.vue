<template>
  <base-layout>
    <HeaderComponent />
    <main-layout>
      <SignupCard />
    </main-layout>
    <FooterComponent />
  </base-layout>
</template>

<script>
  import HeaderComponent from "../components/HeaderComponent.vue";
  import FooterComponent from "@/components/FooterComponent.vue";
  import SignupCard from "@/components/SignupCard.vue"
  import BaseLayout from "@/layout/BaseLayout.vue";
  import MainLayout from "@/layout/MainLayout.vue";

  export default {
    name: "MainPage",
    components: {
      HeaderComponent,
      SignupCard,
      FooterComponent,
      BaseLayout,
      MainLayout,
    },
  };
</script>
