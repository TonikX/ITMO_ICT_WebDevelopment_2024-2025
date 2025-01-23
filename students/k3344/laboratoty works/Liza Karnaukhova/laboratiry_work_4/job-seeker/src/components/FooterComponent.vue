<template>
  <footer class="bg-dark text-white mt-auto">
    <div class="container py-4">
      <div class="row">
        <div class="col-md-4">
          <h4>О нас</h4>
          <p>Краткая информация о компании.</p>
        </div>
        <div class="col-md-4">
          <h5>Ссылки</h5>
          <ul class="list-unstyled">
            <li><router-link to="/" class="text-white">Главная</router-link></li>
            <li><router-link to="/login" class="text-white">Войти</router-link></li>
            <li><router-link to="/signup" class="text-white">Регистрация</router-link></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h5>Контакты</h5>
          <p>
            <MailIcon class="me-2"/>
            <span>Email: info@example.com</span>
          </p>
          <p>
            <PhoneIcon class="me-2"/>
            <span>Телефон: +7 (123) 456-78-90</span>
          </p>
        </div>
      </div>
      <div class="text-center py-3">
        <small>&copy; 2024 Все права защищены.</small>
      </div>
    </div>
  </footer>
</template>

<script>
  import PhoneIcon from "@/components/icons/IconPhone.vue";
  import MailIcon from "@/components/icons/IconMail.vue";

  export default {
    name: 'FooterComponent',
    components: {
      MailIcon,
      PhoneIcon,
    }
  };
</script>

<style scoped>
</style>
