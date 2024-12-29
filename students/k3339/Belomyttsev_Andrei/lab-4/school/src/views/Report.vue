<template>
  <h2>Report {{ grade }}</h2>
  <h3>Total students: {{ report.total_students }}</h3>
  <h3>Teacher: {{ report.teacher }}</h3>
  <h3>Average marks:</h3>
  <p v-for="(value, name) in report.average_marks" :key="name">{{ name }}: {{ value }}</p>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      report: {},
      grade: '',
    }
  },
  methods: {
    async fetchReport() {
      const response = await axios.get(`/api/grade/${this.$route.params.id}/report/`)
      this.report = response.data
    },
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grade = response.data.find(i => i.id == this.$route.params.id)['number'] + response.data.find(i => i.id == this.$route.params.id)['letter']
    }
  },
  mounted() {
    this.fetchReport()
    this.fetchGrades()
  }
}
</script>

<style scoped>

</style>