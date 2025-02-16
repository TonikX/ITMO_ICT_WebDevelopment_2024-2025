<template>
  <div>
    <h2>Grade Report</h2>
    <div v-if="report.length">
      <table>
        <thead>
          <tr>
            <th>Group</th>
            <th>Average Grade</th>
            <th>Number of Grades</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in report" :key="entry.group_id">
            <td>{{ entry.group_id }}</td>
            <td>{{ entry.average_grade.toFixed(2) }}</td>
            <td>{{ entry.count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Loading grade report...</p>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: "GradeReport",
  data() {
    return {
      groups: [],
      sessions: [],
      results: [],
      report: []
    }
  },
  created() {
    Promise.all([
      api.get("http://localhost:8000/api/groups/"),
      api.get("http://localhost:8000/api/classsessions/"),
      api.get("http://localhost:8000/api/results/")
    ])
    .then(([groupsRes, sessionsRes, resultsRes]) => {
      this.groups = groupsRes.data;
      this.sessions = sessionsRes.data;
      this.results = resultsRes.data;
      this.generateReport();
    })
    .catch(error => {
      console.error("Error fetching data for grade report:", error);
    });
  },
  methods: {
    generateReport() {
      this.report = this.groups.map(group => {
        const groupSessions = this.sessions.filter(session => session.group_id === group.group_id);
        let numericResults = [];
        
        groupSessions.forEach(session => {
          const sessionResults = this.results.filter(result => result.class_id === session.class_id);
          sessionResults.forEach(resultObj => {
            const numericValue = parseFloat(resultObj.result);
            if (!isNaN(numericValue)) {
              numericResults.push(numericValue);
            }
          });
        });
        
        const count = numericResults.length;
        const average = count ? numericResults.reduce((sum, val) => sum + val, 0) / count : 0;
        
        return {
          group_id: group.group_id,
          average_grade: average,
          count: count
        };
      });
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

p {
  margin-top: 20px;
}
</style>
