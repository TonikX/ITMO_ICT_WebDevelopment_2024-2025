<template>
  <form @submit.prevent="submit">
    <input v-model="form.name" placeholder="Название типографии" required />
    <input v-model="form.address" placeholder="Адрес" required />
    <button type="submit">Сохранить</button>
    <button @click="cancel">Отменить</button>
  </form>
</template>

<script>
export default {
  props: {
    printShop: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      form: {
        name: this.printShop ? this.printShop.name : "",
        address: this.printShop ? this.printShop.address : "",
      },
    };
  },
  methods: {
    submit() {
      this.$emit("save", { ...this.form, id: this.printShop ? this.printShop.id : null });
    },
    cancel() {
      this.$emit("cancel");
    },
  },
};
</script>
