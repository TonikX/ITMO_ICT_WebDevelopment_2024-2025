<template>
  <v-container class="py-8">
    <v-row class="mb-8">
      <v-col cols="12">
        <h1 class="text-h3 font-weight-bold mb-2">Welcome to Publishing System</h1>
        <p class="text-grey">Manage your publications efficiently and seamlessly</p>
      </v-col>
    </v-row>

    <v-row class="mb-8">
      <v-col cols="12" md="6" lg="3">
        <v-card class="stat-card h-100" @click="$router.push('/newspapers')" style="cursor: pointer; background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%)">
          <v-card-text class="text-white">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-body-2 opacity-75">Total Newspapers</div>
                <div class="text-h3 font-weight-bold mt-1">{{ stats.newspapers }}</div>
              </div>
              <v-icon size="64" class="opacity-25">mdi-newspaper</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="stat-card h-100" @click="$router.push('/printing-houses')" style="cursor: pointer; background: linear-gradient(135deg, #EC4899 0%, #F472B6 100%)">
          <v-card-text class="text-white">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-body-2 opacity-75">Printing Houses</div>
                <div class="text-h3 font-weight-bold mt-1">{{ stats.printingHouses }}</div>
              </div>
              <v-icon size="64" class="opacity-25">mdi-factory</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="stat-card h-100" @click="$router.push('/post-offices')" style="cursor: pointer; background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%)">
          <v-card-text class="text-white">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-body-2 opacity-75">Post Offices</div>
                <div class="text-h3 font-weight-bold mt-1">{{ stats.postOffices }}</div>
              </div>
              <v-icon size="64" class="opacity-25">mdi-mailbox</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="stat-card h-100" @click="$router.push('/distributions')" style="cursor: pointer; background: linear-gradient(135deg, #10B981 0%, #34D399 100%)">
          <v-card-text class="text-white">
            <div class="d-flex align-center justify-space-between">
              <div>
                <div class="text-body-2 opacity-75">Distributions</div>
                <div class="text-h3 font-weight-bold mt-1">{{ stats.distributions }}</div>
              </div>
              <v-icon size="64" class="opacity-25">mdi-package-variant</v-icon>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mb-8">
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title class="text-h5 font-weight-bold">Quick Actions</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  size="large"
                  color="primary"
                  prepend-icon="mdi-plus-circle"
                  to="/newspapers?action=create"
                  class="font-weight-bold"
                >
                  Create Newspaper
                </v-btn>
              </v-col>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  size="large"
                  color="secondary"
                  prepend-icon="mdi-plus-circle"
                  to="/printing-houses?action=create"
                  class="font-weight-bold"
                >
                  Add Print House
                </v-btn>
              </v-col>
              <v-col cols="12" md="4">
                <v-btn
                  block
                  size="large"
                  color="accent"
                  prepend-icon="mdi-plus-circle"
                  to="/post-offices?action=create"
                  class="font-weight-bold"
                >
                  Create Post Office
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">
          <v-card-title class="text-h5 font-weight-bold d-flex align-center gap-2">
            <v-icon>mdi-chart-line</v-icon>
            Factory Report
          </v-card-title>
          <v-card-text>
            <v-btn
              color="primary"
              prepend-icon="mdi-download"
              @click="loadReport"
              :loading="loadingReport"
              class="mb-4"
            >
              Generate Report
            </v-btn>
            <div v-if="reportData.length > 0">
              <v-expansion-panels>
                <v-expansion-panel
                  v-for="(item, index) in reportData"
                  :key="index"
                >
                  <v-expansion-panel-title class="bg-surface">
                    <div>
                      <strong>{{ item.printing_house.name }}</strong>
                      <v-chip size="small" class="ml-2" color="primary" text-color="white">
                        {{ item.total_newspapers }} publications
                      </v-chip>
                    </div>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-table>
                      <thead>
                        <tr>
                          <th>Publication</th>
                          <th>Print Run</th>
                          <th>Distributed</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(newspaper, nIndex) in item.newspapers" :key="nIndex">
                          <td><strong>{{ newspaper.newspaper }}</strong></td>
                          <td>{{ newspaper.circulation }}</td>
                          <td>{{ newspaper.total_distributed }}</td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const stats = ref({
  newspapers: 0,
  printingHouses: 0,
  postOffices: 0,
  distributions: 0,
})

const reportData = ref<{
  printing_house: {
    name: string
  }
  total_newspapers: number
  newspapers: {
    newspaper: string
    circulation: number
    total_distributed: number
  }[]
}[]>([])
const loadingReport = ref(false)

async function loadStats() {
  try {
    const [newspapers, printingHouses, postOffices, distributions] = await Promise.all([
      api.getNewspapers({ page_size: 1 }),
      api.getPrintingHouses({ page_size: 1 }),
      api.getPostOffices({ page_size: 1 }),
      api.getDistributions({ page_size: 1 }),
    ])

    stats.value = {
      newspapers: newspapers.count || 0,
      printingHouses: printingHouses.count || 0,
      postOffices: postOffices.count || 0,
      distributions: distributions.count || 0,
    }
  } catch {
    console.error('Error loading statistics')
  }
}

async function loadReport() {
  loadingReport.value = true
  try {
    const data = await api.getPrintingHousesReport()
    reportData.value = data
  } catch {
    console.error('Error loading report')
  } finally {
    loadingReport.value = false
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stat-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15) !important;
}

.opacity-75 {
  opacity: 0.75;
}

.opacity-25 {
  opacity: 0.25;
}

.gap-2 {
  gap: 0.5rem;
}
</style>
