<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="400"
  >
    <v-card>
      <v-card-title class="text-h5">Подтвердите увольнение</v-card-title>
      <v-card-text>
        Вы уверены, что хотите уволить сотрудника "{{ employee.first_name }} {{ employee.last_name }}"?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="red" @click="confirmDelete">Уволить</v-btn>
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
    employee: {
      type: Object,
      required: true,
    },
  },
  emits: ['update:dialog', 'employees-deleted'],
  methods: {
    emitDialogUpdate(value) {
      this.$emit('update:dialog', value);
    },
    closeDialog() {
      this.$emit('update:dialog', false);
    },
    confirmDelete() {
      this.$emit('employees-deleted', this.employee.id);
      this.closeDialog();
    },
  },
};
</script>
