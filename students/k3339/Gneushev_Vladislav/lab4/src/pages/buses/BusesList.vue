<template>
  <page-wrapper>
    <div class="mb-4 d-flex justify-space-between align-center">
      <h1 class="text-h4">Список автобусов</h1>
      <v-btn
        color="primary"
        prepend-icon="mdi-plus"
        to="/buses/add"
      >
        ДОБАВИТЬ АВТОБУС
      </v-btn>
    </div>

    <v-card>
      <v-table hover>
        <thead>
          <tr>
            <th class="text-left pa-4">Гос. номер</th>
            <th class="text-left pa-4">Тип автобуса</th>
            <th class="text-left pa-4">Вместимость</th>
            <th class="text-center pa-4">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bus in buses" :key="bus.id">
            <td class="pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-text-field
                  v-model="editForm.state_number"
                  density="compact"
                  hide-details
                  :rules="[v => !!v || 'Обязательное поле']"
                ></v-text-field>
              </template>
              <template v-else>
                {{ bus.state_number }}
              </template>
            </td>
            <td class="pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-select
                  v-model="editForm.bus_type_id"
                  :items="busTypes"
                  item-title="name"
                  item-value="id"
                  density="compact"
                  hide-details
                  :rules="[v => !!v || 'Обязательное поле']"
                ></v-select>
              </template>
              <template v-else>
                {{ bus.bus_type.name }}
              </template>
            </td>
            <td class="pa-4">
              {{ getBusTypeCapacity(bus) }} чел.
            </td>
            <td class="text-center pa-4">
              <template v-if="editingBus?.id === bus.id">
                <v-btn
                  icon
                  variant="text"
                  color="success"
                  class="mr-2"
                  @click="saveEdit"
                  :loading="saving"
                  :disabled="!isValidForm"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="cancelEdit"
                >
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </template>
              <template v-else>
                <v-btn
                  icon
                  variant="text"
                  color="primary"
                  class="mr-2"
                  @click="startEdit(bus)"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  color="error"
                  @click="confirmDelete(bus)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </td>
          </tr>
        </tbody>
      </v-table>

      <v-overlay
        :model-value="loading"
        class="align-center justify-center"
      >
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-overlay>
    </v-card>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы действительно хотите удалить автобус {{ selectedBus?.state_number }}?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">
            Отмена
          </v-btn>
          <v-btn 
            color="error" 
            variant="text" 
            @click="deleteBus"
            :loading="deleting"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </page-wrapper>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'BusesList',
  
  components: {
    PageWrapper
  },

  data: () => ({
    buses: [],
    busTypes: [],
    loading: true,
    deleting: false,
    saving: false,
    showDeleteDialog: false,
    showError: false,
    errorMessage: '',
    selectedBus: null,
    editingBus: null,
    editForm: {
      state_number: '',
      bus_type_id: null
    }
  }),

  computed: {
    isValidForm() {
      return this.editForm.state_number && this.editForm.bus_type_id
    }
  },

  async created() {
    await Promise.all([
      this.fetchBuses(),
      this.fetchBusTypes()
    ])
  },

  methods: {
    async fetchBuses() {
      try {
        const { data } = await api.get('/buses')
        this.buses = data
      } catch (error) {
        console.error('Error loading buses:', error)
        this.errorMessage = 'Ошибка при загрузке списка автобусов'
        this.showError = true
      } finally {
        this.loading = false
      }
    },

    async fetchBusTypes() {
      try {
        const { data } = await api.get('/buses/types')
        this.busTypes = data
      } catch (error) {
        console.error('Error loading bus types:', error)
        this.errorMessage = 'Ошибка при загрузке типов автобусов'
        this.showError = true
      }
    },

    getBusTypeCapacity(bus) {
      return bus.bus_type.people_capacity
    },

    startEdit(bus) {
      this.editingBus = bus
      this.editForm = {
        state_number: bus.state_number,
        bus_type_id: bus.bus_type.id
      }
    },

    cancelEdit() {
      this.editingBus = null
      this.editForm = {
        state_number: '',
        bus_type_id: null
      }
    },

    async saveEdit() {
      if (!this.editingBus || !this.isValidForm) return

      this.saving = true
      try {
        await api.put(`/buses/${this.editingBus.id}`, this.editForm)
        await this.fetchBuses()
        this.cancelEdit()
      } catch (error) {
        console.error('Error updating bus:', error)
        this.errorMessage = 'Ошибка при обновлении автобуса'
        this.showError = true
      } finally {
        this.saving = false
      }
    },

    confirmDelete(bus) {
      this.selectedBus = bus
      this.showDeleteDialog = true
    },

    async deleteBus() {
      if (!this.selectedBus) return

      this.deleting = true
      try {
        await api.delete(`/buses/${this.selectedBus.id}`)
        await this.fetchBuses()
        this.showDeleteDialog = false
      } catch (error) {
        console.error('Error deleting bus:', error)
        this.errorMessage = 'Ошибка при удалении автобуса'
        this.showError = true
      } finally {
        this.deleting = false
      }
    }
  }
}
</script> 