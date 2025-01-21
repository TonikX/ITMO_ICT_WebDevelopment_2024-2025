<template>
  <HeaderLoader :currentPath="currentPath" />
  <div class="index-background">
    <main role="main" class="form-container auth-page">
      <button class="form-close" aria-label="Close Authentication Form" @click="closeForm">
          <i class="uil uil-times"></i>
      </button>

      <LoginForm v-show="currentForm === 'login'" @switch-form="switchForm" />
      <SignupForm v-show="currentForm === 'signup'" @switch-form="switchForm" />
    </main>
  </div>
</template>

<script>
import LoginForm from "@/components/LoginForm.vue";
import SignupForm from "@/components/SignupForm.vue";
import HeaderLoader from "@/components/HeaderLoader.vue";

export default {
  components: {
    HeaderLoader,
    LoginForm,
    SignupForm
  },
  data() {
    return {
      currentPath: "auth",
      currentForm: "login"
    };
  },
  methods: {
    switchForm(form) {
      this.currentForm = form;
    },

    closeForm() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
@import url('../assets/css/auth.css');
</style>
