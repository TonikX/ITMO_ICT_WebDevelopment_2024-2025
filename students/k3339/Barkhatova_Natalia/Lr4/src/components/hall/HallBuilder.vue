<template>
  <div class="hall-builder">
    <h2 v-if="isAdmin">{{ isEditing ? 'Изменить зал' : 'Создать зал' }}</h2>

    <div v-if="isAdmin" class="input-container">
      <label for="hall-name">Название зала:</label>
      <input
          id="hall-name"
          v-model="hall.name"
          type="text"
          placeholder="Введите название зала"
      />
      <p v-if="errors.name" class="error">{{ errors.name }}</p>
    </div>

    <div class="legend">
      <div class="legend-item">
        <div class="color-box standard"></div>
        <span>Обычный</span>
      </div>
      <div class="legend-item">
        <div class="color-box vip"></div>
        <span>VIP</span>
      </div>
      <div class="legend-item">
        <div class="color-box handicapped"></div>
        <span>Для людей с инвалидностью</span>
      </div>
      <div class="legend-item">
        <div class="color-box couple"></div>
        <span>Для пары</span>
      </div>
    </div>

    <div class="rows-container" v-if="hall?.rows">
      <RowManager
          v-for="(row, index) in hall.rows"
          :key="index"
          :row="row"
          :errors="getRowError(index)"
          :sessionId="sessionId"
          @update="updateRow(index, $event)"
          @remove="removeRow(index)"
      />
      <p v-if="errors.rows" class="error">{{ errors.rows }}</p>
    </div>

    <button v-if="isAdmin" class="add-row-btn" @click="addRow">+ Добавить ряд</button>
    <button v-if="isAdmin" class="save-btn" @click="saveHall">Сохранить зал</button>
  </div>
</template>

<script>
import {computed, defineComponent, ref} from "vue";
import RowManager from "./RowManager.vue";
import {useHallStore} from "@/stores/hall";
import {useAuthStore} from "@/stores/auth.js";

export default defineComponent({
  components: {RowManager},
  props: {
    hall: {
      type: Object,
      default: () => ({rows: []}),
    },
    isEditing: {
      type: Boolean,
      default: false,
    },
    isAdmin: {
      type: Boolean,
      default: false,
    },
    sessionId: {
      type: String,
      default: "",
    }
  },
  setup(props, {emit}) {
    const errors = ref({});
    const showErrors = ref(false);
    const hallStore = useHallStore();
    const {sessionId} = props;
    const authStore = useAuthStore();
    const isAdmin = computed(() => authStore.isAdmin);
    const addRow = () => {
      props.hall.rows.push({
        number: props.hall.rows.length + 1,
        seats: [],
      });
    };

    const updateRow = (rowIndex, updatedRow) => {
      props.hall.rows.splice(rowIndex, 1, updatedRow);
    };

    const removeRow = (rowIndex) => {
      props.hall.rows.splice(rowIndex, 1);
      props.hall.rows.forEach((row, index) => {
        row.number = index + 1;
      });
    };

    const getRowError = (index) => {
      return errors.value[`rows[${index}].seats`] || null;
    };

    const saveHall = async () => {
      showErrors.value = true;
      try {
        if (props.isEditing) {
          await hallStore.updateHall(props.hall);
        } else {
          await hallStore.addHall(props.hall);
        }

        errors.value = {};
        emit("save", props.hall);
      } catch (error) {
        if (error.response && error.response.data) {
          const serverErrors = error.response.data;
          for (const key in serverErrors) {
            if (Object.prototype.hasOwnProperty.call(serverErrors, key)) {
              errors.value[key] = serverErrors[key];
            }
          }
        } else {
          console.error("Ошибка при сохранении:", error);
        }
      }
    };

    return {
      errors,
      showErrors,
      addRow,
      updateRow,
      removeRow,
      saveHall,
      getRowError,
      sessionId,
      isAdmin
    };
  },
});
</script>

<style>
.hall-builder {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
}

.hall-builder h2 {
  text-align: center;
  font-size: 32px;
  margin-bottom: 20px;
}

.input-container {
  margin-bottom: 20px;
}

.input-container label {
  display: block;
  font-size: 18px;
  margin-bottom: 5px;
}

.input-container input {
  width: 100%;
  padding: 12px;
  border-radius: 5px;
  border: 2px solid #CCC;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: border 0.3s, box-shadow 0.3s;
}

.input-container input:focus {
  border-color: #800020;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.5);
  outline: none;
}

.legend {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-family: 'Great Vibes', cursive;
}

.color-box {
  width: 20px;
  height: 20px;
  margin-right: 5px;
  border-radius: 3px;
  border: 1px solid #333;
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

.button {
  padding: 12px 25px;
  border-radius: 25px;
  border: none;
  margin-top: 15px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.add-row-btn, .save-btn {
  background-color: #FFAA33;
  color: #fff;
}

.add-row-btn:hover, .save-btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}

.error {
  color: #D32F2F;
  font-size: 14px;
  margin-top: -10px;
  margin-bottom: 10px;
  font-family: 'Great Vibes', cursive;
}
</style>