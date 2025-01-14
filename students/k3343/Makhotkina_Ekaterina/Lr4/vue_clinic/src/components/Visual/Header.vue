<template>
  <v-app-bar app color="primary" dark>
    <v-toolbar-title>Медицинская система</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text to="/home">Главная</v-btn>
    <v-btn text to="/patient">Пациенты</v-btn>
    <v-btn text to="/employees">Врачи</v-btn>
    <v-btn text to="/report">Отчеты</v-btn>
    <v-btn text to="/diagnosis">Диагнозы</v-btn>
    <v-btn text to="/appointments">Посещения</v-btn>
    <v-btn text to="/medical-cards">Карты</v-btn>
    <v-btn text to="/services">Услуги</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",
};
</script>

<style scoped>
.v-btn {
  margin-left: 10px;
}
</style>
