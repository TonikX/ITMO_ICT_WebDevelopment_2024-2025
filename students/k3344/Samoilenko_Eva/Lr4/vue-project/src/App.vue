<template>
  <v-layout class="rounded rounded-md">
    <v-navigation-drawer permanent color="green">
      <v-list-item height="100"
                   title="Hotel Administration" align="center"></v-list-item>
      <v-divider thickness="5" color="white"></v-divider>
      <template v-if="!Token.token">

        <router-link to="/login" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Login"></v-list-item>
        </router-link>
        <router-link to="/register" style="text-decoration: none; color: inherit;">
          <v-list-item
            link title="Register"></v-list-item>
        </router-link>
      </template>
      <template v-if="Token.token">
        <router-link to="/rooms" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Rooms"></v-list-item>
        </router-link>
        <router-link to="/clients" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Clients"></v-list-item>
        </router-link>
        <router-link to="/employees" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Employees"></v-list-item>
        </router-link>
        <router-link to="/bookings" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Bookings"></v-list-item>
        </router-link>
        <router-link to="/cleanings" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Cleanings"></v-list-item>
        </router-link>
        <router-link to="/report" style="text-decoration: none; color: inherit;">
          <v-list-item link title="Quarter Report"></v-list-item>
        </router-link>
        <v-list-item to="/login" style="text-decoration: none; background-color: #D32F2F;"
                     @click="Token.deleteToken">Log Out
        </v-list-item>
      </template>
    </v-navigation-drawer>
    <v-main class="d-flex justify-center" style="min-height: 300px;">

      <router-view/>

      <div class="message-div">
        <template v-if="!Token.token && route.path === '/'">
          <p class="custom-message">You are not logged in.</p>
          <p class="welcome-message">But welcome to the Hotel Administration!</p>
          <v-list-item height="100" align="center" base-color="black">Please Log in, or
            Register, as an Administrator to proceed with other pages
          </v-list-item>
        </template>
      </div>
    </v-main>
  </v-layout>
</template>

<script setup>
import {TokenDB} from "@/tokens/TokenDB"
import {useRoute} from "vue-router";

const Token = TokenDB()
const route = useRoute()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.custom-message {
  color: red;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  text-align: center;
}

.welcome-message {
  color: black;
  font-size: 18px;
  font-weight: bold;
  margin-top: 20px;
  text-align: center;
}

.message-div {
  position: absolute;
  align-self: center;
  width: 1000px;
}
</style>
