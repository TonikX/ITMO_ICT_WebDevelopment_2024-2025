<template>
  <div>
    <h2>Список книг</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Авторы</th>
          <th>Издательство</th>
          <th>Год издания</th>
          <th>Раздел</th>
          <th>Шифр</th>
          <th>Экземпляры</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.id }}</td>
          <td>{{ book.title }}</td>
          <td>{{ formatAuthors(book.authors) }}</td>
          <td>{{ book.publisher }}</td>
          <td>{{ book.publication_year }}</td>
          <td>{{ book.section }}</td>
          <td>
            <template v-if="editingBookId === book.id">
              <input v-model="newCode" placeholder="Введите новый шифр" />
              <button @click="submitCodeUpdate(book.id)">Сохранить</button>
              <button @click="cancelEdit">Отмена</button>
            </template>
            <template v-else>
              {{ book.code }}
              <button @click="editCode(book)">Изменить шифр</button>
            </template>
          </td>
          <td>
            <ul v-if="book.copies && book.copies.length">
              <li v-for="(copy, index) in book.copies" :key="index">
                {{ copy.room || 'Неизвестно' }}: {{ copy.quantity }}
              </li>
            </ul>
            <span v-else>Нет данных</span>
          </td>
          <td>
            <button @click="$emit('delete', book.id)">Удалить</button>
            <button v-if="editingBookId !== book.id" @click="editCode(book)">Изменить шифр</button>
            <button @click="$emit('discard', book.id)">Списать</button>
            <button @click="openTransferModal(book)">Переместить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="transferBook" class="modal">
      <div class="modal-content">
        <h3>Перемещение книги "{{ transferBook.title }}"</h3>
        <form @submit.prevent="transfer">
          <div>
            <label for="sourceRoom">Источник:</label>
            <select id="sourceRoom" v-model="sourceRoomId" required>
              <option disabled value="">Выберите зал</option>
              <option v-for="room in availableRooms" :key="room.id" :value="room.id">
                {{ room.name }}
              </option>
            </select>
          </div>

          <div>
            <label for="targetRoom">Назначение:</label>
            <select id="targetRoom" v-model="targetRoomId" required>
              <option disabled value="">Выберите зал</option>
              <option v-for="room in availableRooms" :key="room.id" :value="room.id">
                {{ room.name }}
              </option>
            </select>
          </div>

          <div>
            <label for="quantity">Количество:</label>
            <input id="quantity" type="number" v-model="transferQuantity" min="1" required />
          </div>

          <div class="buttons">
            <button type="submit">Переместить</button>
            <button type="button" @click="closeTransferModal">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    books: {
      type: Array,
      required: true,
    },
    availableRooms: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      editingBookId: null,
      newCode: "",
      transferBook: null,
      sourceRoomId: null,
      targetRoomId: null,
      transferQuantity: 1,
    };
  },
  methods: {
    formatAuthors(authors) {
      if (Array.isArray(authors)) return authors.join(", ");
      if (typeof authors === "string") return authors;
      return "Не указаны";
    },
    editCode(book) {
      this.editingBookId = book.id;
      this.newCode = book.code;
    },
    cancelEdit() {
      this.editingBookId = null;
      this.newCode = "";
    },
    submitCodeUpdate(bookId) {
      if (!this.newCode.trim()) {
        alert("Введите корректный шифр книги.");
        return;
      }
      this.$emit("updateBookCode", { id: bookId, new_code: this.newCode });
      this.cancelEdit();
    },
    openTransferModal(book) {
      this.transferBook = book;
      this.sourceRoomId = null;
      this.targetRoomId = null;
      this.transferQuantity = 1;
    },
    closeTransferModal() {
      this.transferBook = null;
      this.sourceRoomId = null;
      this.targetRoomId = null;
      this.transferQuantity = 1;
    },
    transfer() {
      if (!this.sourceRoomId || !this.targetRoomId || !this.transferQuantity) {
        alert("Заполните все поля для перемещения.");
        return;
      }
      this.$emit("transfer", {
        bookId: this.transferBook.id,
        sourceRoomId: this.sourceRoomId,
        targetRoomId: this.targetRoomId,
        quantity: this.transferQuantity,
      });
      this.closeTransferModal();
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
  text-transform: uppercase;
}

button {
  margin: 5px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px 30px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin-bottom: 20px;
  text-align: center;
}

.modal-content form div {
  margin-bottom: 15px;
}

.modal-content label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.modal-content select,
.modal-content input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.modal-content .buttons {
  display: flex;
  justify-content: space-between;
}

.modal-content button[type="submit"] {
  background-color: #28a745;
  color: white;
}

.modal-content button[type="button"] {
  background-color: #dc3545;
  color: white;
}

.modal-content button[type="submit"]:hover {
  background-color: #218838;
}

.modal-content button[type="button"]:hover {
  background-color: #c82333;
}
</style>
