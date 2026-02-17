<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h3 font-weight-bold">Distributions</h1>
            <p class="text-grey mt-2">Manage newspaper distributions to post offices</p>
          </div>
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-plus-circle"
            @click="openCreateDialog"
            class="font-weight-bold"
          >
            New Distribution
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2" rounded="lg">
          <v-data-table
            :headers="headers"
            :items="distributions"
            :loading="loading"
            :items-per-page="20"
            :server-items-length="totalCount"
            @update:options="loadDistributions"
            class="custom-table"
          >
            <template v-slot:item.quantity="{ item }">
              <v-chip color="info" text-color="white" size="small">
                {{ item.quantity }} units
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <div class="d-flex gap-1">
                <v-btn
                  icon="mdi-pencil"
                  size="x-small"
                  variant="text"
                  color="warning"
                  @click="openEditDialog(item)"
                  title="Edit"
                />
                <v-btn
                  icon="mdi-delete"
                  size="x-small"
                  variant="text"
                  color="error"
                  @click="confirmDelete(item)"
                  title="Delete"
                />
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create/Edit Dialog -->
    <v-dialog v-model="dialog" max-width="600px" persistent rounded="lg">
      <v-card rounded="lg">
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">
            {{ editingItem ? '✎ Edit Distribution' : '➕ New Distribution' }}
          </h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-form ref="formRef">
            <v-select
              v-model="form.post_office"
              :items="postOfficesForSelect"
              item-title="display"
              item-value="id"
              label="Post Office"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-mailbox"
            />
            <v-select
              v-model="form.newspaper"
              :items="newspapers"
              item-title="title"
              item-value="id"
              label="Publication"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-newspaper"
            />
            <v-select
              v-model="form.printing_house"
              :items="printingHouses"
              item-title="name"
              item-value="id"
              label="Printing House"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-factory"
            />
            <v-text-field
              v-model="form.quantity"
              label="Quantity"
              type="number"
              :rules="[rules.required, rules.positive]"
              variant="outlined"
              prepend-inner-icon="mdi-counter"
            />
          </v-form>
        </v-card-text>

        <v-divider />

        <v-card-actions class="px-6 py-4 justify-end gap-2">
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn color="primary" @click="save" :loading="saving" class="font-weight-bold">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px" rounded="lg">
      <v-card rounded="lg">
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #EF4444 0%, #FCA5A5 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">⚠️ Confirm Deletion</h2>
        </div>

        <v-card-text class="px-6 py-5">
          <p>Are you sure you want to delete this distribution?</p>
          <p v-if="itemToDelete" class="font-weight-bold text-body-2 mt-4">
            Post Office: {{ postOffices.find(p => p.id === itemToDelete.post_office)?.number }}<br>
            Publication: {{ newspapers.find(n => n.id === itemToDelete.newspaper)?.title }}<br>
            Quantity: {{ itemToDelete.quantity }}
          </p>
        </v-card-text>

        <v-divider />

        <v-card-actions class="px-6 py-4 justify-end gap-2">
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteItem" :loading="deleting" class="font-weight-bold">
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import api from '@/services/api'
import type { Distribution, Newspaper, PrintingHouse, PostOffice, DistributionForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false, width: '60px' },
  { title: 'Post Office', key: 'post_office_number', sortable: false },
  { title: 'Publication', key: 'newspaper_title', sortable: false },
  { title: 'Factory', key: 'printing_house_name', sortable: false },
  { title: 'Quantity', key: 'quantity', sortable: false, width: '120px' },
  { title: 'Actions', key: 'actions', sortable: false, width: '100px' },
]

const distributions = ref<Distribution[]>([])
const newspapers = ref<Newspaper[]>([])
const printingHouses = ref<PrintingHouse[]>([])
const postOffices = ref<PostOffice[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<Distribution | null>(null)
const itemToDelete = ref<Distribution | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<DistributionForm>({
  post_office: null,
  newspaper: null,
  printing_house: null,
  quantity: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'This field is required') as ValidationRule,
  positive: ((v: string | number | null | undefined) => {
    const num = typeof v === 'string' ? Number.parseInt(v) : v
    return (num && num > 0) || 'Value must be positive'
  }) as ValidationRule,
}

const postOfficesForSelect = computed(() => {
  return postOffices.value.map(po => ({
    id: po.id,
    display: `${po.number} - ${po.address}`,
  }))
})

async function loadDistributions(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getDistributions(params)
    distributions.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Error loading distributions')
  } finally {
    loading.value = false
  }
}

async function loadSelectData() {
  try {
    const [newspapersData, printingHousesData, postOfficesData] = await Promise.all([
      api.getNewspapers({ page_size: 1000 }),
      api.getPrintingHouses({ page_size: 1000 }),
      api.getPostOffices({ page_size: 1000 }),
    ])

    newspapers.value = newspapersData.results || []
    printingHouses.value = printingHousesData.results || []
    postOffices.value = postOfficesData.results || []
  } catch {
    console.error('Error loading reference data')
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: Distribution) {
  editingItem.value = item
  form.post_office = item.post_office_id
  form.newspaper = item.newspaper_id
  form.printing_house = item.printing_house_id
  form.quantity = item.quantity.toString()
  dialog.value = true
}

function resetForm() {
  form.post_office = null
  form.newspaper = null
  form.printing_house = null
  form.quantity = ''
}

function closeDialog() {
  dialog.value = false
  editingItem.value = null
  resetForm()
}

async function save() {
  if (!formRef.value) return
  const { valid } = await formRef.value.validate()
  if (!valid) return

  saving.value = true
  try {
    const data = {
      post_office: form.post_office!,
      newspaper: form.newspaper!,
      printing_house: form.printing_house!,
      quantity: Number.parseInt(form.quantity),
    }

    if (editingItem.value) {
      await api.updateDistribution(editingItem.value.id, data)
    } else {
      await api.createDistribution(data)
    }
    closeDialog()
    loadDistributions()
  } catch {
    console.error('Error saving distribution')
  } finally {
    saving.value = false
  }
}

function confirmDelete(item: Distribution) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deleteDistribution(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadDistributions()
  } catch {
    console.error('Error deleting distribution')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadDistributions({ page: 1, itemsPerPage: 20 })
  loadSelectData()
})
</script>

<style scoped>
.gap-1 {
  gap: 0.25rem;
}

.gap-2 {
  gap: 0.5rem;
}

.dialog-header {
  border-radius: 8px 8px 0 0;
}

:deep(.custom-table tbody tr:hover) {
  background: rgba(124, 58, 237, 0.05);
}
</style>

