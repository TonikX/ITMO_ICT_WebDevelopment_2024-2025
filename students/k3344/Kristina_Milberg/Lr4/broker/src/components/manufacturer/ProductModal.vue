<script setup>
import {ref, watch} from "vue";


const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  manufacturer: {
    type: Object
  },
  productData: {
    type: Object,
    default: () => ({name: "", production_date: "", quantity: "", expiry_period: "", product_group_name: "", manufacturer: ""}),
  },
  mode: {
    type: String,
    default: "add",
  },
});


const emits = defineEmits(["update:modelValue", "save-product"]);

const formData = ref({...props.productData});
formData.value.manufacturer = props.manufacturer;

watch(
    () => props.productData,
    (newVal) => {
      formData.value = {...newVal};
    }
);


function closeModal() {
  emits("update:modelValue", false);
}

function handleSubmit() {
  emits("save-product", formData.value);
  closeModal();
}
</script>

<template>
  <v-dialog :model-value="modelValue" @update:model-value="closeModal" persistent max-width="500">
    <v-card>
      <v-card-title>{{ "Добавить продукт" }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field v-model="formData.name" label="Название" required></v-text-field>
          <v-text-field v-model="formData.production_date" label="Дата изготовления" type="date" required></v-text-field>
          <v-text-field v-model="formData.quantity" label="Количество" required type="number"></v-text-field>
          <v-text-field v-model="formData.expiry_period" label="Срок хранения"  type="number" required></v-text-field>
          <v-text-field v-model="formData.product_group_name" label="Категория" required></v-text-field>
          <v-text-field v-model="formData.manufacturer" label="Производитель" :text="manufacturer.name" required disabled></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="secondary" @click="closeModal">Отмена</v-btn>
        <v-btn color="primary" @click="handleSubmit">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
