<template>
  <nav v-if="authState.isLoggedIn">
    <ul>
      <li><v-btn text to="/planes">Planes</v-btn></li>
      <li><v-btn text to="/flights">Flights</v-btn></li>
      <li><v-btn text to="/crews">Crews</v-btn></li>
      <li><v-btn text to="/maintenances">Maintenances</v-btn></li>
      <li><v-btn text to="/routes">Routes</v-btn></li>
      <li><v-btn text to="/employees">Employees</v-btn></li>

      <li>
        <v-menu offset-y>
          <template #activator="{ props }">
            <v-btn text v-bind="props">Reports</v-btn>
          </template>
          <v-list>
            <v-list-item>
              <v-list-item-title>
                <v-btn text to="/routes-stats" class="menu-link">Отчет по маршрутам</v-btn>
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>
                <v-btn text to="/planes-stats" class="menu-link">Отчет по бортам</v-btn>
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </li>

      <li><v-btn text to="/profile">Profile</v-btn></li>
    </ul>
  </nav>
</template>

<script>
import { authState } from '../../store/auth.js';

export default {
  computed: {
    authState() {
      return authState;
    },
  },
};
</script>

<style>
nav {
  background-color: white;
  color: black;
  padding: 2rem 0;
  display: flex;
  justify-content: center;
}

nav ul {
  display: flex;
  justify-content: center;
  list-style: none;
  gap: 1em;
  margin: 0;
  padding: 0;
}

nav a {
  color: black;
  text-decoration: none;
  font-weight: 500;
}

nav a:hover {
  text-decoration: underline;
}

.menu-link {
  color: black;
}

.menu-link:hover {
  text-decoration: underline;
}
</style>
