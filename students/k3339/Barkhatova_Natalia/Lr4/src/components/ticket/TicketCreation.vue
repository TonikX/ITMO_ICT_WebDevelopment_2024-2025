<template>
  <div class="ticket-purchase">
    <div class="session-info">
      <h2>{{ session?.movie?.name }}</h2>
      <p><strong>Время:</strong> {{ formattedStartTime }}</p>
      <p><strong>Зал:</strong> {{ session?.hall?.name }}</p>
    </div>

    <div class="hall-selection">
      <h3>Выберите ваши места</h3>
      <HallBuilder
          :hall="session?.hall"
          :isEditing="false"
          :sessionId="sessionId"
      />
    </div>
    <button class="buy-ticket-btn" @click="buyTickets">Забронировать билет</button>
  </div>
</template>

<script>
import {computed, defineComponent, onMounted} from 'vue';
import HallBuilder from '@/components/hall/HallBuilder.vue';
import {useRoute} from 'vue-router';
import {useSessionStore} from '@/stores/session.js';
import {useMovieStore} from '@/stores/movie.js';
import {useHallStore} from '@/stores/hall.js';
import {useAuthStore} from "@/stores/auth.js";
import {useTicketStore} from "@/stores/ticket.js";
import router from "@/router/index.js";

export default defineComponent({
  components: {HallBuilder},
  setup() {
    const route = useRoute();
    const sessionId = route.params.sessionId;

    const sessionStore = useSessionStore();
    const authStore = useAuthStore();
    const ticketStore = useTicketStore();
    const movieStore = useMovieStore();
    const hallStore = useHallStore();
    const selectedSeats = computed(() => ticketStore.selectedSeats);
    const session = computed(() => {
      return sessionStore.sessions.find(s => s.id === sessionId);
    });

    const formattedStartTime = computed(() => {
      if (!session.value) return '';
      const date = new Date(session.value.startTime);
      return date.toLocaleString('en-GB', {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit',
      });
    });

    const buyTickets = async () => {
      if (!session.value || selectedSeats.length === 0) {
        alert("Please select at least one seat.");
        return;
      }
      try {
        const ticketPromises = selectedSeats.value.map(seat => {
          const ticket = {
            userId: authStore.user.id,
            sessionId: session.value.id,
            seatId: seat.id,
          };
          return ticketStore.addTicket(ticket);
        });

        await Promise.all(ticketPromises);
        ticketStore.clearSelectedSeats();
        localStorage.setItem('purchaseSuccess', 'true');
        router.push('/tickets');
      } catch (error) {
        console.error("Error purchasing tickets:", error);
      }
    };


    onMounted(() => {
      sessionStore.fetchSessions();
      movieStore.fetchMovies();
      hallStore.fetchHalls();
    })

    return {
      session,
      formattedStartTime,
      buyTickets,
      sessionId
    };
  },
});
</script>

<style>
.ticket-purchase {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
  text-align: center;
}

.session-info {
  margin-bottom: 20px;
}

.session-info h2 {
  font-size: 28px;
  margin-bottom: 10px;
}

.session-info p {
  font-size: 18px;
  margin: 4px 0;
}

.hall-selection h3 {
  font-size: 24px;
  margin-bottom: 10px;
  font-family: 'Great Vibes', cursive;
  color: #800020;
}

.buy-ticket-btn {
  display: inline-block;
  margin-top: 20px;
  background-color: #FFAA33;
  color: #fff;
  padding: 12px 25px;
  text-decoration: none;
  border-radius: 25px;
  font-size: 18px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.buy-ticket-btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}
</style>