<template>
  <div class="d-flex align-center mb-6">
    <div>
      <h1 class="text-h5 font-weight-bold">Find free rooms</h1>
      <div class="text-medium-emphasis">
        Choose dates and we’ll show only available rooms
      </div>
    </div>
  </div>

  <v-card class="pa-5 rounded-xl mb-6" variant="tonal">
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="checkIn"
          type="date"
          label="Check-in"
          :min="today"
        />
      </v-col>

      <v-col cols="12" md="4">
        <v-text-field
          v-model="checkOut"
          type="date"
          label="Check-out"
          :min="checkIn || today"
        />
      </v-col>

      <v-col cols="12" md="4" class="d-flex align-center">
        <v-btn
          color="primary"
          size="large"
          class="pill w-100"
          :loading="loading"
          @click="search"
        >
          Search free rooms
        </v-btn>
      </v-col>
    </v-row>

    <v-alert v-if="err" type="error" variant="tonal" class="mt-3">
      {{ err }}
    </v-alert>
  </v-card>

  <v-row v-if="rooms.length">
    <v-col v-for="r in rooms" :key="r.id" cols="12" md="4">
      <v-card class="room-card rounded-xl">

        <v-card-title class="d-flex justify-space-between align-start">
          <div>
            <div class="text-h6 font-weight-bold">
              Room {{ r.number }}
            </div>

            <div class="meta">
              <span>Floor {{ r.floor }}</span>
              <span>•</span>
              <span class="beds">{{ bedsLabel(r) }}</span>
            </div>
          </div>

          <div class="text-right">
            <div class="price">
              <span class="amount">{{ formatMoney(getPrice(r)) }} ₽</span>
              <div class="per">per day</div>
            </div>
          </div>
        </v-card-title>

        <v-divider />

        <v-card-actions class="pa-4">
          <v-btn
            color="primary"
            class="pill"
            @click="goBook(r.id)"
          >
            Book
          </v-btn>

          <v-spacer />

          <v-chip variant="tonal" color="primary">
            Free for selected dates ✅
          </v-chip>
        </v-card-actions>

      </v-card>
    </v-col>
  </v-row>

  <v-alert
    v-else
    type="info"
    variant="tonal"
    class="mt-4"
  >
    Pick dates and press “Search free rooms”.
  </v-alert>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { roomsApi } from "../api/rooms";

const router = useRouter();

const today = new Date().toISOString().slice(0, 10);

const checkIn = ref(today);
const checkOut = ref(today);

const rooms = ref([]);

const loading = ref(false);
const err = ref("");

function bedsLabel(room) {
  const t = String(room.type || "").toLowerCase();

  if (t.includes("single")) return "🛏 Single";
  if (t.includes("double")) return "🛏🛏 Double";
  if (t.includes("triple")) return "🛏🛏🛏 Triple";

  return room.type || "—";
}

function getPrice(room) {
  return (
    room.price ??
    room.price_per_day ??
    room.cost ??
    0
  );
}

function formatMoney(n) {
  return Number(n || 0).toLocaleString("ru-RU");
}

function goBook(roomId) {
  router.push({
    path: "/stays",
    query: { room: roomId }
  });
}

async function search() {
  err.value = "";
  rooms.value = [];

  if (!checkIn.value || !checkOut.value) {
    err.value = "Please select both dates.";
    return;
  }

  if (checkOut.value < checkIn.value) {
    err.value = "Check-out can’t be earlier than check-in.";
    return;
  }

  loading.value = true;

  try {
    const res = await roomsApi.free({
      check_in: checkIn.value,
      check_out: checkOut.value
    });

    rooms.value = res.data;

    if (!rooms.value.length) {
      err.value = "No free rooms for these dates 😢";
    }

  } catch (e) {
    err.value = "Server error while loading free rooms.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>

.rounded-xl {
  border-radius: 18px;
}

.pill {
  border-radius: 999px;
}

.room-card {
  transition: transform .15s ease, box-shadow .15s ease;
}

.room-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.meta {
  color: #6b7280;
  font-size: 14px;
}

.beds {
  font-weight: 500;
}

.price .amount {
  font-size: 20px;
  font-weight: 700;
}

.price .per {
  font-size: 12px;
  color: #777;
}

</style>