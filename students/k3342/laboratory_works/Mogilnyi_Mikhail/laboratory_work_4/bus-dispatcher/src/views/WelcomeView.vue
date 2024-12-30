<template>
  <div>
    <section class="mt-5 p-4 rounded shadow">
      <div class="row align-items-center">
        <div class="col-md-5 text-center">
          <img
            src="@/assets/icons/bus-logo.svg"
            class="img-fluid"
            alt="Hero Image"
            style="max-width: 150px; height: auto;"
          />
        </div>
        <div class="col-md-7 text-center text-md-start">
          <h2 class="fw-bold mb-4">
            Управляйте автобусным парком с удобством!
          </h2>
          <div>
            <button
              type="button"
              class="btn btn-primary btn-lg me-3"
              data-bs-toggle="modal"
              data-bs-target="#log-in-modal"
            >
              Войти
            </button>
            <button
              type="button"
              class="btn btn-outline-primary btn-lg"
              data-bs-toggle="modal"
              data-bs-target="#register-modal"
            >
              Зарегистрироваться
            </button>
          </div>
        </div>
      </div>
    </section>

    <RegisterModal />
    <LoginModal />
  </div>
</template>

<script>
import LoginModal from '@/components/LoginModal.vue';
import RegisterModal from '@/components/RegisterModal.vue';

export default {
  name: 'WelcomeView',
  components: {
    LoginModal,
    RegisterModal,
  },
};
</script>

<style scoped>
</style>
