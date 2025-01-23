<template>
  <div class="col-12">
    <h5>Информация о компании</h5>
    <p>Название компании: <span>{{ company.name }}</span></p>
    <p>Описание: <span>{{ company.description }}</span></p>
    <p>Контакты: <span>{{ company.contacts }}</span></p>
  </div>
</template>

<script>
  export default {
    props: {
      company: Object
    },
    setup(props) {
      return { company: props.company };
    }
  };
</script>
