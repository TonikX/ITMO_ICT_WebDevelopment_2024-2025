<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Редактирование данных</h3>
      <form @submit.prevent="submitForm">
        <label> Фамилия: <input v-model="editedStudent.last_name" type="text" required /> </label>
        <label> Имя: <input v-model="editedStudent.first_name" type="text" required /> </label>
        <label> Отчество: <input v-model="editedStudent.middle_name" type="text" /> </label>
        <label> Пол:
          <select v-model="editedStudent.gender" required>
            <option value="m">Мужской</option>
            <option value="f">Женский</option>
         </select>
        </label>
        <label> Дата рождения: <input v-model="editedStudent.date_of_birth" type="date" required /> </label>
        <label> Номер телефона: <input v-model="editedStudent.phone_number" type="tel" /> </label>
        <label> Почта: <input v-model="editedStudent.email" type="email" /> </label>
        <label> Дата зачисления: <input v-model="editedStudent.registration_date" type="date" required /> </label>
        <div class="actions">
          <button type="submit">Сохранить</button>
          <button class="cancel" type="button" @click="$emit('close')">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editedStudent: { ...this.student },
    };
  },
  methods: {
    submitForm() {
      this.$emit("update", this.editedStudent);
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  width: 94%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

h3 {
  color: #596dff;
  text-align: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
}

label {
  display: block;
  font-weight: bold;
  margin-top: 5%;
}

input,
select,
button {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.actions {
  margin-top: 5%;
}

button {
  background-color: #596dff;
  color: white;
  cursor: pointer;
  margin-top: 2%
}

button:hover {
  background-color: #4759d1;
}

.cancel:hover {
  background: #c5813b;
}

.cancel {
  background: #ffa44b;
}

</style>
