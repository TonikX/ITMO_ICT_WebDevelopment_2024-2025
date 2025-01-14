<template>
  <v-footer app color="primary" dark>
    <v-col class="text-center" cols="12">
      &copy; {{ new Date().getFullYear() }} Клиника
    </v-col>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>
