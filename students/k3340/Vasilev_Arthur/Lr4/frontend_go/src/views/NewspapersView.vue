<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h1 class="text-h3 font-weight-bold">Publications</h1>
            <p class="text-grey mt-2">Manage all newspapers and publications</p>
          </div>
          <v-btn
            color="primary"
            size="large"
            prepend-icon="mdi-plus-circle"
            @click="openCreateDialog"
            class="font-weight-bold"
          >
            New Publication
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2" rounded="lg">
          <v-data-table
            :headers="headers"
            :items="newspapers"
            :loading="loading"
            :items-per-page="20"
            :server-items-length="totalCount"
            @update:options="loadNewspapers"
            class="custom-table"
          >
            <template v-slot:item.price_per_copy="{ item }">
              <v-chip color="success" text-color="white" size="small">
                ₽{{ item.price_per_copy }}
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
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">
            {{ editingItem ? '✎ Edit Publication' : '➕ New Publication' }}
          </h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-form ref="formRef">
            <v-text-field
              v-model="form.title"
              label="Title"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-newspaper"
            />
            <v-text-field
              v-model="form.publication_index"
              label="Publication Index"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-hashtag"
            />
            <v-text-field
              v-model="form.editor_first_name"
              label="Editor First Name"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-account"
            />
            <v-text-field
              v-model="form.editor_last_name"
              label="Editor Last Name"
              :rules="[rules.required]"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-account"
            />
            <v-text-field
              v-model="form.editor_middle_name"
              label="Editor Middle Name"
              variant="outlined"
              class="mb-4"
              prepend-inner-icon="mdi-account"
            />
            <v-text-field
              v-model="form.price_per_copy"
              label="Price per Copy (₽)"
              type="number"
              :rules="[rules.required, rules.positive]"
              variant="outlined"
              prepend-inner-icon="mdi-currency-rub"
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

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog" max-width="800px" rounded="lg">
      <v-card v-if="selectedItem" rounded="lg">
        <div class="dialog-header px-6 py-5" style="background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%); color: white; border-radius: 8px 8px 0 0;">
          <h2 class="text-h5 font-weight-bold">📄 Publication Details</h2>
        </div>

        <v-card-text class="px-6 py-5">
          <v-row>
            <v-col cols="12" md="6">
              <p class="text-grey text-body-2">TITLE</p>
              <p class="text-h6 font-weight-bold">{{ selectedItem.title }}</p>
              
              <p class="text-grey text-body-2 mt-4">PUBLICATION INDEX</p>
              <p class="text-h6 font-weight-bold">{{ selectedItem.publication_index }}</p>
              
              <p class="text-grey text-body-2 mt-4">PRICE</p>
              <v-chip color="success" text-color="white">₽{{ selectedItem.price_per_copy }}</v-chip>
            </v-col>
            <v-col cols="12" md="6">
              <p class="text-grey text-body-2">EDITOR</p>
              <p class="text-h6 font-weight-bold">{{ selectedItem.editor_full_name }}</p>
            </v-col>
          </v-row>

          <v-divider class="my-6" />

          <div v-if="fullDetails">
            <h3 class="text-h6 font-weight-bold mb-4">📊 Print Runs</h3>
            <v-table v-if="fullDetails.printing_runs?.length" class="custom-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Circulation</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="run in fullDetails.printing_runs" :key="run.id">
                  <td>{{ run.id }}</td>
                  <td><strong>{{ run.circulation }}</strong></td>
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
          <p>Are you sure you want to delete the publication?</p>
          <p v-if="itemToDelete" class="font-weight-bold text-h6 mt-4">
            "{{ itemToDelete.title }}"
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
import type { Newspaper, NewspaperFullDetail, NewspaperForm, TableOptions, ValidationRule } from '@/types'

const headers = [
  { title: 'ID', key: 'id', sortable: false, width: '60px' },
  { title: 'Title', key: 'title', sortable: false },
  { title: 'Index', key: 'publication_index', sortable: false },
  { title: 'Editor', key: 'editor_full_name', sortable: false },
  { title: 'Price', key: 'price_per_copy', sortable: false, width: '100px' },
  { title: 'Actions', key: 'actions', sortable: false, width: '100px' },
]

const newspapers = ref<Newspaper[]>([])
const loading = ref(false)
const totalCount = ref(0)
const dialog = ref(false)
const detailsDialog = ref(false)
const deleteDialog = ref(false)
const saving = ref(false)
const deleting = ref(false)
const editingItem = ref<Newspaper | null>(null)
const selectedItem = ref<Newspaper | null>(null)
const fullDetails = ref<NewspaperFullDetail | null>(null)
const itemToDelete = ref<Newspaper | null>(null)
const formRef = ref<{ validate: () => Promise<{ valid: boolean }> }>()

const form = reactive<NewspaperForm>({
  title: '',
  publication_index: '',
  editor_first_name: '',
  editor_last_name: '',
  editor_middle_name: '',
  price_per_copy: '',
})

const rules = {
  required: ((v: string | number | null | undefined) => !!v || 'This field is required') as ValidationRule,
  positive: ((v: string | number | null | undefined) => {
    const num = typeof v === 'string' ? Number.parseFloat(v) : v
    return (num && num > 0) || 'Value must be positive'
  }) as ValidationRule,
}

async function loadNewspapers(options?: TableOptions) {
  loading.value = true
  try {
    const params: { page?: number; page_size?: number } = {}
    if (options?.page) params.page = options.page
    if (options?.itemsPerPage) params.page_size = options.itemsPerPage

    const data = await api.getNewspapers(params)
    newspapers.value = data.results || []
    totalCount.value = data.count || 0
  } catch {
    console.error('Error loading publications')
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  editingItem.value = null
  resetForm()
  dialog.value = true
}

function openEditDialog(item: Newspaper) {
  editingItem.value = item
  form.title = item.title
  form.publication_index = item.publication_index
  form.editor_first_name = item.editor_first_name
  form.editor_last_name = item.editor_last_name
  form.editor_middle_name = item.editor_middle_name || ''
  form.price_per_copy = item.price_per_copy
  dialog.value = true
}

function resetForm() {
  form.title = ''
  form.publication_index = ''
  form.editor_first_name = ''
  form.editor_last_name = ''
  form.editor_middle_name = ''
  form.price_per_copy = ''
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
      await api.updateNewspaper(editingItem.value.id, form)
    } else {
      await api.createNewspaper(form)
    }
    closeDialog()
    loadNewspapers()
  } catch {
    console.error('Error saving publication')
  } finally {
    saving.value = false
  }
}

async function viewDetails(item: Newspaper) {
  selectedItem.value = item
  try {
    fullDetails.value = await api.getNewspaperFullDetail(item.id)
  } catch {
    console.error('Error loading details')
  }
  detailsDialog.value = true
}

function confirmDelete(item: Newspaper) {
  itemToDelete.value = item
  deleteDialog.value = true
}

async function deleteItem() {
  if (!itemToDelete.value) return

  deleting.value = true
  try {
    await api.deleteNewspaper(itemToDelete.value.id)
    deleteDialog.value = false
    itemToDelete.value = null
    loadNewspapers()
  } catch {
    console.error('Error deleting publication')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadNewspapers({ page: 1, itemsPerPage: 20 })
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

