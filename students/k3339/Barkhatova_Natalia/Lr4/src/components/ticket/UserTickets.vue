<template>
  <div class="tickets">
    <h1>Ваши билеты</h1>

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <Modal v-if="isPurchaseSuccessful" @close="closeModal">
      <h3>Поздравляем!</h3>
      <p>Ваши билеты успешно забронированы</p>
      <button @click="closeModal">Закрыть</button>
    </Modal>

    <ul v-if="tickets.length">
      <li v-for="ticket in tickets" :key="ticket.id" class="ticket-item">
        <div class="ticket-code">
          <strong>Код билета:</strong> {{ ticket.ticketCode }}
        </div>
        <div>
          <strong>Фильм:</strong> {{ ticket.session.movie.name }}
        </div>
        <div>
          <strong>Зал:</strong> {{ ticket.session.hall.name }}
        </div>
        <div>
          <strong>Время сеанса:</strong> {{ formatDate(ticket.session.startTime) }}
        </div>
        <div>
          <strong>Место:</strong> {{ ticket.seat.number }} ({{ translateSeatType(ticket.seat.type) }})
        </div>
        <div>
          <strong>Дата и время бронирования:</strong> {{ formatDate(ticket.purchasedAt) }}
        </div>
      </li>
    </ul>
    <div v-else>Билеты недоступны.</div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { useTicketStore } from "@/stores/ticket.js";
import Modal from "@/components/Modal.vue";

export default {
  name: 'UserTickets',
  components: { Modal },
  setup() {
    const ticketStore = useTicketStore();
    const tickets = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const isPurchaseSuccessful = ref(false);

    onMounted(() => {
      const purchaseStatus = localStorage.getItem('purchaseSuccess');
      if (purchaseStatus === 'true') {
        isPurchaseSuccessful.value = true;
        localStorage.removeItem('purchaseSuccess');
      }
    });

    const closeModal = () => {
      isPurchaseSuccessful.value = false;
    };

    const fetchTickets = async () => {
      try {
        await ticketStore.fetchCurrentUserTickets();
        tickets.value = ticketStore.tickets;
      } catch (err) {
        error.value = 'Failed to load tickets. Please try again later.';
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      };
      return date.toLocaleString('ru', options);
    };

    const translateSeatType = (type) => {
      const seatTypes = {
        STANDARD: 'Обычное',
        VIP: 'VIP',
        HANDICAPPED: 'Для инвалидов',
        COUPLE: 'Парное',
      };
      return seatTypes[type] || 'Неизвестно';
    };

    onMounted(() => {
      fetchTickets();
    });

    return {
      tickets,
      loading,
      error,
      formatDate,
      translateSeatType,
      isPurchaseSuccessful,
      closeModal,
    };
  },
};
</script>

<style>
.tickets {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
}

.tickets h1 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 20px;
}

.loading,
.error {
  font-size: 18px;
  text-align: center;
  margin: 20px 0;
}

.error {
  color: #D32F2F;
}

.ticket-item {
  background-color: #FFF8DC;
  border: 1px solid #800020;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  font-family: 'Great Vibes', cursive;
  color: #333;
}

.ticket-code {
  font-weight: bold;
  background-color: #FFAA33;
  color: #fff;
  padding: 5px;
  border-radius: 5px;
  text-align: center;
  font-size: 18px;
  margin-bottom: 10px;
}
ul {
  list-style-type: none;
  padding-left: 0;
  margin: 0;
}

.ticket-item {
  background-color: #FFF8DC;
  border: 1px solid #800020;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  font-family: 'Great Vibes', cursive;
  color: #333;
}
</style>
