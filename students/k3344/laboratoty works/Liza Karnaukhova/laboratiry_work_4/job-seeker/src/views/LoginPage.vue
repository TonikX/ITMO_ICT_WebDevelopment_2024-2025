<template>
  <base-layout>
    <HeaderComponent />
    <main-layout>
      <LoginCard />
    </main-layout>
    <FooterComponent />
  </base-layout>
</template>

<script>
  import HeaderComponent from "../components/HeaderComponent.vue";
  import FooterComponent from "@/components/FooterComponent.vue";
  import LoginCard from "@/components/LoginCard.vue"
  import BaseLayout from "@/layout/BaseLayout.vue";
  import MainLayout from "@/layout/MainLayout.vue";

  export default {
    name: "MainPage",
    components: {
      HeaderComponent,
      LoginCard,
      FooterComponent,
      BaseLayout,
      MainLayout,
    },
  };
</script>
