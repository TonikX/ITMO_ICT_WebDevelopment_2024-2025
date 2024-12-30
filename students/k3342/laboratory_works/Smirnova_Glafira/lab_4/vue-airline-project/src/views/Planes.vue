<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Список самолётов</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          v-model="selectedModel"
          :items="filterModels"
          label="Фильтр по модели"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="6">
        <v-text-field
          v-model="searchQuery"
          label="Поиск по номеру самолёта"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="openDialog">Добавить самолёт</v-btn>
      </v-col>
    </v-row>

    <CreatePlaneDialog
      :dialog="dialog"
      @update:dialog="dialog = $event"
      :availableModels="availableModels"
      @plane-created="addPlane"
    />

    <EditPlaneDialog
      :dialog="editDialog"
      :plane="selectedPlane"
      @update:dialog="editDialog = $event"
      @plane-updated="handlePlaneUpdate"
    />

    <DeletePlaneDialog
      :dialog="deleteDialog"
      :plane="selectedPlane"
      @update:dialog="deleteDialog = $event"
      @plane-deleted="handlePlaneDelete"
    />

    <v-row>
      <v-col
        cols="12"
        md="6"
        lg="4"
        v-for="plane in paginatedFilteredPlanes"
        :key="plane.id"
      >
        <v-card class="mb-4" elevation="2">
          <v-card-title>{{ plane.model_name }}</v-card-title>
          <v-card-subtitle>Номер: {{ plane.number }}</v-card-subtitle>
          <v-card-text>
            <p>Вместимость: {{ plane.capacity }}</p>
            <p>Скорость: {{ plane.modelSpeed }} км/ч</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="openEditDialog(plane)">Изменить</v-btn>
            <v-btn color="red" @click="openDeleteDialog(plane)">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

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
import apiClient from '@/services/api';
import CreatePlaneDialog from '@/components/planes/CreatePlaneDialog.vue';
import EditPlaneDialog from "@/components/planes/EditPlaneDialog.vue";
import DeletePlaneDialog from "@/components/planes/DeletePlaneDialog.vue";


export default {
  components: {DeletePlaneDialog, EditPlaneDialog, CreatePlaneDialog },

  data() {
    return {
      dialog: false,
      planes: [],
      selectedModel: null,
      filterModels: [],
      availableModels: [],
      searchQuery: '',
      currentPage: 1,
      itemsPerPage: 6,
      editDialog: false,
      deleteDialog: false,
      selectedPlane: { id: null, number: '' },
    };
  },
  computed: {
    filteredPlanes() {
      let filtered = this.planes;

      if (this.selectedModel) {
        filtered = filtered.filter(
          plane => plane.model_name === this.selectedModel
        );
      }

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(plane =>
          plane.number.toLowerCase().includes(query)
        );
      }

      return filtered;
    },
    paginatedFilteredPlanes() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredPlanes.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredPlanes.length / this.itemsPerPage);
    },
  },
  methods: {

    openEditDialog(plane) {
      this.selectedPlane = { ...plane };
      console.log('Selected plane:', this.selectedPlane);
      this.editDialog = true;
    },

    async handlePlaneUpdate(updatedPlane) {
      try {
    if (!updatedPlane.id) {
      console.error('Ошибка: ID самолёта отсутствует.');
      return;
    }
    console.log('Id of plane to change:', updatedPlane.id);
    await apiClient.put(`/planes/${updatedPlane.id}/`, updatedPlane);
    this.editDialog = false;
    await this.fetchPlanes();
  } catch (error) {
    console.error('Ошибка обновления самолёта:', error.response?.data || error.message);
  }
    },

     openDeleteDialog(plane) {
      this.selectedPlane = { ...plane };
      this.deleteDialog = true;
    },
    async handlePlaneDelete(planeId) {
      try {
        await apiClient.delete(`/planes/${planeId}/`);
        this.deleteDialog = false;
        await this.fetchPlanes();
      } catch (error) {
        console.error('Ошибка удаления самолёта:', error.response?.data || error.message);
      }
    },


    async fetchModels() {
      try {
        const response = await apiClient.get('/models/');
        this.availableModels = response.data.map(model => ({
          id: model.id,
          name: model.name,
        }));

        console.log('Дата:', response.data);

      } catch (error) {
        console.error('Ошибка получения моделей:', error.response?.data || error.message);
      }
    },
    async addPlane(planeData) {
      try {
        await apiClient.post('/planes/', planeData);
        await this.fetchPlanes();
      } catch (error) {
        console.error('Ошибка добавления самолёта:', error.response?.data || error.message);
      }
    },

    async fetchPlanes() {
      try {
        const response = await apiClient.get('/planes/');
        console.log('Самолеты из API:', response.data);

        this.planes = response.data.map(plane => ({
          id: plane.id,
          number: plane.number || 'Не указан',
          model_name: plane.model.name || 'Неизвестно',
          capacity: plane.model.seats_capacity || 'Не указана вместимость',
          modelSpeed: plane.model.speed || 'Не указана скорость',
        }));

        this.filterModels = [
          ...new Set(this.planes.map(plane => plane.model_name)),
        ];

      } catch (error) {
        console.error('Ошибка получения данных самолётов:', error.response?.data || error.message);
      }
    },

    openDialog() {
      console.log('Открытие модального окна');
      this.dialog = true;
  },

  },
  async created() {
    await this.fetchModels();
    await this.fetchPlanes();
  },

};
</script>


<style>
.text-center {
  text-align: center;
}


footer {
  text-align: center;
  padding: 10px;
  background-color: #f5f5f5;
  position: relative;
  bottom: 0;
  width: 100%;
}
</style>
