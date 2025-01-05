<template>
  <v-container>
    <h1 class="text-center">Расписание работы</h1>
    <v-divider class="my-4"></v-divider>

    <v-data-table
      :headers="headers"
      :items="schedule"
      class="elevation-1"
      item-key="id"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Расписание</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="fetchSchedule">Обновить</v-btn>
          <v-btn color="success" @click="openAssignDialog">Добавить</v-btn>
        </v-toolbar>
      </template>
      <template v-slot:[`item.day_of_week`]="{ item }">
        <span>{{ item.day_of_week }}</span>
      </template>
      <template v-slot:[`item.floor`]="{ item }">
        <span>{{ item.floor }}</span>
      </template>
      <template v-slot:[`item.staff_name`]="{ item }">
        <span>{{ item.staff_name }}</span>
      </template>
      <template v-slot:[`item.client`]="{ item }">
        <span v-if="item.client">{{ item.client }}</span>
        <span v-else>-</span>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-btn color="red" variant="text" @click="openDialog(item)">
          Удалить
        </v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog.visible" max-width="500px">
      <v-card>
        <v-card-title class="headline">Уволить сотрудника</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить запись?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant=text @click="closeDialog">Отмена</v-btn>
          <v-btn color="red" variant=text @click="confirmDelete">Уволить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="assignDialog.visible" max-width="500px">
      <v-card>
        <v-card-title class="headline">Добавить запись</v-card-title>
        <v-card-text>
          <v-select
            label="Имя работника"
            :items="staff"
            item-title="full_name"
            item-value="id"
            v-model="assignDialog.form.staff_id"
            required
          ></v-select>
          <v-select
            label="День недели"
            :items="daysOfWeek"
            v-model="assignDialog.form.day_of_week"
            required
          ></v-select>
          <v-text-field
            label="Этаж"
            v-model="assignDialog.form.floor"
            type="number"
            required
          ></v-text-field>
          <v-text-field
            label="ID клиента (опционально)"
            v-model="assignDialog.form.client"
            type="number"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" variant=text @click="closeAssignDialog">Cancel</v-btn>
          <v-btn color="green" variant=text @click="confirmAssign">Assign</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import type CleaningSchedule from "@/models/cleaning-schedule";
import type Staff from "@/models/staff";
import axiosApi from "@/plugins/axios";
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "CleaningSchedulePage",
  setup() {
    const schedule = ref([] as CleaningSchedule[]);
    const staff = ref([] as Staff[]);
    const daysOfWeek = ref([
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ]);

    const headers = ref([
      { title: "Работник", value: "staff_name" },
      { title: "День недели", value: "day_of_week" },
      { title: "Этаж", value: "floor" },
      { title: "Id клиента", value: "client" },
      { title: "Действия", value: "actions", sortable: false },
    ]);

    const assignDialog = ref({
      visible: false,
      form: {
        staff_id: null as number | null,
        day_of_week: "",
        floor: 1,
        client: null as number | null,
      },
    });

    const dialog = ref({
      visible: false,
      target: null as CleaningSchedule | null,
    });

    const openDialog = (target: CleaningSchedule) => {
      dialog.value.target = target;
      dialog.value.visible = true;
    };

    const closeDialog = () => {
      dialog.value.visible = false;
      dialog.value.target = null;
    };

    const confirmDelete = async () => {
      if (!dialog.value.target) return;

      try {
        await axiosApi.delete(`/cleaning-schedule/${dialog.value.target.id}/`);
        await fetchSchedule();
        closeDialog();
      } catch (error) {
        console.error("Ошибка при увольнении сотрудника:", error);
      }
    };

    const fetchSchedule = async () => {
      try {
        const response = await axiosApi.get("/cleaning-schedule/");
        schedule.value = response.data;
      } catch (error) {
        console.error("Ошибка загрузки расписания:", error);
      }
    };

    const fetchStaff = async () => {
      try {
        const response = await axiosApi.get("/staff");
        staff.value = response.data.map((s: Staff) => ({
          ...s,
          full_name: `${s.first_name} ${s.last_name} (${s.profession})`,
        }));
      } catch (error) {
        console.error("Ошибка загрузки персонала:", error);
      }
    };

    const openAssignDialog = () => {
      assignDialog.value.visible = true;
    };

    const closeAssignDialog = () => {
      assignDialog.value.visible = false;
      assignDialog.value.form = { staff_id: null, day_of_week: "", floor: 1, client: null };
    };

    const confirmAssign = async () => {
      try {
        await axiosApi.post("/cleaning-schedule/", {
          floor: assignDialog.value.form.floor,
          day_of_week: assignDialog.value.form.day_of_week,
          staff: assignDialog.value.form.staff_id,
        });
        await fetchSchedule();
        closeAssignDialog();
      } catch (error) {
        console.error("Ошибка изменения расписания:", error);
      }
    };

    onMounted(async () => {
      await fetchSchedule();
      await fetchStaff();
    });

    return {
      schedule,
      staff,
      daysOfWeek,
      headers,
      assignDialog,
      fetchSchedule,
      openAssignDialog,
      closeAssignDialog,
      confirmAssign,
      openDialog,
      dialog,
      closeDialog,
      confirmDelete
    };
  },
});
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
