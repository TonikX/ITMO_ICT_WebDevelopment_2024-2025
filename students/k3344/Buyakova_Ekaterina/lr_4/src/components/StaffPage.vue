<template>
  <v-container>
    <h1 class="text-center">Список сотрудников</h1>
    <v-divider class="my-4"></v-divider>

    <v-data-table
      :headers="headers"
      :items="staff"
      class="elevation-1"
      item-key="id"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Сотрудники</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="fetchStaff">Обновить</v-btn>
          <v-btn color="success" @click="openAddDialog">Добавить сотрудника</v-btn>
        </v-toolbar>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <v-btn color="red" variant="text" @click="openDialog('fire', item)">
          Уволить
        </v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog.visible" max-width="500px">
      <v-card>
        <v-card-title class="headline">Уволить сотрудника</v-card-title>
        <v-card-text>
          Вы уверены, что хотите уволить сотрудника
          "{{ dialog.target?.first_name }} {{ dialog.target?.last_name }}"?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant=text @click="closeDialog">Отмена</v-btn>
          <v-btn color="red" variant=text @click="confirmFire">Уволить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="addDialog.visible" max-width="500px">
      <v-card>
        <v-card-title class="headline">Добавить нового сотрудника</v-card-title>
        <v-card-text>
          <v-text-field
            label="Имя"
            v-model="addDialog.form.first_name"
            required
          ></v-text-field>
          <v-text-field
            label="Фамилия"
            v-model="addDialog.form.last_name"
            required
          ></v-text-field>
          <v-text-field
            label="Профессия"
            v-model="addDialog.form.profession"
            required
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant=text @click="closeAddDialog">Отмена</v-btn>
          <v-btn color="green" variant=text @click="confirmAdd">Добавить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import type Staff from "@/models/staff";
import axiosApi from "@/plugins/axios";
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "StaffPage",
  setup() {
    const staff = ref([] as Staff[]);
    const headers = ref([
      { title: "ID", value: "id" },
      { title: "Имя", value: "first_name" },
      { title: "Фамилия", value: "last_name" },
      { title: "Профессия", value: "profession" },
      { title: "Действия", value: "actions", sortable: false },
    ]);

    const dialog = ref({
      visible: false,
      target: null as Staff | null,
    });

    const addDialog = ref({
      visible: false,
      form: {
        first_name: "",
        last_name: "",
        profession: "",
      },
    });

    const fetchStaff = async () => {
      try {
        staff.value = [];
        const response = await axiosApi.get("/staff");
        staff.value = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка сотрудников:", error);
      }
    };

    const openDialog = (action: string, target: Staff) => {
      dialog.value.target = target;
      dialog.value.visible = true;
    };

    const closeDialog = () => {
      dialog.value.visible = false;
      dialog.value.target = null;
    };

    const confirmFire = async () => {
      if (!dialog.value.target) return;

      try {
        await axiosApi.delete(`/staff/${dialog.value.target.id}/`);
        await fetchStaff();
        closeDialog();
      } catch (error) {
        console.error("Ошибка при увольнении сотрудника:", error);
      }
    };

    const openAddDialog = () => {
      addDialog.value.visible = true;
    };

    const closeAddDialog = () => {
      addDialog.value.visible = false;
      addDialog.value.form = { first_name: "", last_name: "", profession: "" };
    };

    const confirmAdd = async () => {
      try {
        await axiosApi.post("/staff/", addDialog.value.form);
        await fetchStaff();
        closeAddDialog();
      } catch (error) {
        console.error("Ошибка при добавлении сотрудника:", error);
      }
    };

    onMounted(fetchStaff);

    return {
      staff,
      headers,
      dialog,
      addDialog,
      fetchStaff,
      openDialog,
      closeDialog,
      confirmFire,
      openAddDialog,
      closeAddDialog,
      confirmAdd,
    };
  },
});
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
