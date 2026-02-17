<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h3 font-weight-bold">Print Runs</h1>
            <p class="text-grey mt-2">Manage newspaper print runs and circulation</p>
          </div>
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-plus-circle"
            @click="openCreateDialog"
            class="font-weight-bold"
          >
            New Print Run
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2" rounded="lg">
          <v-data-table
            :headers="headers"
            :items="printingRuns"
            :loading="loading"
            :items-per-page="20"
            :server-items-length="totalCount"
            @update:options="loadPrintingRuns"
            class="custom-table"
          >
            <template v-slot:item.circulation="{ item }">
              <v-chip color="success" text-color="white" size="small">
                {{ item.circulation }} copies
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
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #10B981 0%, #34D399 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">
            {{ editingItem ? '✎ Edit Print Run' : '➕ New Print Run' }}
          </h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-form ref="formRef">
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
              v-model="form.circulation"
              label="Circulation"
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
          <p>Are you sure you want to delete this print run?</p>
          <p v-if="itemToDelete" class="font-weight-bold text-body-2 mt-4">
            Publication: {{ itemToDelete.newspaper_title }}<br>
            Printing House: {{ itemToDelete.printing_house_name }}<br>
            Circulation: {{ itemToDelete.circulation }}
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
import type { PrintingRun, Newspaper, PrintingHouse, PrintingRunForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false, width: '60px' },
  { title: 'Publication', key: 'newspaper_title', sortable: false },
  { title: 'Printing House', key: 'printing_house_name', sortable: false },
  { title: 'Circulation', key: 'circulation', sortable: false, width: '150px' },
  { title: 'Actions', key: 'actions', sortable: false, width: '100px' },
]

const printingRuns = ref<PrintingRun[]>([])
const newspapers = ref<Newspaper[]>([])
const printingHouses = ref<PrintingHouse[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<PrintingRun | null>(null)
const itemToDelete = ref<PrintingRun | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<PrintingRunForm>({
  newspaper: null,
  printing_house: null,
  circulation: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'This field is required') as ValidationRule,
  positive: ((v: string | number | null | undefined) => {
    const num = typeof v === 'string' ? Number.parseInt(v) : v
    return (num && num > 0) || 'Value must be positive'
  }) as ValidationRule,
}

async function loadPrintingRuns(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getPrintingRuns(params)
    printingRuns.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Error loading print runs')
  } finally {
    loading.value = false
  }
}

async function loadSelectData() {
  try {
    const [newspapersData, printingHousesData] = await Promise.all([
      api.getNewspapers({ page_size: 1000 }),
      api.getPrintingHouses({ page_size: 1000 }),
    ])

    newspapers.value = newspapersData.results || []
    printingHouses.value = printingHousesData.results || []
  } catch {
    console.error('Error loading reference data')
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: PrintingRun) {
  editingItem.value = item
  form.newspaper = item.newspaper_id
  form.printing_house = item.printing_house_id
  form.circulation = item.circulation.toString()
  dialog.value = true
}

function resetForm() {
  form.newspaper = null
  form.printing_house = null
  form.circulation = ''
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
      newspaper_id: form.newspaper!,
      printing_house_id: form.printing_house!,
      circulation: Number.parseInt(form.circulation),
    }

    if (editingItem.value) {
      await api.updatePrintingRun(editingItem.value.id, { circulation: data.circulation })
    } else {
      await api.createPrintingRun(data)
    }
    closeDialog()
    loadPrintingRuns()
  } catch {
    console.error('Error saving print run')
  } finally {
    saving.value = false
  }
}

function confirmDelete(item: PrintingRun) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deletePrintingRun(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadPrintingRuns()
  } catch {
    console.error('Error deleting print run')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadPrintingRuns({ page: 1, itemsPerPage: 20 })
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
  background: rgba(16, 185, 129, 0.05);
}
</style>
