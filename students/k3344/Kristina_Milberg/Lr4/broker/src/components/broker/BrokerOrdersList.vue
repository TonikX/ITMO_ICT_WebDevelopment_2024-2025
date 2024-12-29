<script setup>
import { computed } from "vue";
import { getOrderPaid, getOrderStatus } from "@/utils/functions.js";
import router from "@/utils/router.js";

const props = defineProps({
  orders: Array,
});

defineEmits(["edit-order", "delete-order", "confirm-order"]);

const pendingOrders = computed(() => props.orders.filter((o) => o.status === "Opened"));
const confirmedOrders = computed(() => props.orders.filter((o) => o.status !== "Opened"));
</script>

<template>
  <h3>Требуют подтверждения</h3>
  <div v-if="pendingOrders.length">
    <v-card
        v-for="order in pendingOrders"
        :key="order.id"
        class="mb-4 pending-order"
    >
      <v-card-title>
        Заказ №{{ order.id }} (Требует подтверждения)
      </v-card-title>
      <v-card-text>
        Предоплата: {{ getOrderPaid(order.prepaid) }}<br />
        Дата поставки: {{ order.delivery_date }}<br />
        Статус: {{ getOrderStatus(order.status) }} <br />
        Полная стоимость: {{ order.total_cost }} <br />
        Оплачено: {{ order.total_paid ?? 0 }}<br />
      </v-card-text>
      <v-card-actions>
        <v-btn color="success" class="action-btn" @click="$emit('confirm-order', order.id)">
          Подтвердить
        </v-btn>
        <v-btn color="error" class="action-btn" @click="$emit('delete-order', order.id)">
          Отклонить
        </v-btn>
        <v-btn color="primary" class="action-btn" @click="router.push(`/orders/${order.id}/`)">
          Подробнее
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <p>Нет заказов, требующих подтверждения.</p>
  </div>

  <h3>Подтвержденные заказы</h3>
  <div v-if="confirmedOrders.length">
    <v-card
        v-for="order in confirmedOrders"
        :key="order.id"
        class="mb-4 confirmed-order"
    >
      <v-card-title>
        Заказ №{{ order.id }}
      </v-card-title>
      <v-card-text>
        Предоплата: {{ getOrderPaid(order.prepaid) }}<br />
        Дата поставки: {{ order.delivery_date }}<br />
        Статус: {{ getOrderStatus(order.status) }} <br />
        Полная стоимость: {{ order.total_cost }} рублей <br />
        Оплачено: {{ order.total_paid ?? 0 }}<br />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" class="action-btn" @click="router.push(`/orders/${order.id}/`)">
          Подробнее
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <p>Нет подтвержденных заказов.</p>
  </div>
</template>

<style scoped>
.pending-order {
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: #f8d486;
}

.confirmed-order {
  background-color: #2a2a2a;
  border: 1px solid #444;
  color: #7cfc88;
}

.v-card-title {
  font-weight: bold;
  font-size: 1.1rem;
}

.v-card-text {
  color: #ddd;
}

.v-card-actions {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
}

.action-btn {
  font-weight: bold;
  text-transform: uppercase;
  color: white;
}

</style>
