<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Ремонты самолетов</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.plane"
          :items="choices.planes"
          label="Фильтр по самолету"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.status"
          :items="choices.statuses"
          label="Фильтр по статусу"
          item-value="value"
          item-title="label"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.date"
          label="Фильтр по дате начала"
          type="date"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="openCreateDialog">Добавить ремонт</v-btn>
      </v-col>
    </v-row>

    <EditMaintenanceDialog
      v-if="selectedMaintenance"
      ref="editMaintenanceDialog"
      :dialog="editDialog"
      @update:dialog="editDialog = $event"
      :initial-maintenance="selectedMaintenance"
      :choices="choices"
      @maintenance-updated="updateMaintenance"
    />

    <CreateMaintenanceDialog
      ref="createMaintenanceDialog"
      :dialog="createDialog"
      :choices="choices"
      @update:dialog="createDialog = $event"
      @maintenance-created="addMaintenance"
    />

    <v-row>
      <v-col
        cols="12"
        md="6"
        v-for="maintenance in filteredAndPaginatedMaintenances"
        :key="maintenance.id"
      >
        <v-card class="compact-card mb-6" elevation="2">
          <v-card-title>
            Самолет: {{ maintenance.plane }}
          </v-card-title>
          <v-card-text>
            <p><strong>Дата начала:</strong> {{ formatDate(maintenance.start_date) }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Дата завершения:</strong> {{ maintenance.end_date ? formatDate(maintenance.end_date) : 'Не завершено' }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Описание:</strong> {{ maintenance.description }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Статус:</strong> {{ maintenance.status }}</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="warning" @click="openEditDialog(maintenance)">Редактировать</v-btn>
            <v-btn color="error" @click="openDeleteDialog(maintenance)">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <DeleteMaintenanceDialog
      v-if="selectedMaintenance"
      :dialog="deleteDialog"
      :maintenance="selectedMaintenance"
      @update:dialog="deleteDialog = $event"
      @maintenance-deleted="handleMaintenanceDeleted"
    />

    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="5"
        ></v-pagination>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import apiClient from "@/services/api";
import CreateMaintenanceDialog from "@/components/maintenances/CreateMaintenanceDialog.vue";
import EditMaintenanceDialog from "@/components/maintenances/EditMaintenanceDialog.vue";
import DeleteMaintenanceDialog from "@/components/maintenances/DeleteMaintenanceDialog.vue";

export default {
  components: {DeleteMaintenanceDialog, EditMaintenanceDialog, CreateMaintenanceDialog},
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 4,
      maintenances: [],
      filters: {
        plane: null,
        status: null,
        date: null,
      },
      choices: {
        planes: [],
        statuses: [],
      },
      createDialog: false,
      editDialog: false,
      deleteDialog: false,

      selectedMaintenance: null,
    };
  },
  computed: {
    filteredMaintenances() {
      let filtered = this.maintenances;
      console.log("фильтры", this.filters)
      if (this.filters.plane) {
        filtered = filtered.filter(m => m.plane === this.filters.plane);
      }
      if (this.filters.status) {
        filtered = filtered.filter(m => m.status === this.filters.status);
      }
      if (this.filters.date) {
        filtered = filtered.filter(m => m.start_date.startsWith(this.filters.date));
      }
      console.log("подходит", filtered)

      return filtered;
    },
    filteredAndPaginatedMaintenances() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredMaintenances.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredMaintenances.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchMaintenances() {
      try {
        const response = await apiClient.get("/maintenances/");
        console.log(response.data)
        this.maintenances = response.data;
      } catch (error) {
        console.error("Ошибка загрузки ремонтов:", error.response?.data || error.message);
        alert("Ошибка загрузки ремонтов");
      }
    },
    async fetchChoices() {
      try {
        const response = await apiClient.get("/maintenances/choices/");
        this.choices = response.data;
      } catch (error) {
        console.error("Ошибка загрузки фильтров:", error.response?.data || error.message);
        alert("Ошибка загрузки фильтров");
      }
    },
    async addMaintenance(newMaintenance) {
      try {
        await apiClient.post("/maintenances/", newMaintenance);
        await this.fetchMaintenances();
        this.$refs.createMaintenanceDialog.closeDialog();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.createMaintenanceDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка создания ремонта:", error.response?.data || error.message);
          alert("Ошибка создания ремонта.");
        }
      }
    },
    openCreateDialog() {
      this.createDialog = true;
    },
     openEditDialog(maintenance) {
      this.selectedMaintenance = maintenance
      console.log(this.selectedMaintenance)
      this.editDialog = true;
    },
    openDeleteDialog(maintenance) {
      this.selectedMaintenance = maintenance;
      this.deleteDialog = true;
    },
    async updateMaintenance(updatedMaintenance) {
      try {
        await apiClient.put(`/maintenances/${updatedMaintenance.id}/`, updatedMaintenance);
        this.$refs.editMaintenanceDialog.closeDialog();
        this.editDialog = false;
        await this.fetchMaintenances();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.editMaintenanceDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка обновления ремонта:", error.response?.data || error.message);
        }
      }
    },
    async handleMaintenanceDeleted(maintenanceId) {
      try {
        await apiClient.delete(`/maintenances/${maintenanceId}/`);
        this.maintenances = this.maintenances.filter(m => m.id !== maintenanceId);
      } catch (error) {
        console.error("Ошибка удаления ремонта:", error.response?.data || error.message);
      }
    },
     formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const year = date.getFullYear();
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');

      return `${day}.${month}.${year} ${hours}:${minutes}`;
    },
  },
  async created() {
    await Promise.all([this.fetchMaintenances(), this.fetchChoices()]);
  },
};
</script>
