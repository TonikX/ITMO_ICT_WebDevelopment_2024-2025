<template>
  <div class="d-flex align-center mb-5">
    <div>
      <h1 class="text-h5 font-weight-bold">Book a room</h1>
      <div class="text-medium-emphasis">Create guest + stay</div>
    </div>
    <v-spacer />
    <v-btn color="primary" size="large" class="pill" @click="openDialog()">
      Book room
    </v-btn>
  </div>

  <!-- ✅ Мои бронирования -->
  <v-card class="rounded-xl pa-4 mb-6" variant="tonal">
    <div class="d-flex align-center mb-3">
      <div class="text-subtitle-1 font-weight-medium">My bookings</div>
      <v-spacer />
      <v-btn variant="text" :loading="loadingMy" @click="loadMyBookings">
        Reload
      </v-btn>
    </div>

    <v-alert v-if="myErr" type="error" variant="tonal" class="mb-3">
      {{ myErr }}
    </v-alert>

    <v-alert v-if="!loadingMy && myBookings.length === 0 && !myErr" type="info" variant="tonal">
      You don’t have bookings yet.
    </v-alert>

    <v-table v-if="myBookings.length" density="comfortable">
      <thead>
        <tr>
          <th class="text-left">Room</th>
          <th class="text-left">Check-in</th>
          <th class="text-left">Check-out</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in myBookings" :key="b.id">
          <td>
            <v-chip color="primary" variant="flat" class="pill">
              Room {{ roomLabel(b.room) }}
            </v-chip>
          </td>
          <td>{{ b.check_in }}</td>
          <td>{{ b.check_out }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-card>

  <v-alert v-if="globalOk" type="success" variant="tonal" class="mb-4">
    {{ globalOk }}
  </v-alert>

  <!-- Диалог бронирования -->
  <v-dialog v-model="dialog" max-width="920">
    <v-card class="rounded-xl">
      <v-card-title class="d-flex align-center">
        <span class="text-h6">Booking</span>
        <v-spacer />
        <v-btn icon="mdi-close" variant="text" @click="dialog=false" />
      </v-card-title>

      <v-divider />

      <v-card-text>
        <v-alert v-if="bookErr" type="error" variant="tonal" class="mb-4" style="white-space: pre-line;">
          {{ bookErr }}
        </v-alert>

        <v-row>
          <v-col cols="12" md="6">
            <v-card variant="tonal" class="rounded-xl pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-3">Guest</div>

              <v-text-field v-model="guest.last_name" label="Last name" />
              <v-text-field v-model="guest.first_name" label="First name" />
              <v-text-field v-model="guest.middle_name" label="Middle name (optional)" />
              <v-text-field v-model="guest.city_from" label="City from" />
              <v-text-field v-model="guest.passport_number" label="Passport number (unique)" />
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card variant="tonal" class="rounded-xl pa-4">
              <div class="text-subtitle-1 font-weight-medium mb-3">Stay</div>

              <v-switch v-model="onlyFreeRooms" inset color="primary" label="Show only free rooms" />

              <v-select
                v-model="stay.room"
                :items="rooms"
                item-title="number"
                item-value="id"
                label="Room"
              />

              <v-text-field v-model="stay.check_in" type="date" label="Check-in date" />
              <v-text-field v-model="stay.check_out" type="date" label="Check-out date" />
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>

      <v-divider />

      <v-card-actions class="pa-4">
        <v-btn variant="tonal" class="pill" @click="resetForm">Reset</v-btn>
        <v-spacer />
        <v-btn color="primary" class="pill" :loading="booking" @click="book">
          Book
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import { roomsApi } from "../api/rooms";
import { guestsApi } from "../api/guests";
import { staysApi } from "../api/stays";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const auth = useAuthStore();

const dialog = ref(false);

const rooms = ref([]);
const onlyFreeRooms = ref(true);

const booking = ref(false);
const bookErr = ref("");
const globalOk = ref("");

const guest = ref({
  passport_number: "",
  last_name: "",
  first_name: "",
  middle_name: "",
  city_from: "",
});

const stay = ref({
  room: null,
  check_in: "",
  check_out: "",
});

/** ---------- My bookings --------- */
const loadingMy = ref(false);
const myErr = ref("");
const myBookings = ref([]);

// Мапа id комнаты -> номер (101/102/201)
const roomsMap = computed(() => {
  const m = new Map();
  rooms.value.forEach(r => m.set(r.id, r.number));
  return m;
});

function roomLabel(roomValue) {
  // room может быть id (число) или объект — зависит от твоего бэка/сериализатора
  if (roomValue && typeof roomValue === "object") {
    return roomValue.number ?? roomValue.id ?? "?";
  }
  return roomsMap.value.get(roomValue) ?? roomValue ?? "?";
}

function normalizeDate(d) {
  if (!d) return d;
  if (/^\d{2}\.\d{2}\.\d{4}$/.test(d)) {
    const [dd, mm, yyyy] = d.split(".");
    return `${yyyy}-${mm}-${dd}`;
  }
  return d;
}

function niceError(e) {
  const data = e?.response?.data;
  if (!data) return "Server error";
  if (typeof data === "string") {
    if (data.includes("<!DOCTYPE html>") || data.includes("<html")) {
      return "Server error (Django returned HTML). Check Django console / Network → Response.";
    }
    return data;
  }
  return Object.entries(data)
    .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(" ") : String(v)}`)
    .join("\n");
}

async function loadRooms() {
  const res = onlyFreeRooms.value ? await roomsApi.free() : await roomsApi.list();
  rooms.value = res.data;
}

async function loadMyBookings() {
  myErr.value = "";
  loadingMy.value = true;
  try {
    // 1) тянем все stays
    const res = await staysApi.list();
    const all = res.data;

    // 2) ФИЛЬТР "мои"
    // Вариант А (идеально): бэк отдаёт owner/user в stay (например created_by / user)
    // Тогда сделай условие под твой формат.
    const myUserId = auth.user?.id;
    const myUsername = auth.user?.username;

    let mine = all;

    // Если в stay есть user / created_by
    if (myUserId != null) {
      mine = all.filter(s => s.user === myUserId || s.created_by === myUserId);
    } else if (myUsername) {
      mine = all.filter(s => s.user === myUsername || s.created_by === myUsername);
    }

    // Вариант B (если у stay только guest id):
    // Тогда по-хорошему надо знать guest, привязанного к текущему юзеру.
    // Если у тебя guest никак не связан с юзером — это не вычислить корректно.
    // Но можно оставить как есть: показывать последние брони текущей сессии (после брони мы добавляем вручную)
    myBookings.value = mine
      .map(s => ({
        id: s.id,
        room: s.room,
        check_in: s.check_in,
        check_out: s.check_out,
      }))
      .sort((a, b) => String(b.check_in).localeCompare(String(a.check_in)));

  } catch (e) {
    myErr.value = niceError(e);
  } finally {
    loadingMy.value = false;
  }
}

/** ---------- Dialog + booking --------- */
function resetForm() {
  guest.value = {
    passport_number: "",
    last_name: "",
    first_name: "",
    middle_name: "",
    city_from: "",
  };
  stay.value = { room: null, check_in: "", check_out: "" };
  bookErr.value = "";
}

function openDialog(roomId = null) {
  dialog.value = true;
  bookErr.value = "";
  globalOk.value = "";
  if (roomId) stay.value.room = Number(roomId);
}

async function book() {
  bookErr.value = "";
  globalOk.value = "";

  if (!guest.value.passport_number || !guest.value.last_name || !guest.value.first_name || !guest.value.city_from) {
    bookErr.value = "Fill guest fields: passport, last name, first name, city";
    return;
  }
  if (!stay.value.room || !stay.value.check_in) {
    bookErr.value = "Select room and check-in date";
    return;
  }

  const checkOut = stay.value.check_out || stay.value.check_in;

  booking.value = true;
  try {
    // 1) создаём гостя
    const gRes = await guestsApi.create({
      passport_number: guest.value.passport_number,
      last_name: guest.value.last_name,
      first_name: guest.value.first_name,
      middle_name: guest.value.middle_name || "",
      city_from: guest.value.city_from,
    });

    const guestId = gRes.data.id;

    // 2) создаём проживание
    const sRes = await staysApi.create({
      guest: guestId,
      room: stay.value.room,
      check_in: normalizeDate(stay.value.check_in),
      check_out: normalizeDate(checkOut),
    });

    globalOk.value = "Booked ✅";
    dialog.value = false;

    // обновляем список свободных
    await loadRooms();

    // добавляем бронь в "My bookings" сразу, не светя паспорт/ФИО
    myBookings.value = [
      {
        id: sRes.data?.id ?? `${Date.now()}`,
        room: sRes.data?.room ?? stay.value.room,
        check_in: sRes.data?.check_in ?? normalizeDate(stay.value.check_in),
        check_out: sRes.data?.check_out ?? normalizeDate(checkOut),
      },
      ...myBookings.value,
    ];

    resetForm();
  } catch (e) {
    bookErr.value = niceError(e);
  } finally {
    booking.value = false;
  }
}

onMounted(async () => {
  // на всякий — подтянем юзера если нет
  if (!auth.user && auth.token) {
    try { await auth.fetchUser(); } catch (_) {}
  }

  await loadRooms();
  await loadMyBookings();

  const qRoom = route.query.room;
  if (qRoom) openDialog(qRoom);
});

watch(onlyFreeRooms, loadRooms);
</script>

<style scoped>
.rounded-xl { border-radius: 18px; }
.pill { border-radius: 999px; }
</style>

