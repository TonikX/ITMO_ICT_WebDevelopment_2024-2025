<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">🔄 Список транзакций</v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="transactions"
          item-value="id"
          class="elevation-1"
          no-data-text="Нет доступных транзакций."
        >
          <template v-slot:item.returned="{ item }">
            <v-chip :color="item.returned ? 'green' : 'red'" dark>
              {{ item.returned ? 'Да' : 'Нет' }}
            </v-chip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-row v-if="!transactions.length">
      <v-col cols="12" class="text-center">
        <v-alert type="info">Нет доступных транзакций.</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    transactions: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.v-data-table tr td {
  vertical-align: middle;
  text-align: center;
}
</style>
