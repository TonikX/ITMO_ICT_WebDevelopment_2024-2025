<template>
  <form @submit.prevent="submit">
    <input v-model="form.name" placeholder="Название газеты" required />
    <input v-model="form.index" placeholder="Индекс" required />
    <input v-model="form.editor_last_name" placeholder="Фамилия редактора" required />
    <input v-model="form.editor_first_name" placeholder="Имя редактора" required />
    <input v-model="form.editor_patronymic" placeholder="Отчество редактора" />
    <input v-model="form.price" type="number" placeholder="Цена" required />
    <button type="submit">Сохранить</button>
    <button type="button" @click="$emit('cancel')">Отмена</button>
  </form>
</template>

<script>
export default {
  props: {
    newspaper: {
      type: Object,
      required: false,
      default: () => null,
    },
  },
  data() {
    return {
      form: this.newspaper
        ? { ...this.newspaper }
        : { name: "", index: "", editor_last_name: "", editor_first_name: "", editor_patronymic: "", price: null },
    };
  },
  methods: {
    submit() {
      this.$emit("save", this.form);
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
</style>
