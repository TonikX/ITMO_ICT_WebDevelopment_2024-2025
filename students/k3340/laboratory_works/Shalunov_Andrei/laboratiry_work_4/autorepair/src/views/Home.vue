<template>
  <v-container>
    <h1>Welcome to Auto Repair Shop</h1>

    <v-row>
      <v-col>
        <router-link to="/login">
          <v-btn color="primary" block>Login</v-btn>
        </router-link>
      </v-col>
      <v-col>
        <router-link to="/register">
          <v-btn color="secondary" block>Register</v-btn>
        </router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Home",
};
</script>
