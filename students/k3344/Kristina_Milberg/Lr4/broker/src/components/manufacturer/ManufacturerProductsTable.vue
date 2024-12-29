<script setup>
import {computed, ref} from "vue";

const props = defineProps({
  products: Array,
});
ref(false);
const tableData = computed(() =>
    props.products.map((product) => ({
      id: product.id,
      productName: product.name,
      productGroup: product.product_group_name,
      quantity: product.quantity,
    }))
);

</script>

<template>
  <div class="product-table">
    <h1>Список товаров</h1>
    <table>
      <thead>
      <tr>
        <th>Название товара</th>
        <th>Категория товара</th>
        <th>Количество</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="product in tableData" :key="product.id">
        <td>{{ product.productName }}</td>
        <td>{{ product.productGroup }}</td>
        <td>{{ product.quantity }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>


<style scoped>
.product-table {
  width: 100%;
  margin: 0;
  padding: 20px 10px;
  color: #fff;
}
h1 {
  margin-bottom: 20px;
  font-size: 24px;
  text-align: left;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

thead {
  background-color: #444;
  color: #fff;
}

th,
td {
  padding: 10px;
  text-align: left;
  border: 1px solid #555;
}

tbody tr:nth-child(even) {
  background-color: #333;
}
</style>