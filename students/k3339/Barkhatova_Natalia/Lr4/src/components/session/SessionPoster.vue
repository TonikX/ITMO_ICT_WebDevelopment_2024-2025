<template>
  <div class="session-poster">
    <div class="poster-header">
      <h3>{{ session.movie.name }}</h3>
      <p>{{ session.hall.name }}</p>
    </div>
    <div class="poster-body">
      <p><strong>Время начала:</strong> {{ formattedStartTime }}</p>
      <p><strong>Цена:</strong> {{ session.price }} ₽</p>
      <p><strong>Описание:</strong> {{ session.movie.description || 'Нет описания' }}</p>
    </div>
    <router-link :to="`/sessions/${session.id}/buy`" class="buy-ticket-button">
      Забронировать билет
    </router-link>
  </div>
</template>
<script>
import {computed} from 'vue';

export default {
  props: {
    session: Object, // Данные о сеансе
  },
  setup(props) {
    const formattedStartTime = computed(() => {
      const date = new Date(props.session.startTime);
      const options = {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      };
      return date.toLocaleString('ru', options);
    });

    return {
      formattedStartTime,
    };
  },
};
</script>


<style>
.session-poster {
  background-color: #FFF8DC;
  border: 2px solid #800020;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  font-family: 'Great Vibes', cursive;
}

.poster-header h3 {
  font-size: 24px;
  color: #800020;
  margin: 0;
  text-align: left;
}

.poster-header p {
  margin: 5px 0;
  color: #555;
  font-size: 16px;
  text-align: left;
}

.poster-body p {
  margin: 8px 0;
  color: #333;
  font-size: 16px;
  text-align: left;
}

.buy-ticket-button {
  display: block;
  margin-top: 10px;
  padding: 10px;
  background-color: #FFAA33;
  color: #fff;
  text-align: center;
  text-decoration: none;
  border-radius: 25px;
  font-size: 18px;
  transition: background-color 0.3s, transform 0.3s;
  cursor: pointer;
}

.buy-ticket-button:hover {
  background-color: #800020;
  transform: scale(1.05);
}
</style>
