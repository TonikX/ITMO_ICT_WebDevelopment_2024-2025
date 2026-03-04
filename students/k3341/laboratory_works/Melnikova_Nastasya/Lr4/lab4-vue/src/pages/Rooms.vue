<template>
  <div class="d-flex align-center mb-5">
    <div>
      <h1 class="text-h5 font-weight-bold">Rooms</h1>
      <div class="text-medium-emphasis">
        Browse and book available rooms
      </div>
    </div>

    <v-spacer />

    <v-switch
      v-model="onlyFree"
      inset
      color="primary"
      label="Only free rooms"
    />
  </div>

  <v-progress-linear v-if="loading" indeterminate class="mb-4" />

  <v-alert
    v-if="error"
    type="error"
    variant="tonal"
    class="mb-4"
  >
    {{ error }}
  </v-alert>

  <v-row>
    <v-col
      v-for="room in rooms"
      :key="room.id"
      cols="12"
      md="6"
      lg="4"
    >
      <v-card class="roomCard">

        <!-- HEADER -->
        <div class="top">
          <div>
            <div class="title">Room {{ room.number }}</div>

            <div class="sub text-medium-emphasis">
              Floor {{ room.floor }} • {{ roomType(room.room_type) }}
            </div>
          </div>

          <div class="price">
            {{ formatPrice(room.price_per_day) }}
            <div class="priceSub">per day</div>
          </div>
        </div>

        <v-divider />

        <!-- BODY -->
        <div class="body">

          <div class="typeIcon">
            {{ roomIcon(room.room_type) }}
          </div>

          <div class="actions">
            <v-btn
              color="primary"
              size="large"
              class="pill"
              @click="goBook(room.id)"
            >
              Book
            </v-btn>
          </div>

        </div>

      </v-card>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"
import { roomsApi } from "../api/rooms"

const router = useRouter()

const rooms = ref([])
const loading = ref(false)
const error = ref("")

const onlyFree = ref(true)

function roomIcon(type) {
  if (type === "single") return "🛏 Single"
  if (type === "double") return "🛏🛏 Double"
  if (type === "triple") return "🛏🛏🛏 Triple"
  return type
}

function roomType(type) {
  if (type === "single") return "Single"
  if (type === "double") return "Double"
  if (type === "triple") return "Triple"
  return type
}

function formatPrice(price) {
  return `${Number(price).toFixed(2)} ₽`
}

async function loadRooms() {
  loading.value = true
  error.value = ""

  try {
    const res = onlyFree.value
      ? await roomsApi.free()
      : await roomsApi.list()

    rooms.value = res.data
  } catch (e) {
    error.value = "Failed to load rooms"
  } finally {
    loading.value = false
  }
}

function goBook(roomId) {
  router.push({
    path: "/stays",
    query: { room: roomId }
  })
}

onMounted(loadRooms)
watch(onlyFree, loadRooms)
</script>

<style scoped>

.roomCard {
  border-radius: 18px;
  padding: 18px;
  transition: 0.2s;
}

.roomCard:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 30px rgba(0,0,0,0.10);
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title {
  font-size: 20px;
  font-weight: 700;
}

.sub {
  font-size: 14px;
}

.price {
  font-size: 20px;
  font-weight: 800;
  text-align: right;
}

.priceSub {
  font-size: 12px;
  color: #777;
}

.body {
  margin-top: 14px;
}

.typeIcon {
  font-size: 18px;
  margin-bottom: 16px;
}

.actions {
  display: flex;
}

.pill {
  border-radius: 999px;
}

</style>