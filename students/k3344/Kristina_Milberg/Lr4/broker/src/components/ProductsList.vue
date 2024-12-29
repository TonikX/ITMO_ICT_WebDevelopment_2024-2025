<script setup>
import {ref} from "vue";
import axios from "axios";
import router from "@/utils/router.js";

defineProps({
  products: Array,
});


function filterInput(inputEvent) {
  if (!inputEvent.target.value.length || inputEvent.key === "Backspace") {
    return true;
  }

  if (!Number.isInteger(Number(inputEvent.key))) {
    inputEvent.preventDefault();
  }

  return true;
}

const productQuantities = ref({});
const productPrices = ref({});

function toggleQuantityInput(productId) {
  if (productQuantities.value[productId] !== undefined) {
    delete productQuantities.value[productId];
    delete productPrices.value[productId];
  } else {
    productQuantities.value[productId] = 1; // Инициализируем количество
    productPrices.value[productId] = ""; // Инициализируем цену
  }
}

function incrementQuantity(productId) {
  if (productQuantities.value[productId] !== undefined) {
    productQuantities.value[productId]++;
  }
}

function decrementQuantity(productId) {
  if (productQuantities.value[productId] > 1) {
    productQuantities.value[productId]--;
  } else {
    delete productQuantities.value[productId];
    delete productPrices.value[productId];
  }
}

async function addProduct(productId) {
  const quantity = productQuantities.value[productId];
  const price = productPrices.value[productId];
  if (quantity !== undefined && price !== undefined) {
    await axios.post(
        `/product/${productId}/order/`,
        {quantity: quantity, price_per_unit: price}
    ).catch(error => console.log(error));
  } else {
    console.error("Количество или цена не указаны.");
  }
}
</script>

<template>
  <div class="cards-container">
    <div
        v-for="product in products"
        :key="product.id"
        class="card-wrapper"
    >
      <v-card class="my-card" outlined>
        <template #title>{{ product.name }}</template>
        <template #text>
          <div class="product-info">
            Количество: {{ product.quantity }}<br/>
            Категория: {{ product.product_group }}
          </div>
        </template>

        <template #actions>
          <div v-if="productQuantities[product.id] !== undefined" class="product-controls">
            <div class="quantity-section">
              <v-text-field
                  v-model="productQuantities[product.id]"
                  type="number"
                  append-icon="mdi-plus"
                  prepend-icon="mdi-minus"
                  min="1"
                  class="quantity-input"
                  variant="outlined"
                  hide-details
                  hide-spin-buttons
                  @click:append="incrementQuantity(product.id)"
                  @click:prepend="decrementQuantity(product.id)"
                  @keydown="filterInput"
              ></v-text-field>
            </div>

            <v-text-field
                v-model="productPrices[product.id]"
                type="number"
                min="0"
                placeholder="Цена"
                class="price-input"
                variant="outlined"
                hide-details
                hide-spin-buttons
                style="width: 100%; margin-top: 8px;"
                @keydown="filterInput"
            ></v-text-field>

            <v-btn
                color="primary"
                class="ok-btn"
                @click="addProduct(product.id)"
                style="width: 100%; margin-top: 8px;"
            >
              Ок
            </v-btn>
          </div>
          <div v-else>
            <v-btn
                color="primary"
                @click="router.push(`/products/${product.id}/`)"
                class="add-btn"
                text="Подробнее"
            />
            <v-btn
                color="primary"
                @click="toggleQuantityInput(product.id)"
                class="add-btn"
                text="Добавить"
            />
          </div>
        </template>
      </v-card>
    </div>
  </div>
</template>

<style scoped>
.cards-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
}

.card-wrapper {
  flex: 1 1 calc(25% - 16px);
  max-width: calc(25% - 16px);
}

.my-card {
  background-color: #424242;
  color: #ffffff;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
  border: 1px solid #616161;
  transition: transform 0.2s ease-in-out;
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px;
}

.my-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.3);
}

.product-info {
  margin-bottom: 12px;
}

.product-controls {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.quantity-section {
  flex-direction: row;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
}

.quantity-input {
  font-size: 14px;
  text-align: center;
}

.quantity-input >>> input {
  padding: 0;
  text-align: center;
  min-height: 12px;
  min-width: 30px;
}

.price-input {
  width: 80%;
  font-size: 14px;
  text-align: center;
}

.price-input >>> input {
  padding: 4px;
  min-height: 24px;
  text-align: center;
}

.ok-btn {
  width: 80%;
  margin-top: 12px;
  font-size: 14px;
}

.add-btn {
  font-size: 14px;
  text-align: center;
  width: 100%;
}
</style>