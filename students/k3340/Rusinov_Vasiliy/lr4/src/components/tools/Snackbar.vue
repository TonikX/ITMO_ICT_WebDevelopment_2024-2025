<template>
  <v-snackbar
    v-model="show"
    :timeout="timeout"
    :color="color"
    top
  >
    {{ message }}
  </v-snackbar>
</template>

<script>
export default {
  props: {
    timeout: {
      type: Number,
      default: 3000,
    },
    color: {
      type: String,
      default: "green",
    },
  },
  data() {
    return {
      show: false,
      message: "",
    };
  },
  methods: {
    showSnackbar(msg, color = "green") {
      if (!this.$el) return;
      this.message = msg;
      this.color = color;
      this.show = true;
    },
  },
};
</script>
