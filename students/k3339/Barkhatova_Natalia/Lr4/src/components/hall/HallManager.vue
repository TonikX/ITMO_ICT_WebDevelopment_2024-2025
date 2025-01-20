<template>
  <div class="hall-manager">
    <h2>Управление залами</h2>

    <button class="add-hall-btn" @click="showAddHallModal">Добавить новый зал</button>

    <HallTable
        :halls="halls"
        @edit="editHall"
        @delete="deleteHall"
    />

    <Modal v-if="showModal" @close="closeModal">
      <HallBuilder
          :hall="hallForm"
          :isEditing="isEditing"
          @save="saveHall"
          @cancel="closeModal"
          class="modal-content"
      />
    </Modal>
  </div>
</template>

<script>
import {computed, onMounted, ref} from 'vue';
import {useHallStore} from '@/stores/hall';
import HallTable from './HallTable.vue';
import Modal from "@/components/Modal.vue";
import HallBuilder from "./HallBuilder.vue";

export default {
  components: {
    HallTable,
    Modal,
    HallBuilder,
  },
  setup() {
    const hallStore = useHallStore();
    const halls = computed(() => hallStore.halls);
    const showModal = ref(false);
    const isEditing = ref(false);
    const hallForm = ref(null);

    const showAddHallModal = () => {
      isEditing.value = false;
      hallForm.value = {name: '', rows: []};
      showModal.value = true;
    };

    const editHall = (hall) => {
      isEditing.value = true;
      hallForm.value = JSON.parse(JSON.stringify(hall));
      showModal.value = true;
    };

    const saveHall = async () => {
      showModal.value = false;
    };

    const deleteHall = async (hallId) => {
      await hallStore.deleteHall(hallId);
    };

    const closeModal = () => {
      showModal.value = false;
    };

    onMounted(async () => {
      await hallStore.fetchHalls();
    });

    return {
      halls,
      showModal,
      isEditing,
      hallForm,
      showAddHallModal,
      editHall,
      saveHall,
      deleteHall,
      closeModal,
    };
  },
};
</script>
<style>
.hall-manager {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
}

.hall-manager h2 {
  font-size: 32px;
  margin-bottom: 20px;
}

.add-hall-btn {
  background-color: #FFAA33;
  color: #fff;
  padding: 12px 25px;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-bottom: 20px;
}

.add-hall-btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}

.modal-content {
  background-color: #FFF8DC;
  padding: 30px;
  border-radius: 10px;
  border: 2px solid #800020;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>