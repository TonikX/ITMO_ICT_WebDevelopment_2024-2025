<template>
  <v-container>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="headline">Restaurants' managing</v-card-title>
          <v-card-text>
            <v-btn @click="goToPage('RestList')" color="primary" block>Список ресторанов</v-btn>
            <v-btn @click="goToPage('TableList')" color="primary" block>Список столов</v-btn>
            <v-btn @click="goToPage('BookingList')" color="primary" block>Бронирования</v-btn>
            <v-btn @click="goToPage('ReviewList')" color="primary" block>Отзывы</v-btn>
            <v-btn @click="goToPage('UserProfile')" color="primary" block>Мой профиль</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { VContainer, VRow, VCol, VCard, VCardTitle, VCardText, VBtn } from 'vuetify/components';

export default {
  name: 'MainPage',
  components: {
    VContainer,
    VRow,
    VCol,
    VCard,
    VCardTitle,
    VCardText,
    VBtn,
  },
  methods: {
    goToPage(page) {
      this.$router.push({ name: page });
    },
  },
};
</script>




<style scoped>

.v-btn {
  margin-bottom: 10px;
}
</style>
