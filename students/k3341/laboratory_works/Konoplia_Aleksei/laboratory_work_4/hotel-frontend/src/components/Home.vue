<template>
  <v-container class="d-flex justify-center">
    <v-card
      class="pa-5 elevated-card"
      width="400"
      height="215"
    >
      <h2 class="text-center">Добро пожаловать в гостиницу!</h2>
      <p class="text-center">Здесь можно управлять клиентами, сотрудниками, номерами и т. д.</p>
      <div class="d-flex justify-center mt-4">
        <v-btn variant="elevated" color="primary" to="/profile">
          Перейти к профилю
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'Home'
}
</script>
