<template>
    <div>
      <h2>Classrooms</h2>
      <ul>
        <li v-for="classroom in classrooms" :key="classroom.classroom_id">
          Classroom #{{ classroom.number }} — {{ classroom.type }} — {{ classroom.address }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
import api from '@/api';
  
  export default {
    name: "ClassroomsView",
    data() {
      return {
        classrooms: []
      };
    },
    created() {
      api.get("http://localhost:8000/api/classrooms/")
        .then(response => {
          this.classrooms = response.data;
        })
        .catch(error => {
          console.error("Error fetching classrooms:", error);
        });
    }
  };
  </script>
  
  <style scoped>
  h2 {
    margin-top: 20px;
  }
  </style>
  