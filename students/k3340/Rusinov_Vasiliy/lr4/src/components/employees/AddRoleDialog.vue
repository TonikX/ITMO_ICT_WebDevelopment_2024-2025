<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="400"
  >
    <v-card>
      <v-card-title>Добавление роли сотруднику</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-select
            v-model="selectedRole"
            :items="availableRoles"
            label="Выберите роль"
            item-value="value"
            item-title="label"
            required
          ></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="addRole">Добавить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    employeeId: { type: Number, required: true },
    availableRoles: { type: Array, required: true },
    existingRoles: { type: Array, required: true },
  },
  emits: ["update:dialog", "role-added"],
  data() {
    return {
      selectedRole: null,
    };
  },
  methods: {
    emitDialogUpdate(value) {
      this.$emit("update:dialog", value);
    },
    closeDialog() {
      this.$emit("update:dialog", false);
      this.selectedRole = null;
    },
    async addRole() {
      if (!this.selectedRole) {
        alert("Выберите роль!");
        return;
      }

      if (this.existingRoles.includes(this.selectedRole)) {
        alert("У сотрудника уже есть эта роль.");
        return;
      }

      try {
        const roleData = {
          employee: this.employeeId,
          role: this.selectedRole,
        };
        this.$emit("role-added", roleData);
        this.closeDialog();
      } catch (error) {
        console.error("Ошибка добавления роли:", error.response?.data || error.message);
        alert("Ошибка добавления роли.");
      }
    },
  },
};
</script>
