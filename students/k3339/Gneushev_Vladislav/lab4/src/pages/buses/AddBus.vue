<template>
  <page-wrapper>
    <v-card>
      <v-card-title>Добавление автобуса</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="form.state_number"
            label="Государственный номер"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-select
            v-model="form.bus_type_id"
            :items="busTypes"
            item-title="name"
            item-value="id"
            label="Тип автобуса"
            :rules="[v => !!v || 'Обязательное поле']"
            :loading="loadingTypes"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <v-list-item-title>
                  {{ item.raw.name }} ({{ item.raw.people_capacity }} чел.)
                </v-list-item-title>
              </v-list-item>
            </template>
            <template v-slot:selection="{ item }">
              {{ item.title }} ({{ item.raw.people_capacity }} чел.)
            </template>
          </v-select>

          <div class="d-flex justify-end mt-4">
            <v-btn
              color="grey"
              variant="text"
              class="mr-2"
              to="/buses"
            >
              Отмена
            </v-btn>
            <v-btn
              color="primary"
              type="submit"
              :loading="saving"
              :disabled="!isValid"
            >
              Сохранить
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

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
  name: 'AddBus',
  
  components: {
    PageWrapper
  },

  data: () => ({
    form: {
      state_number: '',
      bus_type_id: null
    },
    busTypes: [],
    loading: false,
    loadingTypes: true,
    saving: false,
    showError: false,
    errorMessage: ''
  }),

  computed: {
    isValid() {
      return this.form.state_number && this.form.bus_type_id
    }
  },

  async created() {
    await this.fetchBusTypes()
  },

  methods: {
    async fetchBusTypes() {
      try {
        const { data } = await api.get('/buses/types')
        this.busTypes = data
      } catch (error) {
        console.error('Error loading bus types:', error)
        this.errorMessage = 'Ошибка при загрузке типов автобусов'
        this.showError = true
      } finally {
        this.loadingTypes = false
      }
    },

    async handleSubmit() {
      if (!this.isValid) return

      this.saving = true
      try {
        await api.post('/buses', this.form)
        this.$router.push('/buses')
      } catch (error) {
        console.error('Error saving bus:', error)
        this.errorMessage = 'Ошибка при сохранении автобуса'
        this.showError = true
      } finally {
        this.saving = false
      }
    }
  }
}
</script> 