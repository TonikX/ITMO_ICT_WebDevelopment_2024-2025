<template>
  <div
      class="seat"
      :class="[
      seat.type.toLowerCase(),
      { selected: isSelected },
      { occupied: isOccupied }
    ]"
      @click="handleClick"
  >
    {{ seat.number }}
  </div>

  <Modal v-if="showEditor && isAdmin" @close="closeEditor">
    <h3 class="modal-title">Редактировать Место</h3>
    <form @submit.prevent="saveSeat" class="seat-form">
      <label for="seat-number">
        Номер Места:
        <input
            id="seat-number"
            v-model="editableSeat.number"
            type="number"
            min="1"
            required
            class="form-input"
        />
      </label>
      <label for="seat-type">
        Тип места:
        <select
            id="seat-type"
            v-model="editableSeat.type"
            class="form-select"
        >
          <option value="STANDARD">Обычное</option>
          <option value="VIP">VIP</option>
          <option value="HANDICAPPED">Для людей с инвалидностью</option>
          <option value="COUPLE">Для пары</option>
        </select>
      </label>

      <div class="modal-actions">
        <button type="submit" class="save-btn">Сохранить</button>
        <button type="button" class="delete-btn" @click="removeSeat">Удалить</button>
      </div>
    </form>
  </Modal>
</template>

<script>
import {computed, defineComponent, onMounted, ref} from 'vue';
import Modal from '@/components/Modal.vue';
import {useAuthStore} from "@/stores/auth.js";
import {useTicketStore} from "@/stores/ticket.js";
import {useOccupiedSeatsStore} from "@/stores/occupiedSeats.js";

export default defineComponent({
  components: {Modal},
  props: {
    seat: {
      type: Object,
      required: true,
    },
    isAdmin: {
      type: Boolean,
      default: false,
    },
    sessionId: {
      type: String,
      required: true,
    },
  },
  emits: ['update', 'remove', 'select'],
  setup(props, {emit}) {
    const showEditor = ref(false);
    const editableSeat = ref({...props.seat});
    const isSelected = ref(false);
    const authStore = useAuthStore();
    const ticketStore = useTicketStore();
    const isAdmin = computed(() => authStore.isAdmin);
    const seatsStore = useOccupiedSeatsStore();

    const isOccupied = computed(() => {
      if (isAdmin.value) {
        return false;
      }
      return seatsStore.occupiedSeats.has(`${props.sessionId}-${props.seat.id}`);
    });

    const fetchStatus = () => {
      seatsStore.fetchSeatStatus(props.sessionId, props.seat.id);
    };

    onMounted(() => {
      if (isAdmin.value) return;
      fetchStatus(props.sessionId, props.seat.id);
    });


    const openEditor = () => {
      if (!isAdmin.value) return;
      showEditor.value = true;
      editableSeat.value = {...props.seat};
    };

    const closeEditor = () => {
      showEditor.value = false;
    };

    const saveSeat = () => {
      emit('update', {...editableSeat.value});
      closeEditor();
    };

    const removeSeat = () => {
      emit('remove');
      closeEditor();
    };

    const handleClick = () => {
      if (isOccupied.value) return;
      if (isAdmin.value) {
        openEditor();
      } else {
        isSelected.value = !isSelected.value;
        emit('select', {seat: props.seat, selected: isSelected.value});
        if (isSelected.value) {
          ticketStore.addSeat(props.seat);
        } else {
          ticketStore.removeSeat(props.seat);
        }
      }
    };

    return {
      showEditor,
      editableSeat,
      isSelected,
      openEditor,
      closeEditor,
      saveSeat,
      removeSeat,
      handleClick,
      isAdmin,
      isOccupied,
    };
  },
});
</script>

<style>
/* Стили для мест */
.seat {
  display: inline-block;
  width: 40px;
  height: 40px;
  margin: 5px;
  padding: 0;
  text-align: center;
  line-height: 40px;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.standard {
  background-color: #39C65C;
}

.vip {
  background-color: #FFD700;
}

.handicapped {
  background-color: #87CEEB;
}

.couple {
  background-color: #FF69B4;
}

.selected {
  position: relative; /* Для псевдоэлементов */
  background-color: #FFF8DC; /* Светлый фон для выделенных элементов */
  border: 2px solid #800020; /* Цвет бордюра для выделенных элементов */
  box-shadow: 0 4px 15px rgba(128, 0, 32, 0.4); /* Более глубокая и мягкая тень */
  transition: all 0.3s ease; /* Плавный переход для анимации */
  transform: scale(1.02); /* Чуть крупнее для акцента */
}

/* Для создания красивого светового эффекта */
.selected::before {
  content: '';
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
  border-radius: 8px;
  background: radial-gradient(
      circle,
      rgba(255, 170, 51, 0.2) 0%,
      rgba(255, 170, 51, 0) 60%
  );
  z-index: -1; /* Под элементом */
  opacity: 0;  /* Начальная прозрачность */
}

.occupied {
  opacity: 0.2;
  cursor: not-allowed;
}

.modal-title {
  font-size: 24px;
  color: #800020;
  text-align: center;
  margin-bottom: 20px;
}

.seat-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #CCC;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: border 0.3s, box-shadow 0.3s;
}

.form-input:focus,
.form-select:focus {
  border-color: #800020;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.5);
  outline: none;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
}

.save-btn,
.delete-btn {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.save-btn {
  background-color: #32CD32;
  color: #fff;
}

.delete-btn {
  background-color: #FF6347;
  color: #fff;
}

.save-btn:hover,
.delete-btn:hover {
  transform: scale(1.05);
}
</style>
