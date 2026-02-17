<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h3 font-weight-bold">Printing Houses</h1>
            <p class="text-grey mt-2">Manage all printing facilities</p>
          </div>
          <v-btn
            color="secondary"
            size="large"
            prepend-icon="mdi-plus-circle"
            @click="openCreateDialog"
            class="font-weight-bold"
          >
            New Factory
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2" rounded="lg">
          <v-data-table
            :headers="headers"
            :items="printingHouses"
            :loading="loading"
            :items-per-page="20"
            :server-items-length="totalCount"
            @update:options="loadPrintingHouses"
            class="custom-table"
          >
            <template v-slot:item.is_active="{ item }">
              <v-chip :color="item.is_active ? 'success' : 'error'" size="small" text-color="white">
                {{ item.is_active ? '✓ Active' : '✗ Inactive' }}
              </v-chip>
            </template>

            <template v-slot:item.actions="{ item }">
              <div class="d-flex gap-1">
                <v-btn
                  icon="mdi-eye"
                  size="x-small"
                  variant="text"
                  color="info"
                  @click="viewDetails(item)"
                  title="View"
                />
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
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">
            {{ editingItem ? '✎ Edit Factory' : '➕ New Factory' }}
          </h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-form ref="formRef">
            <v-text-field
              v-model="form.name"
              label="Factory Name"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-factory"
            />
            <v-text-field
              v-model="form.address"
              label="Address"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-map-marker"
            />
            <div class="d-flex align-center gap-3">
              <v-switch
                v-model="form.is_active"
                label="Active Status"
                color="success"
              />
              <v-chip :color="form.is_active ? 'success' : 'error'" text-color="white" size="small">
                {{ form.is_active ? 'Active' : 'Inactive' }}
              </v-chip>
            </div>
          </v-form>
        </v-card-text>

        <v-divider />

        <v-card-actions class="px-6 py-4 justify-end gap-2">
          <v-btn variant="text" @click="closeDialog">Cancel</v-btn>
          <v-btn color="secondary" @click="save" :loading="saving" class="font-weight-bold">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800px" rounded="lg">
      <v-card v-if="selectedItem" rounded="lg">
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #F97316 0%, #FB923C 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">🏭 Factory Details</h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-row>
            <v-col cols="12" md="6">
              <p class="text-grey text-body-2">NAME</p>
              <p class="text-h6 font-weight-bold">{{ selectedItem.name }}</p>
              
              <p class="text-grey text-body-2 mt-4">ADDRESS</p>
              <p class="text-h6 font-weight-bold">{{ selectedItem.address }}</p>
            </v-col>
            <v-col cols="12" md="6">
              <p class="text-grey text-body-2">STATUS</p>
              <v-chip :color="selectedItem.is_active ? 'success' : 'error'" text-color="white" size="small">
                {{ selectedItem.is_active ? '✓ Active' : '✗ Inactive' }}
              </v-chip>
            </v-col>
          </v-row>

          <v-divider class="my-6" />

          <div v-if="fullDetails">
            <h3 class="text-h6 font-weight-bold mb-4">📰 Print Runs</h3>
            <v-table v-if="fullDetails.printing_runs?.length" class="custom-table">
              <thead>
                <tr>
                  <th>Publication</th>
                  <th>Circulation</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="run in fullDetails.printing_runs" :key="run.id">
                  <td><strong>{{ run.newspaper.title }}</strong></td>
                  <td>{{ run.circulation }}</td>
                </tr>
              </tbody>
            </v-table>
            <v-alert v-else type="info" variant="tonal" rounded="lg">
              No print runs yet
            </v-alert>
          </div>
        </v-card-text>

        <v-divider />

        <v-card-actions class="px-6 py-4 justify-end">
          <v-btn variant="text" @click="detailsDialog = false">Close</v-btn>
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
          <p>Are you sure you want to delete this printing house?</p>
          <p v-if="itemToDelete" class="font-weight-bold text-h6 mt-4">
            "{{ itemToDelete.name }}"
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
import { ref, onMounted, reactive } from 'vue'
import api from '@/services/api'
import type { PrintingHouse, PrintingHouseFullDetail, PrintingHouseForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false, width: '60px' },
  { title: 'Name', key: 'name', sortable: false },
  { title: 'Address', key: 'address', sortable: false },
  { title: 'Status', key: 'is_active', sortable: false, width: '100px' },
  { title: 'Actions', key: 'actions', sortable: false, width: '100px' },
]

const printingHouses = ref<PrintingHouse[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const detailsDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<PrintingHouse | null>(null)
const selectedItem = ref<PrintingHouse | null>(null)
const fullDetails = ref<PrintingHouseFullDetail | null>(null)
const itemToDelete = ref<PrintingHouse | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<PrintingHouseForm>({
  name: '',
  address: '',
  is_active: true,
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'This field is required') as ValidationRule,
}

async function loadPrintingHouses(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getPrintingHouses(params)
    printingHouses.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Error loading printing houses')
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: PrintingHouse) {
  editingItem.value = item
  form.name = item.name
  form.address = item.address
  form.is_active = item.is_active
  dialog.value = true
}

function resetForm() {
  form.name = ''
  form.address = ''
  form.is_active = true
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
    if (editingItem.value) {
      await api.updatePrintingHouse(editingItem.value.id, form)
    } else {
      await api.createPrintingHouse(form)
    }
    closeDialog()
    loadPrintingHouses()
  } catch {
    console.error('Error saving printing house')
  } finally {
    saving.value = false
  }
}

async function viewDetails(item: PrintingHouse) {
  selectedItem.value = item
  try {
    fullDetails.value = await api.getPrintingHouseFullDetail(item.id)
  } catch {
    console.error('Error loading details')
  }
  detailsDialog.value = true
}

function confirmDelete(item: PrintingHouse) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deletePrintingHouse(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadPrintingHouses()
  } catch {
    console.error('Error deleting printing house')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadPrintingHouses({ page: 1, itemsPerPage: 20 })
})
</script>

<style scoped>
.gap-1 {
  gap: 0.25rem;
}

.gap-2 {
  gap: 0.5rem;
}

.gap-3 {
  gap: 0.75rem;
}

.dialog-header {
  border-radius: 8px 8px 0 0;
}

:deep(.custom-table tbody tr:hover) {
  background: rgba(236, 72, 153, 0.05);
}
</style>

