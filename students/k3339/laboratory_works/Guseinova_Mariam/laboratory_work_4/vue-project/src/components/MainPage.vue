<template>
  <div class="main-page">
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <v-container>
      <v-row justify="center" align="center" spacing="6">
        <v-col v-for="(btn, index) in buttons" :key="index" cols="12" sm="4" md="3">
          <v-btn @click="goToPage(btn.page)" class="custom-button" block>{{ btn.text }}</v-btn>
        </v-col>
      </v-row>

      <v-img
        src="/Avtoservise.jpg"
        alt="Автосервис"
        class="service-image"
        contain
      ></v-img>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  data() {
    return {
      buttons: [
        {text: 'Список клиентов', page: 'CustomerList'},
        {text: 'Список услуг', page: 'services'},
        {text: 'Список сотрудников', page: 'employeeList'},
        {text: 'Список заказов', page: 'order-list'},
      ],
    };
  },
  methods: {
    goToPage(page) {
      this.$router.push({name: page});
    },
  },
};
</script>

<style scoped>
/* Задаем светло-зеленый фон для страницы */
.main-page {
  background-color: darkseagreen;
  min-height: 100vh; /* Полная высота страницы */
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
}

/* Стили для шапки */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

/* Стили для кнопок */
.custom-button {
  background-color: darkslategray !important; /* Зеленый цвет кнопок */
  color: white !important;
  text-transform: none !important; /* Отключение заглавных букв */
  font-size: 16px;
  height: 50px; /* Увеличиваем высоту кнопки */
}

.custom-button:hover {
  background-color: darkslategray !important; /* Немного темнее при наведении */
}

/* Стили для изображения */
.service-image {
  margin-top: 30px;
  max-height: 400px; /* Ограничение высоты изображения */
  width: 100%;
  object-fit: contain; /* Подгоняет изображение по размеру, не искажая его */
}
</style>
