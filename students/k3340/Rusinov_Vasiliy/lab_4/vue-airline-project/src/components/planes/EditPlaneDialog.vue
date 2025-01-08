<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="500"
  >
    <v-card>
      <v-card-title>Изменение номера самолёта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="plane.number"
            label="Новый номер самолёта"
            required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="updatePlane">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      required: true,
    },
    plane: {
      type: Object,
      required: true,
    },
  },
  emits: ['update:dialog', 'plane-updated'],
  methods: {
    emitDialogUpdate(value) {
      this.$emit('update:dialog', value);
    },
    closeDialog() {
      this.$emit('update:dialog', false);
    },
    async updatePlane() {
      if (!this.plane.number) {
        alert('Введите номер самолёта');
        return;
      }

      try {
        this.$emit('plane-updated', { ...this.plane });
        this.closeDialog();
      } catch (error) {
        console.error('Ошибка изменения самолёта:', error);
        alert('Ошибка изменения самолёта');
      }
    },
  },
};
</script>

<style>
.v-card-title {
  font-weight: bold;
}
</style>

