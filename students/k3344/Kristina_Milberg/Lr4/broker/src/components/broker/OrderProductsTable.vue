<script setup>
import {computed, ref} from "vue";
import OrderModal from "@/components/broker/OrderModal.vue";

const props = defineProps({
  batches: Array,
  isOpened: Boolean
});

const isEditModalVisible = ref(false);
const selectedBatch = ref({})

const emit = defineEmits(["delete-batch", "edit-batch"]);

const tableData = computed(() =>
    props.batches.map((batch) => ({
      id: batch.id,
      productName: batch.product.name,
      pricePerUnit: batch.price_per_unit,
      quantity: batch.quantity,
      totalCost: batch.quantity * batch.price_per_unit,
    }))
);

function deleteBatch(id) {
  emit("delete-batch", id);
}

function editBatch(batch) {
  emit("edit-batch", batch);
  isEditModalVisible.value = false;
}


function handleEdit(batch) {
  selectedBatch.value = {...batch};
  console.log("selectedBatch")
  console.log(selectedBatch.value)
  isEditModalVisible.value = true;
}

</script>

<template>
  <div class="product-table">
    <h1>Список товаров</h1>
    <table>
      <thead>
      <tr>
        <th>Название товара</th>
        <th>Цена за единицу</th>
        <th>Количество</th>
        <th>Суммарная стоимость</th>
        <th v-if="isOpened">Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="batchRow in tableData" :key="batchRow.id">
        <td>{{ batchRow.productName }}</td>
        <td>{{ batchRow.pricePerUnit }}</td>
        <td>{{ batchRow.quantity }}</td>
        <td>{{ batchRow.totalCost }}</td>
        <td v-if="isOpened">
          <v-btn-group>
            <v-btn class="edit-btn" @click="handleEdit(batchRow)" text="Редактировать"/>
            <v-btn class="delete-btn" @click="deleteBatch(batchRow.id)" text="Удалить"/>
          </v-btn-group>
        </td>
        <OrderModal
            v-model="isEditModalVisible"
            :batch="selectedBatch"
            @edit-batch="editBatch"
        />
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

.edit-btn {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-weight: bold;
  margin-right: 5px;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn {
  background-color: #dc3545;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-weight: bold;
}

.delete-btn:hover {
  background-color: #a71d2a;
}
</style>
