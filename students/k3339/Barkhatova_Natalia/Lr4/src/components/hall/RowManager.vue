<template>
  <div class="row-manager">
    <div class="row-header">
      <span class="row-number">Ряд №{{ row.number }}</span>
      <button
          v-if="isAdmin"
          class="add-seat-btn"
          @click="addSeat">
        + Место
      </button>
      <button
          v-if="isAdmin"
          class="remove-row-btn"
          @click="$emit('remove')">
        Удалить Ряд
      </button>
    </div>
    <div class="error-message">{{ errorMessage }}</div>
    <div class="seats-container">
      <div
          v-for="(seat, index) in row.seats"
          :key="seat.id"
          class="seat-wrapper"
      >
        <SeatManager
            :seat="seat"
            :sessionId="sessionId"
            @update="updateSeat(index, $event)"
            @remove="removeSeat(index)"
        />
      </div>
    </div>
  </div>
</template>


<script>
import {computed, defineComponent, ref} from "vue";
import Modal from "@/components/Modal.vue";
import SeatManager from "@/components/hall/SeatManager.vue";
import {useAuthStore} from "@/stores/auth.js";

export default defineComponent({
  components: {SeatManager, Modal},
  props: {
    row: {
      type: Object,
      required: true,
    },
    errors: {
      type: Object,
      default: () => ({}),
    },
    isAdmin: {
      type: Boolean,
      default: false,
    },
    sessionId: {
      type: String,
      default: "",
    }
  },

  computed: {
    errorMessage() {
      return this.errors || null;
    },
  },

  emits: ["update", "remove"],
  setup(props, {emit}) {
    const showSeatEditor = ref(false);
    const currentSeat = ref(null);
    const currentSeatIndex = ref(null);
    const authStore = useAuthStore();
    const {sessionId} = props;
    const isAdmin = computed(() => authStore.isAdmin);

    const addSeat = () => {
      const newSeat = {number: props.row.seats.length + 1, type: "STANDARD"};
      props.row.seats.push(newSeat);
      emit("update", props.row);
    };

    const updateSeat = (index, newSeat) => {
      props.row.seats[index] = newSeat;
      emit("update", props.row);
    };

    const removeSeat = (index) => {
      props.row.seats.splice(index, 1);
      emit("update", props.row);
    };

    return {
      showSeatEditor,
      currentSeat,
      currentSeatIndex,
      addSeat,
      updateSeat,
      removeSeat,
      isAdmin,
      sessionId
    };
  },
});
</script>


<style>
.row-manager {
  margin-bottom: 20px;
  border: 1px solid #CCC;
  border-radius: 10px;
  padding: 10px 15px;
  background-color: #FFF8DC;
}

.row-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.row-number {
  font-family: 'Pacifico', cursive;
  font-size: 18px;
  color: #800020;
}

button {
  background-color: #FFAA33;
  color: #fff;
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-left: 5px;
}

button.add-seat-btn:hover {
  background-color: #32CD32;
}

button.remove-row-btn:hover {
  background-color: #FF6347;
}

/* Сообщение об ошибке */
.error-message {
  color: #D32F2F;
  font-size: 14px;
  font-family: 'Great Vibes', cursive;
  margin-bottom: 10px;
  text-align: center;
}

.seats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.seat-wrapper {
  flex: 0 0 50px;
}
</style>

