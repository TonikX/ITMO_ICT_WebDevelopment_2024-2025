<template>
  <v-container class="welcome">
    <v-row class="fill-height align-center justify-center">
      <v-col cols="12" class="text-center">
        <h1>Добро пожаловать всем администраторам!</h1>
        <div class="button-group">
          <v-btn color="primary" large to="/login" class="mx-2">Login</v-btn>
          <v-btn color="primary" large to="/register" class="mx-2">Register</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
.welcome {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.button-group {
  margin-top: 30px;
}
</style>
