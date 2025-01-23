<template>
  <div class="col-12">
    <h5>Информация о пользователе</h5>
    <p>E-mail: <span>{{ email }}</span></p>
    <button type="button" class="btn button btn-custom">Изменить пароль</button>
  </div>
</template>

<script>
  export default {
    props: {
      email: {
        type: String,
        required: true
      }
    }
  };
</script>

<style scoped>
  /* Добавьте стили, если необходимо */
</style>
