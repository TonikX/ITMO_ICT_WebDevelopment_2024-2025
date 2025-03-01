<template>
  <v-container>
    <v-card>
      <v-card-title>Отчет по доходу</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-select
            v-model="quarter"
            :items="quarters"
            label="Выберите квартал"
            required
          ></v-select>
          <v-btn color="primary" @click="fetchReport">Получить отчет</v-btn>
        </v-form>
        <div v-if="report">
          <h3>Отчет за {{ report.quarter }} квартал {{ report.year }}</h3>
          <p>Общий доход: {{ report.total_income }}</p>
          <v-data-table :headers="reportHeaders" :items="report.rooms"
                        class="elevation-1"></v-data-table>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Reports',
  data() {
    return {
      quarter: null,
      quarters: [
        {title: '1 квартал', value: '1'},
        {title: '2 квартал', value: '2'},
        {title: '3 квартал', value: '3'},
        {title: '4 квартал', value: '4'},
      ],
      report: null,
      reportHeaders: [
        {title: 'Номер комнаты', value: 'room_number', sortable: true},
        {title: 'Количество клиентов', value: 'client_count', sortable: true},
        {title: 'Доход', value: 'income', sortable: true},
      ],
    }
  },
  methods: {
    fetchReport() {
      if (!this.quarter) {
        alert("Выберите квартал")
        return
      }
      axios.get(`http://localhost:8000/api/reports/?quarter=${this.quarter}`)
        .then(response => {
          this.report = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
  },
}
</script>
