<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Welcome to Airport Management System</h1>
        </v-col>
      </v-row>
      <v-row v-if="user">
        <v-col cols="12">
          <v-card>
            <v-card-text>
              <p>You are logged in as: {{ user.username }}</p>
              <p v-if="user.is_staff">You are logged in as administrator</p>
              <p v-else>You are logged in as user</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Navigation</v-card-title>
            <v-card-text>
              <v-btn v-for="link in links" :key="link.name" :to="link.path" text>
                {{ link.name }}
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import { mapState } from "vuex";
  
  export default {
    name: "Home",
    computed: {
      ...mapState("auth", ["user"]),
      links() {
        const allLinks = [
          { name: "Flights", path: "/flights" },
          { name: "Routes", path: "/routes" },
          { name: "Airplanes", path: "/airplanes" },
          { name: "Employees", path: "/employees" },
          { name: "Requests", path: "/requests" },
          { name: "Profile", path: "/profile" },
        ];
        if (this.user) {
          if (this.user.is_admin) {
            return allLinks;
          } else {
            return [
              { name: "Flights", path: "/flights" },
              { name: "Profile", path: "/profile" },
            ];
          }
        } else {
            return []
        }
      },
    },
  };
  </script>
  