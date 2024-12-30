<template>
  <v-container>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="headline">Автосервис</v-card-title>
          <v-card-text>
            <v-btn @click="goToPage('CustomerList')" color="primary" block>Список клиентов</v-btn>
            <v-btn @click="goToPage('services')" color="primary" block>Список услуг</v-btn>
            <v-btn @click="goToPage('employeeList')" color="primary" block>Список сотрудников</v-btn>
            <v-btn @click="goToPage('order-list')" color="primary" block>Список заказов</v-btn>
            <v-btn @click="goToPage('PaymentList')" color="primary" block>Список платежей</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'MainPage',
  methods: {
    // Метод для навигации по страницам
    goToPage(page) {
      this.$router.push({ name: page });
    }
  }
};
</script>

<style scoped>
/* Стили для страницы */
.v-btn {
  margin-bottom: 10px;
}
</style>
